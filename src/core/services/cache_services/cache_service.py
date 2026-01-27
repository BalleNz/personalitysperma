import datetime
import logging
from typing import Optional, Any

from src.api.response_schemas.characteristic import GetAllCharacteristicResponse
from src.core.schemas.user_schemas import UserSchema, UserTelegramDataSchema
from src.core.services.api_client.personalityGPT_api import PersonalityGPT_APIClient
from src.core.services.cache_services.redis_service import RedisService
from src.infrastructure.database.models.base import S

logger = logging.getLogger(__name__)


class CacheService:
    """Сервис для работы с кэшем"""

    def __init__(
            self,
            redis_service: RedisService,
            api_client: PersonalityGPT_APIClient
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

    async def get_all_characteristics(
            self,
            access_token: str,
            telegram_id: str,
            expiry: int = 86400 * 7  # 7 дней
    ) -> dict[str, dict[str, Any]]:
        """
        Получить все характеристики
        запрашивает из API и сохраняет
        """
        cached_all = await self.redis_service.get_characteristics(telegram_id)

        if cached_all is not None:
            return cached_all

        try:
            response_obj: GetAllCharacteristicResponse = await self.api_client.get_characteristics(access_token)
            all_raw = response_obj["response"]
        except Exception as e:
            logger.error(f"Ошибка получения всех характеристик для {telegram_id}: {e}")
            return {}

        characteristics_dict: dict[str, dict[str, Any]] = {}

        for item in all_raw:
            type_name = item["type"]
            characteristic_obj = item["characteristic"]

            characteristics_dict[type_name] = characteristic_obj

        await self.redis_service.set_all_characteristics(
            telegram_id=telegram_id,
            characteristics=characteristics_dict,
            expire_seconds=expiry
        )

        return characteristics_dict

    async def get_characteristic(
            self,
            access_token: str,
            telegram_id: str,
            characteristic_type: type[S],
            expiry: int = 86400 * 7
    ) -> type[S] | None:
        """
        Получить одну конкретную характеристику.
        Использует get_all_characteristics внутри.
        """
        logger.info(f"Получение профиля типа {characteristic_type.__name__} для {telegram_id}")
        all_chars = await self.get_all_characteristics(
            access_token=access_token,
            telegram_id=telegram_id,
            expiry=expiry
        )

        type_name = characteristic_type.__name__
        if type_name in all_chars:
            try:
                return characteristic_type.model_validate(all_chars[type_name])
            except Exception as e:
                logger.error(f"Ошибка валидации характеристики {type_name} для {telegram_id}: {e}")
                return None

        return None
