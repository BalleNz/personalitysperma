from typing import Type

from infrastructure.database.models.base import IDMixin, S


class ClinicalProfile(IDMixin):
    """КЛИНИЧЕСКАЯ-ПСИХОЛОГИЯ"""

    __tablename__ = "user_..."

    @property
    def schema_class(self) -> Type[S]:
        return ...
