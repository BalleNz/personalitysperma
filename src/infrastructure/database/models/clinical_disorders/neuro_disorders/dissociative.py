from typing import Type

from sqlalchemy import Float, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.schemas.clinical_disorders.neuro_disorders.dissociative import DissociativeSchema
from src.infrastructure.database.models.base import TimestampsMixin, IDMixin, S


class DissociativeDisorder(IDMixin, TimestampsMixin):
    """Диссоциативные расстройства"""
    __tablename__ = "dissociative_disorder"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user = relationship("User", back_populates="dissociative_disorder")

    dissociative = mapped_column(Float, default=None, comment="Диссоциативные симптомы (0-1)")
    depersonalization = mapped_column(Float, default=None, comment="Деперсонализация / дереализация (0-1)")
    amnesia = mapped_column(Float, default=None, comment="Амнезия (0-1)")
    did = mapped_column(Float, default=None, comment="Диссоциативное расстройство идентичности / раздвоение личности (0-1)")

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return DissociativeSchema
