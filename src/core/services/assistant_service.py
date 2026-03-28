import json
import logging
from typing import Type, Any
from uuid import UUID

import aiohttp
from fastapi import HTTPException
from openai import AsyncOpenAI, NOT_GIVEN, NotGiven
from pydantic import ValidationError
from starlette import status

from src.api.response_schemas.check_in import CheckInResponse, AssistantResponse
from src.api.response_schemas.survey import ResearchSurveyFinishResponse
from src.core.prompts.check_in import CHECK_IN
from src.core.prompts.funcs.diary import GET_SUMMARY_LOG_FROM_DAILY_LOGS
from src.core.prompts.funcs.extract_name import EXTRACT_NAME_PROMPT
from prompts.generation.generation import GENERATE_CHARACTERISTIC_PROMPT
from src.core.prompts.funcs.telegram import TELEGRAM_CHARACTERISTIC_DIFF
from prompts.main.psycho import PSYCHO_PROMPT
from src.core.schemas.assistant_response import SummaryResponseSchema
from src.core.services.cache_services.redis_service import RedisService
from src.infrastructure.config.config import config
from src.infrastructure.database.models.base import S

logger = logging.getLogger(__name__)


def clean_message_for_history(message: Any) -> str | None:
    """
    Очищает сообщение перед сохранением в историю.

    - Извлекает самое осмысленное поле (answer, question, precise_question, user_answer)
    - Обрезает результат до ~150–250 токенов (примерно 550–950 символов)
    - Возвращает None, если после очистки ничего осмысленного не осталось.
    """
    if message is None:
        return None

    if isinstance(message, str):
        message = message.strip()
        if not message:
            return None
        try:
            parsed = json.loads(message)
            message = parsed
        except json.JSONDecodeError:
            # обычная строка — продолжаем с ней
            pass

    if not isinstance(message, (dict, list)):
        text = str(message).strip()
        return truncate_to_token_limit(text) if text else None

    def find_meaningful_text(data: Any) -> str | None:
        if isinstance(data, dict):
            for key in ("answer", "question", "precise_question", "user_answer"):
                val = data.get(key)
                if isinstance(val, str) and val.strip():
                    return val.strip()
            for v in data.values():
                result = find_meaningful_text(v)
                if result:
                    return result
        elif isinstance(data, list):
            for item in data:
                result = find_meaningful_text(item)
                if result:
                    return result
        return None

    meaningful = find_meaningful_text(message)
    if meaningful:
        return truncate_to_token_limit(meaningful)

    # Fallback — компактный JSON
    if isinstance(message, dict):
        try:
            compact = json.dumps(message, ensure_ascii=False, separators=(",", ":"))
            if len(compact) > 10:
                return truncate_to_token_limit(compact)
        finally:
            pass

    return None


def truncate_to_token_limit(text: str) -> str:
    """
    Обрезает текст примерно до 150–250 токенов.
    Используем грубую, но очень быструю и надёжную оценку:
    ~4 символа = 1 токен (для смешанного русско-английского текста это хорошее приближение).
    """
    if not text:
        return text

    # Примерно 600–1000 символов → 150–250 токенов
    target_chars = 800  # середина диапазона (≈200 токенов)

    if len(text) <= target_chars + 50:  # небольшой запас
        return text

    # Обрезаем по символам + пытаемся не резать слово посередине
    truncated = text[:target_chars]

    # Отрезаем до последнего пробела, чтобы не обрывать слово (если возможно)
    last_space = truncated.rfind(' ')
    if last_space > target_chars * 0.7:  # обрезаем только если потеряем не слишком много
        truncated = truncated[:last_space]

    return truncated.rstrip() + "…"


