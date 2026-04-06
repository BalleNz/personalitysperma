from typing import Type

from pydantic import ConfigDict
from sqlalchemy import Float, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.schemas.triads.light_triad import LightTriadsSchema
from src.infrastructure.database.models.base import IDMixin, S, TimestampsMixin


class LightTriads(IDMixin, TimestampsMixin):
    """Светлая ТРИАДА"""

    __tablename__ = "user_dark_triads"
    model_config = ConfigDict(from_attributes=True)

    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="dark_triads")

    faith_in_humanity: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Вера в человечность: 0=цинизм и недоверие → 1=глубокая вера в доброту людей"
    )
    humanism: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Гуманизм: 0=видеть людей как средство → 1=видеть в людях ценность саму по себе"
    )
    kantianism: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Кантианство: 0=манипулятивность → 1=уважение к автономии и достоинству других"
    )
    humility: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Скромность / humility: 0=нарциссизм и высокомерие → 1=скромность и принятие себя"
    )

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(self) -> Type[S]:
        return LightTriadsSchema
