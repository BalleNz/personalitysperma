from typing import Type

from sqlalchemy import String, Column, Enum, Float, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models.base import IDMixin, TimestampsMixin, S


class User(IDMixin, TimestampsMixin):
    __tablename__ = "users"

    telegram_id: Mapped[str] = mapped_column(String, comment="tg id")
    username: Mapped[str] = mapped_column(String, comment="username")
    first_name: Mapped[str | None] = mapped_column(String, comment="first name")
    last_name: Mapped[str | None] = mapped_column(String, comment="last name")

    # [ base info ]
    gender: Mapped[str] = mapped_column(Enum(...), nullable=False)  # TODO: Enum
    orientation: Mapped[str] = mapped_column(Enum(...), nullable=False)
    # TODO: age

    # [ MAIN characteristics ]
    social_profile = relationship("SocialProfile", back_populates="user", uselist=False)
    sensory_profile = relationship("SensoryProfile", back_populates="user", uselist=False)
    cognitive_profile = relationship("CognitiveProfile", back_populates="user", uselist=False)
    emotional_profile = relationship("EmotionalProfile", back_populates="user", uselist=False)
    behavioral_profile = relationship("BehavioralProfile", back_populates="user", uselist=False)

    # [ DARK characteristics ]
    dark_triads = relationship("DarkTriad", back_populates="user", uselist=False)
    clinical_profile = relationship("ClinicalProfile", back_populates="user", uselist=False)

    # [ ROMANCE characteristics ]
    love_language = relationship("LoveLanguage", back_populates="user", uselist=False)
    sexual_preference = relationship("SexualPreference", back_populates="user", uselist=False)

    # [ HUMOR profile ]
    humor_profile = relationship("HumorProfile", back_populates="user", uselist=False)

    @property
    def schema_class(self) -> Type[S]:
        return ...

# TODO: 3 personal tables. personality_type: Mapped[str | None] = Column(Enum(PersonalityTypeEnum))


class CharacteristicHistory(IDMixin, TimestampsMixin):
    """История изменений полей"""
    __tablename__ = "characteristic_history"

    user_id = mapped_column(UUID, ForeignKey('users.id'))

    profile_type: Mapped[str] = Column(String)  # 'cognitive', 'emotional', etc.
    characteristic_name: Mapped[str] = Column(String)
    old_value: Mapped[float] = Column(Float)
    new_value: Mapped[float] = Column(Float)
    source: Mapped[str] = Column(String)  # 'voice_message', 'test', 'manual'

    @property
    def schema_class(self) -> Type[S]:
        return ...
