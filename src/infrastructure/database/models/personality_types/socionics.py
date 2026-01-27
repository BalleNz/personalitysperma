from typing import Type

from sqlalchemy import UUID, ForeignKey, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.enums.socionics import SocionicsType
from src.core.schemas.personality_types.socionics_type import UserSocionicsSchema
from src.infrastructure.database.models.base import IDMixin, S, TimestampsMixin

SocionicsTypeEnum = Enum(
    SocionicsType,
    name="socionics_type",
    values_callable=lambda obj: [e.value for e in obj]
)


class UserSocionics(IDMixin, TimestampsMixin):
    """
    Соционика — 16 соционических типов (на основе Юнга, но с межтиповыми отношениями).
    Храним тип.
    В схеме вычисляем дополнительные признаки.
    """

    __tablename__ = "user_socionics"

    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('users.id'), nullable=False, unique=True)
    user = relationship("User", back_populates="socionics")

    socionics_type: Mapped[str | None] = mapped_column(SocionicsTypeEnum, default=None)

    @property
    def schema_class(self) -> Type[S]:
        return UserSocionicsSchema
