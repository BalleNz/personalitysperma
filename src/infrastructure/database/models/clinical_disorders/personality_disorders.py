from typing import Type

from sqlalchemy import UUID, ForeignKey, Float, Integer
from sqlalchemy.orm import mapped_column, relationship, Mapped

from src.core.schemas.clinical_disorders.personality_disorders import PersonalityDisordersSchema
from src.infrastructure.database.models.base import TimestampsMixin, S, IDMixin


class PersonalityDisorders(IDMixin, TimestampsMixin):
    """РАССТРОЙСТВА ЛИЧНОСТИ"""
    __tablename__ = "personality_disorders"

    user_id = mapped_column(UUID, ForeignKey('users.id', ondelete="CASCADE"), nullable=False, comment="ID пользователя")
    user = relationship("User", back_populates="personality_disorders")

    # [ ПРЛ ]
    bpd_severity = mapped_column(Float, default=None, comment="Тяжесть ПРЛ (0-1)")
    bpd_abandonment = mapped_column(Float, default=None, comment="Страх брошенности (0-1)")
    bpd_unstable_relations = mapped_column(Float, default=None, comment="Нестабильные отношения (0-1)")
    bpd_identity = mapped_column(Float, default=None, comment="Нарушение идентичности (0-1)")
    bpd_impulsivity = mapped_column(Float, default=None, comment="Импульсивность (0-1)")
    bpd_suicidal = mapped_column(Float, default=None, comment="Суицидальное поведение (0-1)")
    bpd_mood_swings = mapped_column(Float, default=None, comment="Перепады настроения (0-1)")
    bpd_emptiness = mapped_column(Float, default=None, comment="Чувство пустоты (0-1)")
    bpd_anger = mapped_column(Float, default=None, comment="Неадекватный гнев (0-1)")
    bpd_paranoia = mapped_column(Float, default=None, comment="Параноидные идеи (0-1)")

    # [ Другие РЛ ]
    npd = mapped_column(Float, default=None, comment="Нарциссическое РЛ (0-1)")
    aspd = mapped_column(Float, default=None, comment="Антисоциальное РЛ (0-1)")
    avpd = mapped_column(Float, default=None, comment="Избегающее РЛ (0-1)")
    dpd = mapped_column(Float, default=None, comment="Зависимое РЛ (0-1)")
    ocpd = mapped_column(Float, default=None, comment="Обсессивно-компульсивное РЛ (0-1)")
    ppd = mapped_column(Float, default=None, comment="Параноидное РЛ (0-1)")
    szpd = mapped_column(Float, default=None, comment="Шизоидное РЛ (0-1)")
    stpd = mapped_column(Float, default=None, comment="Шизотипическое РЛ (0-1)")

    records: Mapped[int | None] = mapped_column(
        Integer,
        default=None,
        comment="количество записей"
    )

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return PersonalityDisordersSchema
