from typing import Type

from sqlalchemy import Float, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.schemas.clinical_disorders.mood_disorders.depression import DepressionSchema
from src.infrastructure.database.models.base import TimestampsMixin, IDMixin, S


class DepressionDisorder(IDMixin, TimestampsMixin):
    """Депрессия"""
    __tablename__ = "depression_disorder"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user = relationship("User", back_populates="depression_disorder")

    anhedonia = mapped_column(Float, default=None, comment="Ангедония / потеря интереса и удовольствия (0-1)")
    fatigue = mapped_column(Float, default=None, comment="Усталость, потеря энергии, ощущение истощения (0-1)")
    sleep_disturbance = mapped_column(Float, default=None, comment="Нарушения сна (бессонница / гиперсомния) (0-1)")
    worthlessness = mapped_column(Float, default=None, comment="Чувство никчёмности, вины (0-1)")
    suicidal = mapped_column(Float, default=None, comment="Суицидальные мысли / поведение (0-1)")

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return DepressionSchema
