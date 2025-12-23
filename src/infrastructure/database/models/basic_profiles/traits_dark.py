from typing import Type

from sqlalchemy import Column, Float
from sqlalchemy.orm import Mapped

from infrastructure.database.models.base import IDMixin, S


class ClinicalProfile(IDMixin):
    """КЛИНИЧЕСКАЯ-ПСИХОЛОГИЯ"""

    __tablename__ = "user_..."

    @property
    def schema_class(self) -> Type[S]:
        return ...


class DarkTriads(IDMixin):
    """ТЁМНАЯ ТРИАДА"""

    __tablename__ = "user_dark_triads"

    cynicism: Mapped[float | None] = Column(Float, default=None)  # trust → distrust of others' motives
    narcissism: Mapped[float | None] = Column(Float, default=None)  # modesty → self-admiration
    machiavellianism: Mapped[float | None] = Column(Float, default=None)  # directness → manipulative tendency
    psychoticism: Mapped[float | None] = Column(Float, default=None)  # normality → unusual experiences

    @property
    def schema_class(self) -> Type[S]:
        return ...
