from src.api.request_schemas.generation import CheckInRequest
from src.api.response_schemas.characteristic import GetAllCharacteristicResponse
from src.api.response_schemas.generation import CheckInResponse
from src.core.schemas.user_schemas import UserSchema, UserTelegramDataSchema
from src.core.services.api_client.base_http_client import BaseHttpClient, HTTPMethod


class PersonalityGPT_APIClient(BaseHttpClient):
    """Универсальный клиент для DrugSearch API"""
    # [ AUTH ]
    async def telegram_auth(self, telegram_user_data: UserTelegramDataSchema) -> str:
        response: dict = await self._request(
            HTTPMethod.POST,
            "/v1/auth/",
            request_body=telegram_user_data.model_dump()
        )
        return response["token"]

    # [ USER ]
    async def get_current_user(self, access_token: str) -> UserSchema:
        """Получение текущего пользователя"""
        return await self._request(
            HTTPMethod.GET,
            "/v1/user/",
            response_model=UserSchema,
            access_token=access_token
        )

    # [ CHARACTERISTIC ]
    async def check_in(self, access_token: str, request: CheckInRequest) -> CheckInResponse:
        """CHECK IN:
        — Анализ текста юзера
        — Добавление батча / обновление таблиц"""
        return await self._request(
            HTTPMethod.POST,
            request_body=request,
            endpoint="/v1/generation/check_in",
            response_model=CheckInResponse,
            access_token=access_token
        )

    async def get_characteristics(self, access_token: str) -> GetAllCharacteristicResponse:
        """получить все характеристики"""
        response = await self._request(
            HTTPMethod.GET,
            endpoint="/v1/characteristic/",
            access_token=access_token
        )
        return response

    # [ Admin ]

    # [ REFERRALS ]
