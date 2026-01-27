import json
import logging
from enum import Enum
from typing import Optional, Sequence, Any

from redis.asyncio import Redis

from src.core.schemas.user_schemas import UserSchema
from src.infrastructure.config.config import config
from src.infrastructure.database.models.base import S

logger = logging.getLogger(__name__)


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

    @staticmethod
    def _get_characteristics_key(telegram_id: str) -> str:
        return f"user:{telegram_id}:characteristics"

    # [ GETTERS ]
    async def get_characteristics(self, telegram_id: str) -> dict[str, dict[str, Any]] | None:
        """
        Получить все характеристики одним словарем: {"SocialProfileSchema": {...}, ... }
        """
        redis_key = self._get_characteristics_key(telegram_id)
        cached_json = await self.redis.get(redis_key)

        if cached_json:
            try:
                return json.loads(cached_json)
            except json.JSONDecodeError:
                logger.warning(f"Повреждённый кэш характеристик: {redis_key}")
                await self.redis.delete(redis_key)
        return None

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

    async def set_all_characteristics(
            self,
            telegram_id: str,
            characteristics: dict[str, dict],
            expire_seconds: int = 86400 * 7  # 7 дней
    ) -> None:
        """
        Сохранить все характеристики одним ключом
        """
        redis_key = self._get_characteristics_key(telegram_id)
        await self.redis.set(
            redis_key,
            json.dumps(characteristics),
            ex=expire_seconds
        )

    # [ INVALIDATE ]
    async def _invalidate_user_profile(self, telegram_id: str) -> None:
        """Инвалидация кэша профиля пользователя"""
        cache_key = self._get_user_profile_key(telegram_id)
        await self.redis.delete(cache_key)

    async def _invalidate_characteristics(self, telegram_id: str) -> None:
        """Инвалидация кэша характеристик"""
        cache_key = self._get_characteristics_key(telegram_id)
        await self.redis.delete(cache_key)
