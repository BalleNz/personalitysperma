from typing import Type

from sqlalchemy import Float
from sqlalchemy.orm import mapped_column, Mapped

from src.infrastructure.database.models.base import TimestampsMixin, S, IDMixin


class ADHD(IDMixin, TimestampsMixin):
    """СДВГ"""

    adhd = mapped_column(Float, default=None, comment="вероятность СДВГ (0-1)")
    adhd_inattention = mapped_column(Float, default=None, comment="Невнимательность (0-1)")
    adhd_hyperactivity = mapped_column(Float, default=None, comment="Гиперактивность (0-1)")
    adhd_impulsivity = mapped_column(Float, default=None, comment="Импульсивность (0-1)")

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return ...