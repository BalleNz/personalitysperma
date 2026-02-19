from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field, BaseModel

from src.core.enums.user import TALKING_MODES
from src.core.schemas.clinical_disorders.anxiety_disorders import AnxietyDisordersSchema
from src.core.schemas.clinical_disorders.clinical_profile import ClinicalProfileSchema
from src.core.schemas.clinical_disorders.mood_disorders import MoodDisordersSchema
from src.core.schemas.clinical_disorders.neuro_disorders import NeuroDisordersSchema
from src.core.schemas.clinical_disorders.personality_disorders import PersonalityDisordersSchema
from src.core.schemas.diary_schema import DiarySchema
from src.core.schemas.personality_types.hexaco import UserHexacoSchema
from src.core.schemas.personality_types.holland_codes import UserHollandCodesSchema
from src.core.schemas.personality_types.socionics_type import UserSocionicsSchema
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

    # [ settings ]
    talk_mode: TALKING_MODES = Field(..., description="режим общения")

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
    socionics: Optional[UserSocionicsSchema] = None
    holland_codes: Optional[UserHollandCodesSchema] = None
    hexaco: Optional[UserHexacoSchema] = None

    # [ clinical disorders ]
    clinical_profile: Optional[ClinicalProfileSchema] = None
    mood_disorder: Optional[MoodDisordersSchema] = None
    anxiety_ocd_trauma_disorder: Optional[AnxietyDisordersSchema] = None
    personality_disorder: Optional[PersonalityDisordersSchema] = None
    neurodevelopmental_eating_disorder: Optional[NeuroDisordersSchema] = None

    # [ romance_preferences ]
    # TODO:
    #   love_language: Optional[LoveLanguageSchema] = None
    #   sexual_preference: Optional[SexualPreferenceSchema] = None
    #   relationship_preference: Optional[RelationshipPreferenceSchema] = None
