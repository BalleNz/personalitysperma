import logging
import uuid
from enum import Enum
from typing import Optional, Dict, Any, List, Type, Generic
from datetime import datetime

from sqlalchemy import select, update
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.repository.base_repo import BaseRepository
from infrastructure.database.models.base import M, S
from infrastructure.database.models.basic_profiles.traits_core import (
    CognitiveProfile, EmotionalProfile, BehavioralProfile,
    SocialProfile
)
from infrastructure.database.models.basic_profiles.traits_humor import HumorProfile
from infrastructure.database.models.basic_profiles.traits_dark import DarkTriads
from infrastructure.database.models.clinical_disorders.clinical_profile import ClinicalProfile
from infrastructure.database.models.love_preferences.relationships import LoveLanguage, SexualPreference, RelationshipPreference
from infrastructure.database.models.user import CharacteristicHistory
from core.schemas.traits_core import CognitiveProfileSchema, BehavioralProfileSchema, EmotionalProfileSchema
from core.schemas.traits_dark import DarkTriadsSchema
from core.schemas.traits_humor import HumorProfileSchema

logger = logging.getLogger(__name__)


class CharacteristicModels(Generic[S, M]):
    def get_model_type_from_schema_type(self, schema_type: Type[S]) -> Type[M]:
        return CHARACTERISTIC_SCHEMAS_TO_MODELS[schema_type]


CHARACTERISTIC_MODELS = {
    "SocialProfile": SocialProfile,
    "CognitiveProfile": CognitiveProfile,
    "EmotionalProfile": EmotionalProfile,
    "BehavioralProfile": BehavioralProfile,

    "HumorProfile": HumorProfile,

    "ClinicalProfile": ClinicalProfile,
    "DarkTriads": DarkTriads,

    "RelationshipPreference": RelationshipPreference,
    "LoveLanguage": LoveLanguage,
    "SexualPreference": SexualPreference
}

CHARACTERISTIC_SCHEMAS_TO_MODELS = {
    SocialProfile: SocialProfile,
    CognitiveProfileSchema: CognitiveProfile,
    EmotionalProfileSchema: EmotionalProfile,
    BehavioralProfileSchema: BehavioralProfile,

    HumorProfileSchema: HumorProfile,

    "ClinicalProfileSchema": ClinicalProfile,
    DarkTriadsSchema: DarkTriads,

    "RelationshipPreferenceSchema": RelationshipPreference,
    "LoveLanguageSchema": LoveLanguage,
    "SexualPreferenceSchema": SexualPreference
}


class CharacteristicRepository(BaseRepository):
    """Репозиторий для работы со всеми характеристиками пользователя"""
    def __init__(self, session: AsyncSession):
        super().__init__(model=..., session=session)

    async def get_profile_by_type(self, user_id: uuid.UUID, profile_type: type[S]) -> S:
        """Получение профиля юзера по типу схемы"""
        logger.info(f"Получение профиля типа {profile_type.__name__} для user_id={user_id}")

        try:
            # [ получение типа модели по типу схемы ]
            model_type: type[M] = CHARACTERISTIC_SCHEMAS_TO_MODELS.get(profile_type)
            if not model_type:
                logger.error(f"Не найден маппинг для схемы {profile_type.__name__}")
                raise ValueError(f"Неизвестный тип профиля: {profile_type.__name__}")

            stmt = select(model_type).where(model_type.user_id == user_id)
            result = await self.session.execute(stmt)
            profile_model = result.scalar_one_or_none()

            if not profile_model:
                logger.info(f"Профиль типа {profile_type.__name__} не найден для user_id={user_id}")
                raise ValueError(f"Профиль типа {profile_type.__name__} не найден для user_id={user_id}")

            return profile_model.get_schema()

        except Exception as e:
            logger.error(f"Ошибка при получении профиля {profile_type.__name__} для user_id={user_id}: {e}")
            raise

    # мб удалить?
    async def get_all_profiles(self, user_id: uuid.UUID) -> dict[type[S], S]:
        """
        Получение всех профилей пользователя

        :param user_id: ID пользователя
        :return: Словарь со всеми профилями
        """
        profiles = {}

        for profile_type, model in CHARACTERISTIC_SCHEMAS_TO_MODELS.items():
            profile: S = await self.get_profile_by_type(user_id, profile_type)
            if profile:
                profiles[profile_type] = profile
        return profiles

    async def update_characteristic(
            self,
            user_id: uuid.UUID,
            characteristic: S
    ) -> Optional[Any]:
        """
        Обновление конкретной характеристики
        """
        try:
            schema_type: type[S] = type(characteristic)
            model_type: type[M] = CHARACTERISTIC_SCHEMAS_TO_MODELS.get(schema_type)

            if not model_type:
                logger.error(f"Не найден маппинг для схемы {schema_type.__name__}")
                raise ValueError(f"Неизвестный тип характеристики: {schema_type.__name__}")

            stmt = select(model_type).where(model_type.user_id == user_id)
            result = await self.session.execute(stmt)
            existing_profile = result.scalar_one_or_none()

            if not existing_profile:
                logger.info(f"Профиль не найден, создаем новый для user_id={user_id}")

                # [ новый профиль ]
                new_profile: M = model_type.from_pydantic(characteristic)
                new_profile.user_id = user_id
                self.session.add(new_profile)
                await self.session.commit()
                await self.session.refresh(new_profile)

                return new_profile.get_schema()

            update_data: dict = characteristic.model_dump(exclude_unset=True, exclude_none=True)

            if not update_data:
                logger.info(f"Нет данных для обновления профиля {schema_type.__name__} для user_id={user_id}")
                return existing_profile.get_schema()

            stmt_update = (
                update(model_type)
                .where(model_type.user_id == user_id)
                .values(**update_data)
                .returning(model_type)
            )

            result = await self.session.execute(stmt_update)
            updated_profile = result.scalar_one()
            await self.session.commit()
            await self.session.refresh(updated_profile)

            logger.info(f"Характеристики успешно обновлены для user_id={user_id}")
            return updated_profile.get_schema()

        except Exception as e:
            await self.session.rollback()
            logger.error(f"Ошибка при обновлении характеристики для user_id={user_id}: {e}")
            raise
