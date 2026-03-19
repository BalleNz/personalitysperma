from typing import Type

from sqlalchemy import UUID, ForeignKey, Float
from sqlalchemy.orm import mapped_column, relationship, Mapped

from src.core.schemas.clinical_disorders.personality_disorders.bpd import BPDSchema
from src.infrastructure.database.models.base import TimestampsMixin, S, IDMixin


class BPDDisorder(IDMixin, TimestampsMixin):
    """РАССТРОЙСТВА ЛИЧНОСТИ"""
    __tablename__ = "bpd_disorder"

    user_id = mapped_column(UUID, ForeignKey('users.id', ondelete="CASCADE"), nullable=False, comment="ID пользователя")
    user = relationship("User", back_populates="bpd_disorder")

    # [ ПРЛ ]
    bpd_severity = mapped_column(Float, default=None, comment="Уровень ПРЛ (0-1)")
    bpd_abandonment = mapped_column(Float, default=None, comment="Страх брошенности (0-1)")
    bpd_unstable_relations = mapped_column(Float, default=None, comment="Нестабильные отношения (0-1)")
    bpd_identity = mapped_column(Float, default=None, comment="Нарушение идентичности (0-1)")
    bpd_impulsivity = mapped_column(Float, default=None, comment="Импульсивность (0-1)")
    bpd_mood_swings = mapped_column(Float, default=None, comment="Перепады настроения (0-1)")
    bpd_emptiness = mapped_column(Float, default=None, comment="Чувство пустоты (0-1)")
    bpd_anger = mapped_column(Float, default=None, comment="Неадекватный гнев (0-1)")
    bpd_paranoia = mapped_column(Float, default=None, comment="Параноидные идеи (0-1)")

    bpd_suicidal = mapped_column(Float, default=None, comment="Суицидальное поведение, угрозы, самоповреждения (0-1)")

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return BPDSchema