class AssistantService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=config.DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
        self._session: aiohttp.ClientSession | None = None

    @staticmethod
    async def check_balance():
        """Асинхронная проверка баланса"""
        try:
            async with aiohttp.ClientSession() as session:
                async with session.get(
                        "https://api.deepseek.com/user/balance",
                        headers={
                            'Accept': 'application/json',
                            'Authorization': f'Bearer {config.DEEPSEEK_API_KEY}'
                        }
                ) as response:
                    balance_data = await response.json()

                    usd_balance_info = next(
                        (item for item in balance_data["balance_infos"] if item["currency"] == "USD"),
                        None
                    )
                    balance_now: float = float(usd_balance_info["total_balance"]) if usd_balance_info else 0.0

                    if balance_now > config.MINIMUM_USD_ON_BALANCE:
                        logger.info(f"Выполняется запрос, на балансе: {balance_now}")
                        return

                    logger.error(f"На балансе недостаточно денег: {balance_now} < {config.MINIMUM_USD_ON_BALANCE}")
                    raise HTTPException(
                        status_code=status.HTTP_402_PAYMENT_REQUIRED,
                        detail="На балансе DeepseekAPI недостаточно денег!"
                    )

        except aiohttp.ClientError as e:
            logger.error(f"Ошибка при проверке баланса: {e}")
            return

    async def get_response(
            self,
            input_query: str,
            prompt: str,
            pydantic_model: Type[S] | None = None,
            temperature: float = 0.3,
            max_tokens: int | NotGiven = NOT_GIVEN
    ) -> S | str:
        """
        Одноразовый запрос к модели без сохранения контекста.
        Используется для случаев, где история не нужна (например, разовые генерации характеристик).
        """
        try:
            await self.check_balance()

            response = await self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": prompt},
                    {"role": "user", "content": input_query},
                ],
                response_format={"type": "json_object"} if pydantic_model else NOT_GIVEN,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            logger.info("статистика по токенам:\n")
            logger.info(response.usage)

            content = response.choices[0].message.content.strip()

            try:
                if pydantic_model:
                    return pydantic_model.model_validate_json(content)
                return content
            except ValidationError as e:
                logger.error(f"Validation error: {e}")
                logger.error(f"Input Query: {input_query}")
                logger.error(f"Raw response: {content}\nModel: {pydantic_model}")
                raise ValueError(f"Invalid assistant response: {e}")

        except Exception as ex:
            logger.error(f"Error in get_response: {ex}")
            raise

    async def get_chat_response(
            self,
            user_id: UUID,
            input_query: str,
            prompt: str,
            redis_service: RedisService,
            pydantic_model: Type[S] | None = None,
            temperature: float = 0.6,
            max_tokens: int | NotGiven = NOT_GIVEN,
            history_limit: int = 40,
    ) -> S | str:
        """
        Запрос с поддержкой контекста (истории диалога).

        Если redis_service и user_id переданы — загружает историю, добавляет новое сообщение
        и сохраняет ответ в историю после успешного ответа.
        """
        try:
            await self.check_balance()

            history = []
            if redis_service:
                try:
                    history = await redis_service.get_history(
                        user_id=user_id,
                        max_messages=history_limit  # с запасом
                    )
                except Exception as e:
                    logger.warning(f"Не удалось загрузить историю для {user_id}: {e}")

            messages = [
                {"role": "system", "content": prompt},
                *history,
                {"role": "user", "content": input_query},
            ]

            response = await self.client.chat.completions.create(
                model="deepseek-chat",
                messages=messages,
                response_format={"type": "json_object"} if pydantic_model else NOT_GIVEN,
                temperature=temperature,
                max_tokens=max_tokens,
            )

            content = response.choices[0].message.content.strip()
            logger.info("статистика по токенам (чат):\n")
            logger.info(response.usage)

            # [ cache ]
            assistant_content = content.strip()
            input_query = clean_message_for_history(message=input_query)
            assistant_message = clean_message_for_history(message=assistant_content)
            try:
                if input_query not in (message['content'] for message in history):  # anti-duplicates
                    if input_query and assistant_message:
                        await redis_service.add_message(user_id, "user", input_query)
                        await redis_service.add_message(user_id, "assistant", assistant_message)
                    else:
                        logger.error("ошибка парсинга ответа для контекста")
                        raise
                else:
                    logger.info(f"дубликат лога пропущен: {input_query}")
            except Exception as e:
                logger.warning(f"Не удалось сохранить историю для {user_id}: {e}")

            # [ response format ]
            try:
                if pydantic_model:
                    return pydantic_model.model_validate_json(content)
                return content
            except ValidationError as e:
                logger.error(f"Validation error in chat: {e}")
                logger.error(f"User message: {input_query}")
                logger.error(f"Raw response: {content}")
                if prompt == PSYCHO_PROMPT:
                    # noinspection PyArgumentList
                    return AssistantResponse(
                        user_answer="шиза дневник не понимает тебя ;( \nпопробуй написать что-то другое"
                    )
                raise ValueError(f"Invalid chat response: {e}")

        except Exception as ex:
            logger.error(f"Error in get_chat_response: {ex}")
            raise

    # [ GENERATION ]
    async def generate_characteristic(
            self,
            characteristic_type: type[S],
            old_characteristic: str,  # старая характеристика + пояснение к полям
    ):
        """генерация характеристики"""

        prompt: str = GENERATE_CHARACTERISTIC_PROMPT
        pydantic_model: type[S] = characteristic_type

        return await self.get_response(
            old_characteristic,
            prompt=prompt,
            pydantic_model=pydantic_model
        )

    async def generate_telegram_message_characteristic_diff(
            self,
            input_query: str
    ) -> str:
        return await self.get_response(
            input_query,
            prompt=TELEGRAM_CHARACTERISTIC_DIFF
        )

    # [ CHECK IN ]

    async def get_check_in(
            self,
            user_message: str
    ) -> ...:
        """Возвращает список названий характеристик которые нужно учитывать"""
        prompt: str = CHECK_IN
        pydantic_model: type[S] = CheckInResponse

        return await self.get_response(
            user_message,
            prompt=prompt,
            pydantic_model=pydantic_model
        )

    async def get_shiza_response(
            self,
            user_message: str,
            user_id: UUID,
            prompt: str,
            redis_service: RedisService,
            temperature: float | None = 0.6,
            user_profile: str | None = None,
            pydantic_model: type[S] = None
    ) -> AssistantResponse | ResearchSurveyFinishResponse:
        """ШИЗА ответ"""
        profile_text = ""
        if user_profile:
            profile_text = "\n\nТекущий профиль пользователя:\n" + user_profile
            logger.info(profile_text)

        full_prompt: str = prompt + profile_text

        return await self.get_chat_response(
            input_query=user_message,
            prompt=full_prompt,
            pydantic_model=AssistantResponse if not pydantic_model else pydantic_model,
            temperature=temperature,
            max_tokens=600,
            user_id=user_id,
            redis_service=redis_service
        )

    # [ SUMMARIZE ]

    async def summarize_user_daily_logs(
            self,
            user_logs: str
    ) -> SummaryResponseSchema:
        """создает один рассказ из всех логов"""
        prompt: str = GET_SUMMARY_LOG_FROM_DAILY_LOGS

        pydantic_model: type[S] = SummaryResponseSchema

        return await self.get_response(
            input_query=user_logs,
            pydantic_model=pydantic_model,
            prompt=prompt
        )

    # [ FUNCS ]

    async def extract_user_name(self, input_query: str) -> str:
        return await self.get_response(
            input_query,
            prompt=EXTRACT_NAME_PROMPT
        )
