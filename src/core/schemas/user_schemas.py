from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field, BaseModel

from src.core.enums.user import GENDER
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
from src.core.schemas.diary_schema import DiarySchema
from src.core.schemas.personality_types.hexaco import HexacoSchema
from src.core.schemas.personality_types.holland_codes import HollandCodesSchema
from src.core.schemas.personality_types.socionics_type import MBTISchema
from src.core.schemas.traits.traits_basic import BehavioralProfileSchema, EmotionalProfileSchema, \
    CognitiveProfileSchema, \
    SocialProfileSchema
from src.core.schemas.traits.traits_dark import DarkTriadsSchema
from src.core.schemas.traits.traits_humor import HumorProfileSchema


class UserTelegramDataSchema(BaseModel):
    telegram_id: str = Field(..., description="Телеграм айди")  # telegram id
    username: str = Field(..., description="Имя пользователя (логин) для идентификации.")
    first_name: Optional[str] = Field(None, description="first name")
    last_name: Optional[str] = Field(None, description="last name")
    auth_date: datetime | None = Field(datetime.now(), description="дата авторизации")

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    id: UUID = Field(...)

    telegram_id: str = Field(..., description="Уникальный идентификатор пользователя в Telegram")
    username: str = Field(..., description="Имя пользователя в Telegram")
    first_name: Optional[str] = Field(None, description="Имя пользователя")
    last_name: Optional[str] = Field(None, description="Фамилия пользователя")
    age: int | None = Field(None, description="приблизительный возраст пользователя")

    real_name: Optional[str] = Field(None, description="Имя пользователя")

    gender: GENDER = Field(..., description="пол")
    passed_typing: bool = Field(..., description="прошел типирование или не")

    # [ charges ]

    used_voice_messages: int = Field(..., description="количество бесплатных голосовых")
    full_access: int | bool = Field(..., description="полный доступ")

    dark_triads_full: bool = Field(..., description="доступ к темной триаде")
    humor_access: bool = Field(..., description="доступ к стилю юмора")
    clinical_access: bool = Field(..., description="доступ к клинике")
    love_access: bool = Field(..., description="доступ к секс портрету")

    created_at: datetime | None = Field(None)
    updated_at: datetime | None = Field(None)

    # [ diary ]
    diary: list[DiarySchema] | None = None

    # [ traits core ]
    social_profile: Optional[SocialProfileSchema] = None
    cognitive_profile: Optional[CognitiveProfileSchema] = None
    emotional_profile: Optional[EmotionalProfileSchema] = None
    behavioral_profile: Optional[BehavioralProfileSchema] = None

    # [ traits dark ]
    dark_triads: Optional[DarkTriadsSchema] = None

    # [ traits humore ]
    humor_profile: Optional[HumorProfileSchema] = None

    # [ personality types ]
    socionics: Optional[MBTISchema] = None
    holland_codes: Optional[HollandCodesSchema] = None
    hexaco: Optional[HexacoSchema] = None

    # [ clinical disorders ]
    bipolar_disorder: Optional[BipolarDisorderSchema] = None
    depression_disorder: Optional[DepressionDisorderSchema] = None
    adhd_disorder: Optional[ADHDSchema] = None
    autism_disorder: Optional[AutismSchema] = None
    dissociative_disorder: Optional[DissociativeSchema] = None
    eating_disorder: Optional[EatingSchema] = None
    looks_disorder: Optional[LooksSchema] = None
    gdr_disorder: Optional[GDRSchema] = None
    panic_disorder: Optional[PanicSchema] = None
    ptsd_disorder: Optional[PTSDSchema] = None
    bpd_disorder: Optional[BPDSchema] = None

    # [ romance_preferences ]
    # TODO:
    #   love_language: Optional[LoveLanguageSchema] = None
    #   sexual_preference: Optional[SexualPreferenceSchema] = None
    #   relationship_preference: Optional[RelationshipPreferenceSchema] = None
