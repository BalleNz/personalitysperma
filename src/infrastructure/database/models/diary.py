from typing import Type

from sqlalchemy import UUID, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.schemas.diary_schema import DiarySchema
from src.infrastructure.database.models.base import S
from src.infrastructure.database.models.base import TimestampsMixin, IDMixin


class UserDiary(IDMixin, TimestampsMixin):
    """Записи в дневник (сгенерированные)"""
    __tablename__ = "user_diary"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    user = relationship("User", back_populates="diary")

    text: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    @property
    def schema_class(cls) -> Type[S]:
        return DiarySchema
