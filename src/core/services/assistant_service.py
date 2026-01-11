import logging
from typing import Type

import aiohttp
from openai import AsyncOpenAI, NOT_GIVEN, NotGiven, APIError
from pydantic import ValidationError

from config.config import config
from infrastructure.database.models.base import S

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
                    raise APIError("На балансе DeepseekAPI недостаточно денег!")

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
    ):
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
