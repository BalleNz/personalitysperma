from typing import Type

from sqlalchemy import UUID, ForeignKey, Float
from sqlalchemy.orm import mapped_column, relationship, Mapped

from src.core.schemas.clinical_disorders.neuro_disorders.adhd import ADHDSchema
from src.infrastructure.database.models.base import TimestampsMixin, S, IDMixin


class ADHDDisorder(IDMixin, TimestampsMixin):
    """СДВГ"""
    __tablename__ = "adhd_disorder"

    user_id = mapped_column(UUID, ForeignKey('users.id', ondelete="CASCADE"), nullable=False, comment="ID пользователя")
    user = relationship("User", back_populates="adhd_disorder")

    adhd = mapped_column(Float, default=None, comment="уровень СДВГ (0-1)")
    adhd_inattention = mapped_column(Float, default=None, comment="Невнимательность (0-1)")
    adhd_hyperactivity = mapped_column(Float, default=None, comment="Гиперактивность (0-1)")

    hyperfocus = mapped_column(Float, default=None, comment="Склонность к гиперфокусу (осознанная защитная реакция) (0-1)")
    internal_hyperactivity = mapped_column(Float, default=None, comment="Внутренняя гиперактивность / постоянный внутренний шум (0-1)")
    time_blindness = mapped_column(Float, default=None, comment="Нарушение чувства времени / тайм-слепота (0-1)")
    motivation_problems = mapped_column(Float, default=None, comment="Проблемы с внутренней мотивацией / прокрастинация при отсутствии дофаминового 'пинка' (0-1)")

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return ADHDSchema
