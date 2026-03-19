from typing import Type

from sqlalchemy import Float, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.schemas.clinical_disorders.anxiety.ptsd import PTSDSchema
from src.infrastructure.database.models.base import TimestampsMixin, IDMixin, S


class PTSDDisorder(IDMixin, TimestampsMixin):
    """ПТСР"""
    __tablename__ = "ptsd_disorder"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user = relationship("User", back_populates="ptsd_disorder")

    ptsd = mapped_column(Float, default=None, comment="Общий уровень ПТСР / комплексного ПТСР (0-1)")
    ptsd_intrusions = mapped_column(Float, default=None, comment="Интрузивные воспоминания, флэшбэки (0-1)")
    ptsd_cognition = mapped_column(Float, default=None, comment="Негативные изменения в мышлении и настроении (0-1)")
    ptsd_arousal = mapped_column(Float, default=None, comment="Гипервозбуждение при триггере (0-1)")

    ptsd_self = mapped_column(Float, default=None, comment="Нарушения самооценки, чувство никчёмности (0-1)")
    ptsd_avoidance = mapped_column(Float, default=None, comment="Избегание триггеров, мыслей, мест (0-1)")
    ptsd_relations = mapped_column(Float, default=None, comment="Нарушения в отношениях, недоверие (0-1)")

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return PTSDSchema
