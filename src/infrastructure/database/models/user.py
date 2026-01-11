from typing import Type

from sqlalchemy import String, Column, Enum, Float, ForeignKey, UUID, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models.base import IDMixin, TimestampsMixin, S
from core.schemas.user_schemas import UserSchema, CharacteristicHistorySchema


class User(IDMixin, TimestampsMixin):
    __tablename__ = "users"

    telegram_id: Mapped[str] = mapped_column(String, comment="tg id")
    username: Mapped[str] = mapped_column(String, comment="username")
    first_name: Mapped[str | None] = mapped_column(String, comment="first name")
    last_name: Mapped[str | None] = mapped_column(String, comment="last name")

    # [ base info ]
    age: Mapped[int] = mapped_column(Integer, comment="возраст (предугадывает нейронка)")

    # [ MAIN characteristics ]
    social_profile = relationship("SocialProfile", back_populates="user", uselist=False)
    sensory_profile = relationship("SensoryProfile", back_populates="user", uselist=False)
    cognitive_profile = relationship("CognitiveProfile", back_populates="user", uselist=False)
    emotional_profile = relationship("EmotionalProfile", back_populates="user", uselist=False)
    behavioral_profile = relationship("BehavioralProfile", back_populates="user", uselist=False)

    # [ DARK characteristics ]
    dark_triads = relationship("DarkTriad", back_populates="user", uselist=False)

    # [ PERSONALITY ]
    # TODO

    # [ CLINICAL ]
    # TODO
    clinical_profile = relationship("ClinicalProfile", back_populates="user", uselist=False)

    # [ LOVE characteristics ]
    # TODO
    love_language = relationship("LoveLanguage", back_populates="user", uselist=False)
    sexual_preference = relationship("SexualPreference", back_populates="user", uselist=False)

    # [ HUMOR profile ]
    humor_profile = relationship("HumorProfile", back_populates="user", uselist=False)

    @property
    def schema_class(self) -> Type[S]:
        return UserSchema
