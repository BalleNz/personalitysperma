from typing import Type

from sqlalchemy import Float
from sqlalchemy.orm import mapped_column, Mapped

from src.infrastructure.database.models.base import S, IDMixin, TimestampsMixin


class Bipolar(IDMixin, TimestampsMixin):
    """Биполярное расстройство"""

    bipolar = mapped_column(Float, default=None, comment="Биполярное расстройство (0-1)")
    cyclothymia = mapped_column(Float, default=None, comment="Циклотимия (0-1)")
    bipolar_mania = mapped_column(Float, default=None, comment="Маниакальные эпизоды (0-1)")
    bipolar_hypomania = mapped_column(Float, default=None, comment="Гипоманиакальные эпизоды (0-1)")
    bipolar_depression = mapped_column(Float, default=None, comment="Депрессивные эпизоды (0-1)")
    bipolar_rapid = mapped_column(Float, default=None, comment="Быстрая смена фаз (0-1)")
    bipolar_psychotic = mapped_column(Float, default=None, comment="Психотические черты (0-1)")

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return ...
