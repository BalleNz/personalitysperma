import logging
import uuid
from typing import Type, Generic, Sequence, Any

from sqlalchemy import select, delete
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.schemas.clinical_disorders.anxiety_disorders import AnxietyDisordersSchema
from src.core.schemas.clinical_disorders.clinical_profile import ClinicalProfileSchema
from src.core.schemas.clinical_disorders.mood_disorders import MoodDisordersSchema
from src.core.schemas.clinical_disorders.neuro_disorders import NeuroDisordersSchema
from src.core.schemas.clinical_disorders.personality_disorders import PersonalityDisordersSchema
from src.core.schemas.personality_types.hexaco import UserHexacoSchema
from src.core.schemas.personality_types.holland_codes import UserHollandCodesSchema
from src.core.schemas.personality_types.socionics_type import UserSocionicsSchema
from src.core.schemas.traits.traits_core import CognitiveProfileSchema, EmotionalProfileSchema, BehavioralProfileSchema, \
    SocialProfileSchema
from src.core.schemas.traits.traits_dark import DarkTriadsSchema
from src.core.schemas.traits.traits_humor import HumorProfileSchema
from src.core.services.cache_services.cache_service import CacheService
from src.infrastructure.database.models.base import M, S
from src.infrastructure.database.models.basic_profiles.traits_core import (
    CognitiveProfile, EmotionalProfile, BehavioralProfile,
    SocialProfile
)
from src.infrastructure.database.models.basic_profiles.traits_dark import DarkTriads
from src.infrastructure.database.models.basic_profiles.traits_humor import HumorProfile
from src.infrastructure.database.models.clinical_disorders.anxiety_disorders import AnxietyDisorders
from src.infrastructure.database.models.clinical_disorders.clinical_profile import ClinicalProfile
from src.infrastructure.database.models.clinical_disorders.mood_disorders import MoodDisorders
from src.infrastructure.database.models.clinical_disorders.neuro_disorders import NeuroDisorders
from src.infrastructure.database.models.clinical_disorders.personality_disorders import PersonalityDisorders
from src.infrastructure.database.models.logs import CharacteristicBatchLog
from src.infrastructure.database.models.personality_types.hexaco import UserHexaco
from src.infrastructure.database.models.personality_types.holland_codes import UserHollandCodes
from src.infrastructure.database.models.personality_types.socionics import UserSocionics

# from src.infrastructure.database.models.love_preferences.relationships import LoveLanguage, SexualPreference, \
#    RelationshipPreference

logger = logging.getLogger(__name__)


class CharacteristicFormat(Generic[S, M]):
    def get_model_type_from_schema_type(self, schema_type: Type[S]) -> Type[M]:
        return CHARACTERISTIC_SCHEMAS_TO_MODELS[schema_type]

    @staticmethod
    def get_schema_type_from_schema_name(schema_name: str) -> type[S] | None:
        for schema in CHARACTERISTIC_SCHEMAS_TO_MODELS.keys():
            if schema_name == schema.__name__:
                return schema
        return None


CHARACTERISTIC_SCHEMAS_TO_MODELS = {
    SocialProfileSchema: SocialProfile,
    CognitiveProfileSchema: CognitiveProfile,
    EmotionalProfileSchema: EmotionalProfile,
    BehavioralProfileSchema: BehavioralProfile,

    DarkTriadsSchema: DarkTriads,

    HumorProfileSchema: HumorProfile,

    ClinicalProfileSchema: ClinicalProfile,
    MoodDisordersSchema: MoodDisorders,
    AnxietyDisordersSchema: AnxietyDisorders,
    NeuroDisordersSchema: NeuroDisorders,
    PersonalityDisordersSchema: PersonalityDisorders,

    UserHexacoSchema: UserHexaco,
    UserHollandCodesSchema: UserHollandCodes,
    UserSocionicsSchema: UserSocionics,

    # "RelationshipPreferenceSchema": RelationshipPreference,
    # "LoveLanguageSchema": LoveLanguage,
    # "SexualPreferenceSchema": SexualPreference
}


