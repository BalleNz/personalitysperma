from typing import Type

from sqlalchemy import Float, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.schemas.clinical_disorders.anxiety.panic import PanicSchema
from src.infrastructure.database.models.base import TimestampsMixin, IDMixin, S


class PanicDisorder(IDMixin, TimestampsMixin):
    """Панические расстройства"""
    __tablename__ = "panic_disorder"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user = relationship("User", back_populates="panic_disorder")

    panic_general = mapped_column(Float, default=None, comment="Общий уровень панического расстройства (0-1)")
    attack_frequency = mapped_column(Float, default=None, comment="Частота полноценных панических атак (0-1)")

    anticipatory = mapped_column(Float, default=None, comment="Тревога ожидания новой атаки (0-1)")
    fear_catastrophe = mapped_column(Float, default=None, comment="Страх смерти / сумасшествия / потери контроля (0-1)")

    situational_avoid = mapped_column(Float, default=None, comment="Избегание ситуаций / мест (0-1)")
    interoceptive_avoid = mapped_column(Float, default=None, comment="Избегание телесных ощущений / триггеров (0-1)")
    life_impairment = mapped_column(Float, default=None, comment="Нарушение жизни / функционирования из-за панического расстройства (0-1)")  # как сильно сказывается

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return PanicSchema
