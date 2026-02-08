from typing import Type

from sqlalchemy import UUID, ForeignKey, String, Text, Index
from sqlalchemy.orm import mapped_column, Mapped

from src.core.schemas.log_schemas import CharacteristicBatchLogSchema, UserLogSchema
from src.infrastructure.database.models.base import S, IDMixin, TimestampsMixin


class CharacteristicBatchLog(IDMixin, TimestampsMixin):
    """Пре-батчи для характеристик"""
    __tablename__ = "characteristic_batch_logs"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    characteristic_type: Mapped[str] = mapped_column(
        String(64),
        nullable=False,
        index=True
    )

    message: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    __table_args__ = (
        Index(
            "ix_batch_user_type_created",
            "user_id",
            "characteristic_type",
            "created_at"
        ),
    )

    @property
    def schema_class(self) -> Type[S]:
        return CharacteristicBatchLogSchema


class UserLog(IDMixin, TimestampsMixin):
    """Просто логи"""
    __tablename__ = "user_logs"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id"),
        nullable=False,
        index=True
    )

    log: Mapped[str] = mapped_column(
        Text,
        nullable=False
    )

    __table_args__ = (
        # Составной индекс: пользователь + дата создания
        Index('idx_userlog_user_date', 'user_id', 'created_at'),

        # Индекс по дате создания (для временных выборок)
        Index('idx_userlog_date', 'created_at'),

        Index('idx_userlog_user_created_at', 'user_id', 'created_at')

    )

    @property
    def schema_class(cls) -> Type[S]:
        return UserLogSchema