def get_schema_type_from_name(schema_name: str) -> type[S] | None:
    for schema in CHARACTERISTIC_SCHEMAS_TO_MODELS.keys():
        if schema_name == schema.__name__:
            return schema


class CharacteristicRepository:
    """Репозиторий для работы со всеми характеристиками пользователя"""

    def __init__(self, session: AsyncSession, cache_service: CacheService):
        self.session = session
        self.cache_service = cache_service

    async def get_all_characteristics(
            self,
            user_id: uuid.UUID
    ) -> list[dict]:
        """
        Получить все характеристики пользователя.
        Возвращает список схем разных типов.
        """
        characteristics: list[dict[str, dict[str, Any]]] = []

        # Список пар (модель, схема)
        model_schema_pairs = [
            (SocialProfile, SocialProfileSchema),
            (CognitiveProfile, CognitiveProfileSchema),
            (EmotionalProfile, EmotionalProfileSchema),
            (BehavioralProfile, BehavioralProfileSchema),
            (DarkTriads, DarkTriadsSchema),
            (HumorProfile, HumorProfileSchema),
            (ClinicalProfile, ClinicalProfileSchema),
            (MoodDisorders, MoodDisordersSchema),
            (AnxietyDisorders, AnxietyDisordersSchema),
            (NeuroDisorders, NeuroDisordersSchema),
            (PersonalityDisorders, PersonalityDisordersSchema),
            (UserHexaco, UserHexacoSchema),
            (UserHollandCodes, UserHollandCodesSchema),
            (UserSocionics, UserSocionicsSchema),
        ]

        for model_cls, schema_cls in model_schema_pairs:
            stmt = select(model_cls).where(model_cls.user_id == user_id)
            result = await self.session.execute(stmt)
            instance = result.scalar_one_or_none()

            if instance:
                schema: S = schema_cls.model_validate(instance)
                characteristics.append(
                    {
                        "type": schema_cls.__name__,
                        "characteristic": schema
                    }
                )

        return characteristics

    async def append_characteristic(
            self,
            user_id: uuid.UUID,
            characteristic: S,
            telegram_id: str
    ) -> None:
        """
        Добавление новой характеристики юзера
        """
        char_data = characteristic.model_dump(exclude={"created_at", "updated_at"})  # даты на стороне БД
        char_data["user_id"] = user_id

        model_class: type[M] = CHARACTERISTIC_SCHEMAS_TO_MODELS.get(type(characteristic))

        stmt = (
            insert(model_class)
            .values(char_data)
            .returning(None)
        )

        await self.session.execute(stmt)
        await self.session.commit()

        await self.cache_service.redis_service._invalidate_characteristics(telegram_id)

    async def create_log_in_batch(
            self,
            user_id: uuid.UUID,
            characteristic_type: type[M],
            message: str
    ) -> None:
        """Создает лог в таблице батчей"""
        batch_log = CharacteristicBatchLog(
            user_id=user_id,
            characteristic_type=characteristic_type.__name__,
            message=message
        )

        self.session.add(batch_log)
        await self.session.commit()
        await self.session.refresh(batch_log)

    async def get_batch_logs(
            self,
            user_id: uuid.UUID,
            characteristic_type: type[M]
    ) -> Sequence[S]:
        """Все батчи конкретной характеристики юзера"""
        characteristic_type_name = characteristic_type.__name__  # просто название модели в строчном виде

        stmt = select(CharacteristicBatchLog).where(
            CharacteristicBatchLog.user_id == user_id,
            CharacteristicBatchLog.characteristic_type == characteristic_type_name
        ).order_by(CharacteristicBatchLog.created_at.asc())

        result = await self.session.execute(stmt)
        return [model.get_schema() for model in result.scalars().all()]

    async def delete_batch_logs(
            self,
            user_id: uuid.UUID,
            characteristic_type: type[M]
    ):
        """Удаляет все батчи конкретной характеристики у юзера"""
        characteristic_type_name = characteristic_type.__name__

        stmt = delete(CharacteristicBatchLog).where(
            CharacteristicBatchLog.user_id == user_id,
            CharacteristicBatchLog.characteristic_type == characteristic_type_name
        )

        await self.session.execute(stmt)
        await self.session.commit()
