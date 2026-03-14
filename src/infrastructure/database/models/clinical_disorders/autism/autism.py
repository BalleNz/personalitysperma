from typing import Type

from sqlalchemy import Float
from sqlalchemy.orm import mapped_column, Mapped

from src.infrastructure.database.models.base import TimestampsMixin, S, IDMixin


class Autism(IDMixin, TimestampsMixin):
    """Аутизм"""

    autism = mapped_column(Float, default=None, comment="Аутистические черты (0-1)")
    autism_social = mapped_column(Float, default=None, comment="Нарушения социальной коммуникации (0-1)")
    autism_interests = mapped_column(Float, default=None, comment="Ограниченные интересы/ритуалы (0-1)")

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return ...
