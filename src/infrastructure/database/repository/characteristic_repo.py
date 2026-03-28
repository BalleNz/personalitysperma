import logging
import uuid
from typing import Type, Generic, Sequence, Any

from sqlalchemy import select, delete, desc, func
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession

from src.api.response_schemas.characteristic import CharacteristicResponseRaw
from src.core.schemas.clinical_disorders.anxiety.gdr import GDRSchema
from src.core.schemas.clinical_disorders.anxiety.panic import PanicSchema
from src.core.schemas.clinical_disorders.anxiety.ptsd import PTSDSchema
from src.core.schemas.clinical_disorders.mood_disorders.bipolar import BipolarDisorderSchema
from src.core.schemas.clinical_disorders.mood_disorders.depression import DepressionDisorderSchema
from src.core.schemas.clinical_disorders.neuro_disorders.adhd import ADHDSchema
from src.core.schemas.clinical_disorders.neuro_disorders.autism import AutismSchema
from src.core.schemas.clinical_disorders.neuro_disorders.dissociative import DissociativeSchema
from src.core.schemas.clinical_disorders.neuro_disorders.eating import EatingSchema
from src.core.schemas.clinical_disorders.neuro_disorders.looks_disorder import LooksSchema
from src.core.schemas.clinical_disorders.personality_disorders.bpd import BPDSchema
from src.core.schemas.personality_types.hexaco import HexacoSchema
from src.core.schemas.personality_types.holland_codes import HollandCodesSchema
from src.core.schemas.personality_types.socionics_type import MBTISchema
from src.core.schemas.traits.traits_basic import CognitiveProfileSchema, EmotionalProfileSchema, \
    BehavioralProfileSchema, \
    SocialProfileSchema
from src.core.schemas.traits.traits_dark import DarkTriadsSchema
from src.core.schemas.traits.traits_humor import HumorProfileSchema
from src.core.services.cache_services.cache_service import CacheService
from src.infrastructure.database.models.base import M, S
from src.infrastructure.database.models.basic_profiles.traits_basic import (
    CognitiveProfile, EmotionalProfile, BehavioralProfile,
    SocialProfile
)
from src.infrastructure.database.models.basic_profiles.traits_dark import DarkTriads
from src.infrastructure.database.models.basic_profiles.traits_humor import HumorProfile
from src.infrastructure.database.models.clinical_disorders.anxiety.gdr import GDRDisorder
from src.infrastructure.database.models.clinical_disorders.anxiety.panic import PanicDisorder
from src.infrastructure.database.models.clinical_disorders.anxiety.ptsd import PTSDDisorder
from src.infrastructure.database.models.clinical_disorders.mood_disorders.bipolar import BipolarDisorder
from src.infrastructure.database.models.clinical_disorders.mood_disorders.depression import DepressionDisorder
from src.infrastructure.database.models.clinical_disorders.neuro_disorders.adhd import ADHDDisorder
from src.infrastructure.database.models.clinical_disorders.neuro_disorders.autism import AutismDisorder
from src.infrastructure.database.models.clinical_disorders.neuro_disorders.dissociative import DissociativeDisorder
from src.infrastructure.database.models.clinical_disorders.neuro_disorders.eating_disorders import EatingDisorder
from src.infrastructure.database.models.clinical_disorders.neuro_disorders.looks_disorder import LooksDisorder
from src.infrastructure.database.models.clinical_disorders.personality_disorders.bpd import BPDDisorder
from src.infrastructure.database.models.logs import CharacteristicBatchLog
from src.infrastructure.database.models.personality_types.hexaco import UserHexaco
from src.infrastructure.database.models.personality_types.holland_codes import UserHollandCodes
from src.infrastructure.database.models.personality_types.socionics import UserSocionics
from src.infrastructure.database.models.records import UserRecords

# from src.infrastructure.database.models.love_preferences.relationships import LoveLanguage, SexualPreference, \
#    RelationshipPreference

logger = logging.getLogger(__name__)


class CharacteristicFormat(Generic[S, M]):
    def get_model_type_from_schema_type(self, schema_type: Type[S]) -> Type[M]:
        return CHARACTERISTIC_SCHEMAS_TO_MODELS[schema_type]

    @staticmethod
    def get_cls_from_schema_name(schema_name: str) -> type[S] | None:
        for cls in CHARACTERISTIC_SCHEMAS_TO_MODELS.keys():
            if schema_name == cls.__name__:
                return cls
        return None


CHARACTERISTIC_SCHEMAS_TO_MODELS = {
    # [ traits core ]
    SocialProfileSchema: SocialProfile,
    CognitiveProfileSchema: CognitiveProfile,
    EmotionalProfileSchema: EmotionalProfile,
    BehavioralProfileSchema: BehavioralProfile,

    DarkTriadsSchema: DarkTriads,

    HumorProfileSchema: HumorProfile,

    BipolarDisorderSchema: BipolarDisorder,
    DepressionDisorderSchema: DepressionDisorder,
    ADHDSchema: ADHDDisorder,
    AutismSchema: AutismDisorder,
    DissociativeSchema: DissociativeDisorder,
    EatingSchema: EatingDisorder,
    LooksSchema: LooksDisorder,
    GDRSchema: GDRDisorder,
    PanicSchema: PanicDisorder,
    PTSDSchema: PTSDDisorder,
    BPDSchema: BPDDisorder,

    HexacoSchema: UserHexaco,
    HollandCodesSchema: UserHollandCodes,
    MBTISchema: UserSocionics,

    # "RelationshipPreferenceSchema": RelationshipPreference,
    # "LoveLanguageSchema": LoveLanguage,
    # "SexualPreferenceSchema": SexualPreference
}

