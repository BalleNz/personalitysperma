# TODO: 1) кеш будет сохранятся каждой таблицы отдельно по мере запроса,

from enum import Enum
from typing import Optional

from redis.asyncio import Redis

from config.config import config
from core.schemas.user_schemas import UserSchema


class CacheKeys(str, Enum):
    AUTH = "auth"
    USER_PROFILE = "user_profile"


class RedisService:
    def __init__(self, redis_client: Redis):
        self.redis = redis_client

    # [ KEYS ]
    @staticmethod
    def _get_token_key(telegram_id: str) -> str:
        return f"{CacheKeys.AUTH}:{telegram_id}"

    @staticmethod
    def _get_user_profile_key(telegram_id: str) -> str:
        return f"{CacheKeys.USER_PROFILE}:{telegram_id}"

    # [ GETTERS ]
    async def get_access_token(self, telegram_id: str) -> Optional[str]:
        """Получение access token из кэша"""
        redis_key = self._get_token_key(telegram_id)
        return await self.redis.get(redis_key)

    async def get_user_profile(self, telegram_id: str) -> UserSchema | None:
        """Получение профиля юзера из кэша"""
        redis_key = self._get_token_key(telegram_id)
        return await self.redis.get(redis_key)

    # [ SETTERS ]
    async def set_access_token(
            self,
            telegram_id: str,
            access_token: str,
            expire_seconds: int = config.ACCESS_TOKEN_EXPIRES_MINUTES
    ) -> None:
        """Сохранение access token в кэш"""
        redis_key = self._get_token_key(telegram_id)
        await self.redis.set(redis_key, access_token, ex=expire_seconds)

    async def set_user_profile(
            self,
            telegram_id: str,
            data: UserSchema,
            expire_seconds: int = 86400
    ) -> None:
        """Сохранение информации о профиле юзера"""
        cache_key: str = self._get_user_profile_key(telegram_id)
        await self.redis.set(
            cache_key,
            data.model_dump_json(),
            ex=expire_seconds
        )

    # [ INVALIDATE ]
    async def __invalidate_user_profile(self, telegram_id: str) -> None:
        """Инвалидация кэша профиля пользователя"""
        cache_key = self._get_user_profile_key(telegram_id)
        await self.redis.delete(cache_key)
