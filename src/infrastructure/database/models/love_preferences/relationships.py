from typing import Type

from sqlalchemy import Column, Float, ForeignKey, UUID, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models.base import IDMixin, S


class RelationshipPreference(IDMixin):
    __tablename__ = "ralationships_pre"
    user_id: ...

    ...

    # attachment_style (secure, anxious, avoidant) - КРИТИЧНО для отношений

    @property
    def schema_class(self) -> Type[S]:
        return ...


class LoveLanguage(IDMixin):
    """Язык любви"""
    ...

    user_id: ...

    words_of_affirmation: Mapped[float] = Column(Float, default=0.2)
    acts_of_service: Mapped[float] = Column(Float, default=0.2)
    receiving_gifts: Mapped[float] = Column(Float, default=0.2)
    quality_time: Mapped[float] = Column(Float, default=0.2)
    sensuality: Mapped[float | None] = Column(Float, default=None, comment="Внимание к физическим ощущениям и близости")

    @property
    def schema_class(self) -> Type[S]:
        return ...


class SexualPreference(IDMixin):
    """18+ Описание сексуальных предпочтений"""
    __tablename__ = "sexual_preferences"

    ...

    gender: Mapped[str] = mapped_column(Enum(...))  # TODO: Enum
    orientation: Mapped[str] = mapped_column(Enum(...))

    # TODO: подумать об объединении с UserLoveLanguage

    # TODO: Sexual предпочтения таблица, libido value
    # sex_drive_type: Mapped[... | None] = Column(Enum(SexDriveTypeEnum))

    user_id = mapped_column(UUID, ForeignKey('users.id'), nullable=False, unique=True)
    user = relationship("User", back_populates="sexual_preference")

    libido: Mapped[float] = Column(Float, default=0.5)  # 0-1
    adventurousness: Mapped[float] = Column(Float, default=0.5)  # консервативный → экспериментальный
    emotional_intimacy_need: Mapped[float] = Column(Float, default=0.5)  # физическое → эмоциональное
    dominance: Mapped[float] = Column(Float, default=0.5)  # подчинение → доминирование

    # Добавить enum для kinks/preferences если нужно

    @property
    def schema_class(self) -> Type[S]:
        return ...
