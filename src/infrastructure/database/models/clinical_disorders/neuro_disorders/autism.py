from typing import Type

from sqlalchemy import Float, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.schemas.clinical_disorders.neuro_disorders.autism import AutismSchema
from src.infrastructure.database.models.base import TimestampsMixin, IDMixin, S


class AutismDisorder(IDMixin, TimestampsMixin):
    """Аутизм"""
    __tablename__ = "autism_disorder"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user = relationship("User", back_populates="autism_disorder")

    autism = mapped_column(Float, default=None, comment="Аутистические черты (0-1)")
    autism_social = mapped_column(Float, default=None, comment="Нарушения социальной коммуникации (0-1)")
    autism_interests = mapped_column(Float, default=None, comment="Ограниченные интересы/ритуалы (0-1)")

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return AutismSchema
