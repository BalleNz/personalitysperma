from datetime import datetime

from sqlalchemy import String, DateTime, func
from sqlalchemy.orm import mapped_column, Mapped

from src.infrastructure.database.models.base import IDMixin, TimestampsMixin


class UserRecords(IDMixin):

    __tablename__ = "user_records"

    user_id: Mapped[str] = mapped_column(String, index=True)

    profile_name: Mapped[str] = mapped_column(String, index=True)

    created_at: Mapped[datetime] = mapped_column(
        DateTime(timezone=True),
        nullable=False,
        server_default=func.now(),
        index=True
    )
