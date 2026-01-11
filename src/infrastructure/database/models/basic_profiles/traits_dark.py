from typing import Type

from sqlalchemy import Float, Integer
from sqlalchemy.orm import Mapped, mapped_column

from core.schemas.traits.traits_dark import DarkTriadsSchema
from infrastructure.database.models.base import IDMixin, S, TimestampsMixin


class DarkTriads(IDMixin, TimestampsMixin):
    """ТЁМНАЯ ТРИАДА"""

    __tablename__ = "user_dark_triads"

    cynicism: Mapped[float | None] = mapped_column(Float, default=None)  # trust → distrust of others' motives
    narcissism: Mapped[float | None] = mapped_column(Float, default=None)  # modesty → self-admiration
    machiavellianism: Mapped[float | None] = mapped_column(Float, default=None)  # directness → manipulative tendency
    psychoticism: Mapped[float | None] = mapped_column(Float, default=None)  # normality → unusual experiences

    records: Mapped[int | None] = mapped_column(
        Integer,
        default=None,
        comment="количество записей"
    )

    @property
    def schema_class(self) -> Type[S]:
        return DarkTriadsSchema
