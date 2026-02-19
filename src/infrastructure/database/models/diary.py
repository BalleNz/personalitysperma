from datetime import datetime
from typing import Type

from sqlalchemy import UUID, ForeignKey, String, Date, UniqueConstraint
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.schemas.diary_schema import DiarySchema
from src.infrastructure.database.models.base import IDMixin, S


class UserDiary(IDMixin):
    """Записи в дневник (сгенерированные)"""
    __tablename__ = "user_diary"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )
    user = relationship("User", back_populates="diary")

    context_text: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    text: Mapped[str] = mapped_column(
        String,
        nullable=False
    )

    created_at: Mapped[datetime.date] = mapped_column(Date, nullable=False, index=True, unique=True)

    __table_args__ = (
        UniqueConstraint("user_id", "created_at", name="uq_user_diary_one_per_day"),
    )

    @property
    def schema_class(cls) -> Type[S]:
        return DiarySchema
