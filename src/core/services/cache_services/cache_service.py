import datetime
import logging
from typing import Optional

from core.services.cache_services.redis_service import RedisService
from core.schemas.user_schemas import UserSchema, UserTelegramDataSchema

logger = logging.getLogger(__name__)


class CacheService:
    """Сервис для работы с кэшем"""

    def __init__(
            self,
            redis_service: RedisService,
            api_client: ...
    ):
        self.redis_service = redis_service
        self.api_client = api_client

    async def get_or_refresh_access_token(
            self,
            telegram_data: UserTelegramDataSchema
    ) -> str:
        """Получение или обновление access token"""
        cached_token: Optional[str] = await self.redis_service.get_access_token(telegram_data.telegram_id)
        if cached_token:
            return cached_token

        access_token = await self.api_client.telegram_auth(
            telegram_user_data=telegram_data
        )

        await self.redis_service.set_access_token(
            telegram_data.telegram_id,
            access_token
        )

        return access_token

    async def get_user_profile(
            self,
            access_token: str,
            telegram_id: str,
            expiry: int = 86400
    ) -> UserSchema:
        """Получение информации о юзере"""
        cache_data: Optional[UserSchema] = await self.redis_service.get_user_profile(telegram_id)
        if cache_data:
            if cache_data.subscription_end and (
                    not cache_data.subscription_end < datetime.datetime.now() and not cache_data.tokens_last_refresh < datetime.datetime.now()):
                return cache_data

        fresh_data: UserSchema = await self.api_client.get_current_user(access_token)

        await self.redis_service.set_user_profile(
            telegram_id,
            fresh_data,
            expiry
        )

        return fresh_data
