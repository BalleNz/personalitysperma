from typing import Type

from pydantic import BaseModel
from sqlalchemy import Float, ForeignKey, UUID, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.schemas.personality_types.hexaco import UserHexacoSchema
from src.infrastructure.database.models.base import TimestampsMixin, IDMixin


class UserHexaco(IDMixin, TimestampsMixin):
    """
    Модель личности HEXACO (6 факторов).
    Ключевая для совместимости — H (Honesty-Humility): низкие значения связаны с манипулятивностью,
    нарциссизмом, макиавеллизмом, психопатией (Dark Triad).
    Низкий H — красный флаг для долгосрочных отношений.
    """

    __tablename__ = "user_hexaco"

    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="hexaco")

    # H — Честность-Смирение (ключевой для токсичности)
    honesty_humility: Mapped[float | None] = mapped_column(Float, default=None, comment="H: 0=манипулятивный, нарциссичный, жадный → 1=искренний, скромный, бескорыстный")
    emotionality: Mapped[float | None] = mapped_column(Float, default=None, comment="E: эмоциональность, тревожность, сентиментальность")
    extraversion: Mapped[float | None] = mapped_column(Float, default=None, comment="X: экстраверсия, социальность")
    agreeableness: Mapped[float | None] = mapped_column(Float, default=None, comment="A: согласность, терпимость, мягкость")
    conscientiousness: Mapped[float | None] = mapped_column(Float, default=None, comment="C: добросовестность, организованность")
    openness: Mapped[float | None] = mapped_column(Float, default=None, comment="O: открытость опыту, креативность")

    records: Mapped[int | None] = mapped_column(
        Integer,
        default=None,
        comment="количество записей"
    )

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(self) -> Type[BaseModel]:
        return UserHexacoSchema
