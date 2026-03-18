import json
import logging
from typing import Type, Any
from uuid import UUID

import aiohttp
from openai import AsyncOpenAI, NOT_GIVEN, NotGiven, APIError
from pydantic import ValidationError

from src.api.request_schemas.research import ResearchSurveyFinishRequest
from src.api.response_schemas.psycho import PsychoResponse
from src.api.response_schemas.research import ResearchSurveyFinishResponse, ResearchSurveyResponse, \
    ResearchDefaultResponse
from src.core.prompts import GET_PROMPT_BY_SCHEMA_TYPE
from src.core.prompts.check_in.psycho import CHECK_IN_PSYCHO_PROMPT
from src.core.prompts.check_in.research import TO_LEARN_SURVEY_FINISH, RESEARCH_SURVEY_PROMPT, RESEARCH_DEFAULT_PROMPT
from src.core.prompts.diary import GET_SUMMARY_LOG_FROM_DAILY_LOGS
from src.core.schemas.assistant_response import SummaryResponseSchema
from src.core.services.cache_services.redis_service import RedisService
from src.infrastructure.config.config import config
from src.infrastructure.database.models.base import S

logger = logging.getLogger(__name__)


def clean_message_for_history(message: Any) -> str | None:
    """
    Очищает сообщение перед сохранением в историю.

    Возвращает:
    - строку с "answer", "question", "precise_question" или "user_answer" — если нашлось
    - None — если ничего осмысленного не найдено (тогда сообщение НЕ сохраняется)
    """
    if message is None:
        return None

    # Если уже строка — пробуем распарсить как JSON
    if isinstance(message, str):
        message = message.strip()
        if not message:
            return None
        try:
            parsed = json.loads(message)
            message = parsed
        except json.JSONDecodeError:
            # обычная строка — возвращаем
            return message

    # Теперь работаем с dict / list
    if not isinstance(message, (dict, list)):
        return str(message).strip() or None

    # Рекурсивный поиск "answer", "question", "precise_question", "user_answer"
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

    # Если ничего осмысленного не нашли — возвращаем None (не сохраняем)
    if meaningful:
        return meaningful

    # Последний fallback — компактный JSON или строка
    if isinstance(message, dict):
        try:
            compact = json.dumps(message, ensure_ascii=False, separators=(",", ":"))
            if len(compact) > 10:  # минимальная длина, чтобы не сохранять пустышки
                return compact
        except:
            pass

    return None  # ничего не сохраняем


class AssistantService:
    def __init__(self):
        self.client = AsyncOpenAI(api_key=config.DEEPSEEK_API_KEY, base_url="https://api.deepseek.com")
        self._session: aiohttp.ClientSession | None = None

    async def check_balance(self):
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
                    raise APIError(message="На балансе DeepseekAPI недостаточно денег!")

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
            history_limit: int = 20,
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

            try:
                assistant_content = content.strip()
                input_query = clean_message_for_history(message=input_query)
                assistant_message = clean_message_for_history(message=assistant_content)

                if input_query:
                    await redis_service.add_message(user_id, "user", input_query)
                else:
                    logger.error("ошибка парсинга ответа для контекста")
                    raise

                if assistant_message:
                    await redis_service.add_message(user_id, "assistant", assistant_message)
                else:
                    logger.error("ошибка парсинга ответа для контекста")
                    raise

            except Exception as e:
                logger.warning(f"Не удалось сохранить историю для {user_id}: {e}")

            try:
                if pydantic_model:
                    return pydantic_model.model_validate_json(content)
                return content
            except ValidationError as e:
                logger.error(f"Validation error in chat: {e}")
                logger.error(f"User message: {input_query}")
                logger.error(f"Raw response: {content}")
                raise ValueError(f"Invalid chat response: {e}")

        except Exception as ex:
            logger.error(f"Error in get_chat_response: {ex}")
            raise

    # [ GENERATION ]

    async def generate_characteristic(
            self,
            characteristic_type: type[S],
            messages_text: str,
    ):
        """генерация характеристики"""

        prompt = GET_PROMPT_BY_SCHEMA_TYPE.get(characteristic_type)
        pydantic_model: type[S] = characteristic_type

        return await self.get_response(
            messages_text,
            prompt=prompt,
            pydantic_model=pydantic_model
        )

    # [ CHECK IN ]

    async def get_psycho_response(
            self,
            user_message: str,
            user_id: UUID,
            redis_service: RedisService,
            user_characteristics: str | None = None,
    ) -> PsychoResponse:
        """PSYCHO"""
        profile_text = ""
        if user_characteristics:
            profile_text = "\n\nТекущий профиль пользователя:\n" + user_characteristics
            logger.info(profile_text)

        full_prompt: str = CHECK_IN_PSYCHO_PROMPT + profile_text

        return await self.get_chat_response(
            input_query=user_message,
            prompt=full_prompt,
            pydantic_model=PsychoResponse,
            temperature=0.6,  # чуть выше, чтобы был живой стиль
            max_tokens=600,
            user_id=user_id,
            redis_service=redis_service
        )

    async def get_research_default_response(
            self,
            user_message: str,
            user_id: UUID,
            redis_service: RedisService,
            user_characteristics: str | None = None,
    ) -> ResearchDefaultResponse:
        """research: DEFAULT"""
        profile_text = ""
        if user_characteristics:
            profile_text = "\n\nТекущий профиль пользователя:\n" + user_characteristics
            logger.info(profile_text)

        full_prompt: str = RESEARCH_DEFAULT_PROMPT + profile_text

        return await self.get_chat_response(
            input_query=user_message,
            prompt=full_prompt,
            pydantic_model=ResearchDefaultResponse,
            temperature=0.6,  # чуть выше, чтобы был живой стиль
            max_tokens=600,
            user_id=user_id,
            redis_service=redis_service
        )

    async def get_research_survey_response(
            self,
            user_message: str,
            user_id: UUID,
            redis_service: RedisService,
            user_characteristics: str | None = None
    ) -> ResearchSurveyResponse:
        """SURVEY:

        получить пак с ответами
        """
        profile_text = ""
        if user_characteristics:
            profile_text = "\n\nТекущий профиль пользователя:\n" + user_characteristics
            logger.info(profile_text)

        full_prompt: str = RESEARCH_SURVEY_PROMPT + profile_text

        return await self.get_chat_response(
            input_query=user_message,
            prompt=full_prompt,
            pydantic_model=ResearchSurveyResponse,
            user_id=user_id,
            redis_service=redis_service
        )

    async def get_to_learn_survey_finish_response(
            self,
            request: ResearchSurveyFinishRequest,
            user_id: UUID,
            redis_service: RedisService,
    ) -> ResearchSurveyFinishResponse:
        """SURVEY:

        Финальная обработка
        """
        prompt: str = TO_LEARN_SURVEY_FINISH

        return await self.get_chat_response(
            input_query=request.model_dump_json(),
            prompt=prompt,
            pydantic_model=ResearchSurveyFinishResponse,
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
