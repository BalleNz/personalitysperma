from typing import Type

from sqlalchemy import Float
from sqlalchemy.orm import mapped_column, Mapped

from src.infrastructure.database.models.base import IDMixin, TimestampsMixin, S


class PTSD(IDMixin, TimestampsMixin):
    """ПТСР"""

    ptsd = mapped_column(Float, default=None, comment="Посттравматическое стрессовое расстройство (0-1)")
    cptsd = mapped_column(Float, default=None, comment="Комплексное ПТСР (0-1)")
    ptsd_intrusions = mapped_column(Float, default=None, comment="Интрузивные воспоминания (0-1)")
    ptsd_avoidance = mapped_column(Float, default=None, comment="Избегание триггеров (0-1)")
    ptsd_cognition = mapped_column(Float, default=None, comment="Негативные мысли (0-1)")
    ptsd_arousal = mapped_column(Float, default=None, comment="Гипервозбуждение (0-1)")  # TODO: удалить??
    acute_stress = mapped_column(Float, default=None, comment="Острое стрессовое расстройство (0-1)")
    cptsd_self = mapped_column(Float, default=None, comment="Нарушения самооценки (0-1)")
    cptsd_relations = mapped_column(Float, default=None, comment="Нарушения в отношениях (0-1)")

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return ...
