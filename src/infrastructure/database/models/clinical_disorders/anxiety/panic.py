from typing import Type

from sqlalchemy import Float
from sqlalchemy.orm import mapped_column, Mapped

from src.infrastructure.database.models.base import S, IDMixin, TimestampsMixin


class Panic(IDMixin, TimestampsMixin):
    """Панические расстройства"""

    panic = mapped_column(Float, default=None, comment="Паническое расстройство (0-1)")
    panic_frequency = mapped_column(Float, default=None, comment="Частота панических атак")

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return ...
