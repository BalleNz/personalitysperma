from typing import Type

from pydantic import ConfigDict
from sqlalchemy import Float, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.schemas.triads.dark_triad import DarkTriadsSchema
from src.infrastructure.database.models.base import IDMixin, S, TimestampsMixin


class DarkTriads(IDMixin, TimestampsMixin):
    """ТЁМНАЯ ТРИАДА"""

    __tablename__ = "user_dark_triads"
    model_config = ConfigDict(from_attributes=True)

    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="dark_triads")

    cynicism: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="0=глубокая вера в доброту людей → 1=циничный, недоверие к мотивам людей"
    )
    narcissism: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Нарциссизм: 0=скромный → 1=самолюбование, грандиозность"
    )
    machiavellianism: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Макиавеллизм: 0=прямой и честный → 1=манипулятивный, хитрый"
    )
    psychoticism: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Психотизм: 0=нормальность, эмпатия → 1=холодность, необычный опыт"
    )
    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(self) -> Type[S]:
        return DarkTriadsSchema