PERSONALITY_SCHEMAS = (
    HexacoSchema,
    HollandCodesSchema,
    MBTISchema
)

# LOVE_SCHEMAS = (
#     RelationshipPreferenceSchema,
#     LoveLanguageSchema,
#     SexualPreferenceSchema
# )

SCHEMA_SHORT_NAMES = {
    "SocialProfileSchema":      "soc",
    "CognitiveProfileSchema":   "cog",
    "EmotionalProfileSchema":   "emo",
    "BehavioralProfileSchema":  "beh",

    "DarkTriadsSchema":         "dark",
    "HumorProfileSchema":       "hum",

    "BipolarDisorderSchema":    "bip",
    "DepressionSchema":         "dep",
    "ADHDSchema":               "adhd",
    "AutismSchema":             "aut",
    "DissociativeSchema":       "dis",
    "EatingSchema":             "eat",
    "LooksSchema":              "look",
    "GDRSchema":                "gad",
    "PanicSchema":              "pan",
    "PTSDSchema":               "pts",
    "BPDSchema":                "bpd",

    "HexacoSchema":         "hex",
    "HollandCodesSchema":   "hol",
    "MBTISchema":      "socion",

    "ChangeName": "name"
    # добавляй новые по мере появления
}
SHORT_TO_FULL_SCHEMA = {v: k for k, v in SCHEMA_SHORT_NAMES.items()}


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
    ) -> list[CharacteristicResponseRaw]:
        """
        Получить все характеристики пользователя.
        Возвращает список из CharacteristicRaw схем разных типов.

        CharacteristicRaw содержит две схемы (самую свежую и самую свежую любого другого дня)
        """

        # Список пар (модель, схема)
        model_schema_pairs: list[tuple[M, S]] = [
            (m, s) for s, m in CHARACTERISTIC_SCHEMAS_TO_MODELS.items()
        ]

        profile_models = [m for m, s in model_schema_pairs]
        profile_names = {m.__tablename__ for m, s in model_schema_pairs}

        if profile_models:
            count_subquery = (
                select(
                    UserRecords.user_id,
                    UserRecords.profile_name,
                    func.count(UserRecords.id).label("record_count")
                )
                .where(
                    UserRecords.user_id == user_id,
                    UserRecords.profile_name.in_(profile_names)
                )
                .group_by(UserRecords.user_id, UserRecords.profile_name)
                .subquery()
            )

            counts_result = await self.session.execute(
                select(count_subquery.c.profile_name, count_subquery.c.record_count)
            )
            records_map = dict(counts_result.all())  # {"social": 42, "emotional": 15, ...}
        else:
            records_map = {}

        # [ получаем каждую модель в правильно порядке для CharacteristicRaw ]
        response: list[CharacteristicResponseRaw] = []
        for model_cls, schema_cls in model_schema_pairs:
            stmt = (
                select(model_cls)
                .where(model_cls.user_id == user_id)
                .order_by(desc(model_cls.created_at))
                .limit(20)
            )

            result = await self.session.execute(stmt)
            instances: list[Any] | Any = result.scalars().all()

            if not instances:
                instances = []
            else:
                latest = instances[0]

                latest_date = latest.created_at.date()
                second = None

                for inst in instances[1:]:
                    if inst.created_at.date() != latest_date:
                        second = inst
                        break

                instances = [latest]
                if second:
                    instances.append(second)

            if instances:
                raw = CharacteristicResponseRaw(
                    type=schema_cls.__name__,
                    characteristics=[schema_cls.model_validate(instance, from_attributes=True) for instance in instances]
                )
                # [ добавление records ]
                if model_cls.__tablename__ in records_map:
                    raw.characteristics[0].records = records_map[model_cls.__tablename__]
                else:
                    raw.characteristics[0].records = 0
                response += [raw]
        return response

    async def append_characteristic(
            self,
            user_id: uuid.UUID,
            characteristic: S,
            telegram_id: str
    ) -> None:
        """
        Добавление новой характеристики юзера
        """
        char_data = characteristic.model_dump(exclude={"created_at", "updated_at", "GROUP", "records"})  # даты на стороне БД
        char_data["user_id"] = user_id

        model_class: type[M] = CHARACTERISTIC_SCHEMAS_TO_MODELS.get(type(characteristic))

        stmt = (
            insert(model_class)
            .values(char_data)
            .returning(None)
        )
        await self.session.execute(stmt)

        # [ добавление UserRecords ]
        record_stmt = insert(UserRecords).values(
            user_id=str(user_id),
            profile_name=model_class.__tablename__,
        )
        await self.session.execute(record_stmt)
        await self.session.commit()

        await self.cache_service.redis_service.invalidate_characteristics(telegram_id)

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
