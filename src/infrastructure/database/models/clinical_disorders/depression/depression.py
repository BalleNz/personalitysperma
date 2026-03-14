from typing import Type

from sqlalchemy import Float
from sqlalchemy.orm import mapped_column, Mapped

from src.infrastructure.database.models.base import S, IDMixin, TimestampsMixin


class Depression(IDMixin, TimestampsMixin):
    """Депрессия"""

    depression = mapped_column(Float, default=None, comment="Уровень депрессии (0-1)")
    suicide_risk = mapped_column(Float, default=None, comment="Уровень суицидального риска (0-1)")
    depression_sadness = mapped_column(Float, default=None, comment="Грусть (0-1)")
    depression_anhedonia = mapped_column(Float, default=None, comment="Ангедония (0-1)")
    depression_appetite = mapped_column(Float, default=None, comment="Нарушение аппетита (0-1)")
    depression_worthlessness = mapped_column(Float, default=None, comment="Чувство никчемности (0-1)")
    depression_suicidal = mapped_column(Float, default=None, comment="Суицидальные мысли (0-1)")

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return ...
