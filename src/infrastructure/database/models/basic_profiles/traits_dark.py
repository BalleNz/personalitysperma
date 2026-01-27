from typing import Type

from sqlalchemy import Float, Integer, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.schemas.traits.traits_dark import DarkTriadsSchema
from src.infrastructure.database.models.base import IDMixin, S, TimestampsMixin


class DarkTriads(IDMixin, TimestampsMixin):
    """ТЁМНАЯ ТРИАДА"""

    __tablename__ = "user_dark_triads"

    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('users.id'), nullable=False, unique=True)
    user = relationship("User", back_populates="dark_triads")

    cynicism: Mapped[float | None] = mapped_column(Float, default=None)  # trust → distrust of others' motives
    narcissism: Mapped[float | None] = mapped_column(Float, default=None)  # modesty → self-admiration
    machiavellianism: Mapped[float | None] = mapped_column(Float, default=None)  # directness → manipulative tendency
    psychoticism: Mapped[float | None] = mapped_column(Float, default=None)  # normality → unusual experiences

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
    def schema_class(self) -> Type[S]:
        return DarkTriadsSchema
