from datetime import datetime

from sqlalchemy import String, DateTime, func, UUID, ForeignKey
from sqlalchemy.orm import mapped_column, Mapped

from src.infrastructure.database.models.base import IDMixin


class UserRecords(IDMixin):

    __tablename__ = "user_records"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    profile_name: Mapped[str] = mapped_column(String, index=True)  # __tablename__

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True
    )
