from typing import Optional, Type

from sqlalchemy import Float, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.schemas.clinical_disorders.anxiety.gdr import GDRSchema
from src.infrastructure.database.models.base import TimestampsMixin, IDMixin, S


class GDRDisorder(IDMixin, TimestampsMixin):
    """Генерализированное тревожное расстройство"""
    __tablename__ = "gdr_disorder"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user = relationship("User", back_populates="gdr_disorder")

    gad_worry: Mapped[Optional[float]] = mapped_column(
        Float,
        default=None,
        comment="Чрезмерное беспокойство / тревожные ожидания (0-1)"
    )
    gad_uncontrollable: Mapped[Optional[float]] = mapped_column(
        Float,
        default=None,
        comment="Трудности с контролем беспокойства (0-1)"
    )
    gad_catastrophic: Mapped[Optional[float]] = mapped_column(
        Float,
        default=None,
        comment="Предчувствие беды / ощущение надвигающейся катастрофы (0-1)"
    )

    # Физические и поведенческие симптомы (ключевые по DSM-5 и GAD-7)
    gad_restlessness: Mapped[Optional[float]] = mapped_column(
        Float,
        default=None,
        comment="Моторное беспокойство, неусидчивость, ощущение на взводе (0-1)"
    )
    gad_fatigue: Mapped[Optional[float]] = mapped_column(
        Float,
        default=None,
        comment="Лёгкая утомляемость, быстрое истощение (0-1)"
    )
    gad_concentration: Mapped[Optional[float]] = mapped_column(
        Float,
        default=None,
        comment="Трудности с концентрацией внимания, «пустота в голове» (0-1)"
    )
    gad_irritability: Mapped[Optional[float]] = mapped_column(
        Float,
        default=None,
        comment="Раздражительность, вспыльчивость (0-1)"
    )
    gad_muscle_tension: Mapped[Optional[float]] = mapped_column(
        Float,
        default=None,
        comment="Мышечное напряжение, скованность (0-1)"
    )

    gad_relaxation: Mapped[Optional[float]] = mapped_column(
        Float,
        default=None,
        comment="Трудности с расслаблением (0-1)"
    )

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return GDRSchema
