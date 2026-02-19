from schemas.diary_schema import DiarySchema
from src.api.request_schemas.generation import CheckInRequest
from src.api.response_schemas.characteristic import GetAllCharacteristicResponse
from src.api.response_schemas.generation import CheckInResponse
from src.core.schemas.user_schemas import UserSchema, UserTelegramDataSchema
from src.core.services.api_client.base_http_client import BaseHttpClient, HTTPMethod


class PersonalityGPT_APIClient(BaseHttpClient):
    """Универсальный клиент для DrugSearch API"""

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

    async def increase_used_voices(self, access_token: str) -> None:
        """Отнимает 1 голосовой запрос + invalidate cache"""
        return await self._request(
            HTTPMethod.PUT,
            endpoint="/v1/user/increase_used_voices",
            access_token=access_token
        )

    # [ DIARY ]
    async def get_diary(self, access_token: str) -> list[DiarySchema]:
        return await self._request(
            HTTPMethod.GET,
            endpoint="/v1/user/diary",
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

    # [ SETTINGS ]
    async def change_talk_mode(self, access_token: str) -> None:
        """меняет режим общения"""
        await self._request(
            HTTPMethod.PUT,
            endpoint="/v1/user/change_talking_mode",
            access_token=access_token
        )
