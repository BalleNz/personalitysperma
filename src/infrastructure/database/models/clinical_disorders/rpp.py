from typing import Type

from sqlalchemy import Float, ForeignKey, UUID
from sqlalchemy.orm import mapped_column, Mapped, relationship

from src.infrastructure.database.models.base import TimestampsMixin, S, IDMixin


class EatingDisorders(IDMixin, TimestampsMixin):
    """Пищевое поведение"""
    __tablename__ = "eating_disorders"

    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="hexaco")

    eating = mapped_column(Float, default=None, comment="Общий уровень РПП (0-1)")
    anorexia = mapped_column(Float, default=None, comment="Нервная анорексия (0-1)")
    bulimia = mapped_column(Float, default=None, comment="Нервная булимия (0-1)")
    binge = mapped_column(Float, default=None, comment="Компульсивное переедание (0-1)")

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return ...
