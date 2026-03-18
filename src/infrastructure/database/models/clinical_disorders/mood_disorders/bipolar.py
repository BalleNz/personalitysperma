from typing import Type

from sqlalchemy import Float, UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped, relationship

from schemas.clinical_disorders.mood_disorders.bipolar import BipolarDisorderSchema
from src.infrastructure.database.models.base import S, IDMixin, TimestampsMixin


class BipolarDisorder(IDMixin, TimestampsMixin):
    """Биполярное расстройство"""
    __tablename__ = "bipolar_disorder"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user = relationship("User", back_populates="bipolar_disorder")

    bipolar_mania = mapped_column(Float, default=None, comment="Маниакальные эпизоды (0-1)")
    bipolar_hypomania = mapped_column(Float, default=None, comment="Гипоманиакальные эпизоды (0-1)")
    bipolar_depression = mapped_column(Float, default=None, comment="Депрессивные эпизоды (0-1)")
    bipolar_rapid = mapped_column(Float, default=None, comment="Частота смены фаз (0-1)")
    bipolar_psychotic = mapped_column(Float, default=None, comment="Психотические черты (0-1)")

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return BipolarDisorderSchema
