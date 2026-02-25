import logging
from typing import Optional, Any

from src.core.schemas.diary_schema import DiarySchema
from src.api.response_schemas.characteristic import GetAllCharacteristicResponse
from src.core.schemas.personality_types.socionics_type import UserSocionicsSchema
from src.core.schemas.traits.traits_basic import EmotionalProfileSchema, BehavioralProfileSchema, \
    CognitiveProfileSchema, \
    SocialProfileSchema
from src.core.schemas.user_schemas import UserSchema, UserTelegramDataSchema
from src.core.services.api_client.personalityGPT_api import PersonalityGPT_APIClient
from src.core.services.cache_services.redis_service import RedisService
from src.infrastructure.database.models.base import S

logger = logging.getLogger(__name__)

GROUP_REGISTRY: dict[str, list[type[S]]] = {
    "basic": [
        SocialProfileSchema,
        CognitiveProfileSchema,
        EmotionalProfileSchema,
        BehavioralProfileSchema,
    ],
    # ...
}

SCHEMA_REGISTRY = {
    "SocialProfileSchema": SocialProfileSchema,
    "CognitiveProfileSchema": CognitiveProfileSchema,
    "EmotionalProfileSchema": EmotionalProfileSchema,
    "BehavioralProfileSchema": BehavioralProfileSchema,

    "UserSocionicsSchema": UserSocionicsSchema,
}


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
            characteristic_type: str,
            group: str | None = None,
            expiry: int = 86400 * 7
    ) -> S | list[S] | None:
        """
        Получить одну конкретную характеристику.
        Использует get_all_characteristics внутри.
        """
        logger.info(f"Получение профиля типа {characteristic_type} для {telegram_id}")
        all_chars = await self.get_all_characteristics(access_token, telegram_id, expiry)

        if group:
            schemas = GROUP_REGISTRY.get(group, [])
            if not schemas:
                raise ValueError(f"Unknown group: {group}")
            result = []
            for sch_cls in schemas:
                raw = all_chars.get(sch_cls.__name__)
                if raw:
                    result.append(sch_cls.model_validate(raw))
            return result if result else None

        # [ одна характеристика ]
        type_name = (
            characteristic_type.__name__
            if isinstance(characteristic_type, type)
            else characteristic_type
        )
        raw = all_chars.get(type_name)
        if not raw:
            return None

        cls = SCHEMA_REGISTRY.get(type_name)
        if not cls:
            raise ValueError(f"Unknown schema: {type_name}")

        return cls.model_validate(raw)

    async def get_diary(
            self,
            access_token: str,
            telegram_id: str,
            force_refresh: bool = False,
            expiry: int = 86400 * 3,
    ) -> list[DiarySchema] | None:
        if not force_refresh:
            cached = await self.redis_service.get_diary(telegram_id)
            if cached is not None:
                return cached

        try:
            entries = await self.api_client.get_diary(access_token)

            if entries and isinstance(entries[0], dict):
                entries = [DiarySchema.model_validate(e) for e in entries]

            await self.redis_service.set_diary(telegram_id, entries, expiry)
            return entries

        except Exception as e:
            logger.error(f"Ошибка получения дневника {telegram_id}", exc_info=True)
            return None
