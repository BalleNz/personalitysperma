from typing import Type

from sqlalchemy import ForeignKey, UUID, String, Text, Float, Integer
from sqlalchemy.orm import mapped_column, relationship, Mapped

from src.core.schemas.clinical_disorders.clinical_profile import ClinicalProfileSchema
from src.infrastructure.database.models.base import TimestampsMixin, IDMixin, S


class ClinicalProfile(IDMixin, TimestampsMixin):
    """ОСНОВНОЙ КЛИНИЧЕСКИЙ ПРОФИЛЬ"""
    __tablename__ = "clinical_profiles"

    user_id = mapped_column(UUID, ForeignKey('users.id', ondelete="CASCADE"), nullable=False, comment="ID пользователя")
    user = relationship("User", back_populates="clinical_profile")

    # [ Общая информация ]
    overall_severity = mapped_column(String(20), default="NONE", comment="Общая тяжесть состояния")  # TODO: enum
    diagnosis_status = mapped_column(String(30), default="NOT_DIAGNOSED", comment="Статус диагностики")  # TODO: enum

    notes = mapped_column(Text, default=None, comment="Заметки и комментарии исходя из других характеристик")

    # [ Суицидальность ]
    suicide_risk = mapped_column(Float, default=None, comment="Уровень суицидального риска (0-1)")
    suicide_ideation_frequency = mapped_column(String(20), default=None, comment="Частота суицидальных мыслей")  # TODO: enum

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
        return ClinicalProfileSchema
