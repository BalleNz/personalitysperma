from typing import Type

from sqlalchemy import Float
from sqlalchemy.orm import mapped_column, Mapped

from src.infrastructure.database.models.base import S, IDMixin, TimestampsMixin


class Dissociative(IDMixin, TimestampsMixin):
    """Диссоциативные расстройства"""

    depersonalization = mapped_column(Float, default=None, comment="Деперсонализация/дереализация (0-1)")  # TODO: возможно разделить, если есть рзница
    dissociative = mapped_column(Float, default=None, comment="Диссоциативные симптомы (0-1)")
    amnesia = mapped_column(Float, default=None, comment="Амнезия (0-1)")
    did = mapped_column(Float, default=None, comment="Диссоциативное расстройство идентичности (0-1)")

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return ...