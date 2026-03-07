import json
import logging
from typing import Type, Any

import aiohttp
from openai import AsyncOpenAI, NOT_GIVEN, NotGiven, APIError
from pydantic import ValidationError

from src.api.request_schemas.research import ResearchSurveyFinishRequest
from src.api.response_schemas.psycho import PsychoResponse
from src.api.response_schemas.research import ResearchSurveyFinishResponse, ResearchSurveyResponse, \
    ResearchDefaultResponse
from src.core.prompts import GET_PROMPT_BY_SCHEMA_TYPE
from src.core.prompts.check_in.psycho import CHECK_IN_PSYCHO_PROMPT
from src.core.prompts.check_in.research import TO_LEARN_SURVEY_FINISH, TO_LEARN_SURVEY, RESEARCH_DEFAULT_PROMPT
from src.core.prompts.diary import GET_SUMMARY_LOG_FROM_DAILY_LOGS
from src.core.schemas.assistant_response import SummaryResponseSchema
from src.infrastructure.config.config import config
from src.infrastructure.database.models.base import S

logger = logging.getLogger(__name__)


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
            pydantic_model: Type[S],
            temperature: float = 0.3,
            max_tokens: int | NotGiven = NOT_GIVEN
    ) -> S | str:
        try:
            await self.check_balance()

            response = await self.client.chat.completions.create(
                model="deepseek-chat",
                messages=[
                    {"role": "system", "content": f"{prompt}"},
                    {"role": "user", "content": f"{input_query}"}
                ],
                response_format={"type": "json_object"},
                temperature=temperature,
                max_tokens=max_tokens
            )

            logger.info("статистика по токенам:\n")
            logger.info(response.usage)

            try:
                if pydantic_model:
                    return pydantic_model.model_validate_json(response.choices[0].message.content)

                # если нет Pydantic модели —> возвращает строку.
                return response.choices[0].message.content
            except ValidationError as e:
                logger.error(f"Validation error: {e}")
                logger.error(f"Input Query: {input_query}")
                logger.error(f"Raw response: {response.choices[0].message.content}\n\n"
                             f"Model: {pydantic_model}")
                raise ValueError(f"Invalid assistant response: {e}")

        except Exception as ex:
            logger.error(f"Error in get_response: {ex}")
            raise

    # [ GENERATION ]

    async def generate_characteristic(self, characteristic_type: type[S], messages_text: str):
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
            user_characteristics: dict[str, dict[str, Any]] | None = None,
    ) -> PsychoResponse:
        """PSYCHO"""
        profile_text = ""
        if user_characteristics:
            profile_text = "\n\nТекущий профиль пользователя:\n" + \
                           json.dumps(user_characteristics, ensure_ascii=False, indent=2)
            logger.info(profile_text)

        full_prompt: str = CHECK_IN_PSYCHO_PROMPT + profile_text

        return await self.get_response(
            input_query=user_message,
            prompt=full_prompt,
            pydantic_model=PsychoResponse,
            temperature=0.6,  # чуть выше, чтобы был живой стиль
            max_tokens=600,
        )

    async def get_research_default_response(
            self,
            user_message: str,
            user_characteristics: dict[str, dict[str, Any]] | None = None,
    ) -> ResearchDefaultResponse:
        """research: DEFAULT"""
        profile_text = ""
        if user_characteristics:
            profile_text = "\n\nТекущий профиль пользователя:\n" + \
                           json.dumps(user_characteristics, ensure_ascii=False, indent=2)
            logger.info(profile_text)

        full_prompt: str = RESEARCH_DEFAULT_PROMPT + profile_text

        return await self.get_response(
            input_query=user_message,
            prompt=full_prompt,
            pydantic_model=ResearchDefaultResponse,
            temperature=0.6,  # чуть выше, чтобы был живой стиль
            max_tokens=600,
        )

    async def get_research_survey_response(
            self,
            user_message: str
    ) -> ResearchSurveyResponse:
        # TODO: попробовать в дипсик передавать тип личности, чтобы сравнить ответы
        """SURVEY:

        получить пак с ответами
        """
        prompt: str = TO_LEARN_SURVEY

        return await self.get_response(
            input_query=user_message,
            prompt=prompt,
            pydantic_model=ResearchSurveyResponse
        )

    async def get_to_learn_survey_finish_response(
            self,
            request: ResearchSurveyFinishRequest
    ) -> ResearchSurveyFinishResponse:
        """SURVEY:

        Финальная обработка
        """
        prompt: str = TO_LEARN_SURVEY_FINISH

        # TODO: разделить для быстрейшего ответа
        # TODO: records сделать триггер в моделях

        return await self.get_response(
            input_query=request.model_dump_json(),
            prompt=prompt,
            pydantic_model=ResearchSurveyFinishResponse
        )

    # [ SUMMARIZE ]

    async def summarize_user_daily_logs(self, user_logs: str) -> SummaryResponseSchema:
        """создает один рассказ из всех логов"""

        prompt: str = GET_SUMMARY_LOG_FROM_DAILY_LOGS

        pydantic_model: type[S] = SummaryResponseSchema

        return await self.get_response(
            input_query=user_logs,
            pydantic_model=pydantic_model,
            prompt=prompt
        )
