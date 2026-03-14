from typing import Type

from sqlalchemy import Float
from sqlalchemy.orm import mapped_column, Mapped

from src.infrastructure.database.models.base import S, IDMixin, TimestampsMixin


class OCD(IDMixin, TimestampsMixin):
    """ОКР и родственные болезни"""

    ocd = mapped_column(Float, default=None, comment="Обсессивно-компульсивное расстройство (0-1)")
    ocd_obsessions = mapped_column(Float, default=None, comment="Навязчивые мысли (0-1)")
    ocd_compulsions = mapped_column(Float, default=None, comment="Компульсивные действия (0-1)")
    ocd_insight = mapped_column(Float, default=None, comment="Ипохондрия (0-1)")
    body_dysmorphia = mapped_column(Float, default=None, comment="Дисморфофобия (0-1)")
    bfrb = mapped_column(Float, default=None, comment="Повторяющееся поведение (0-1)")

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return ...
