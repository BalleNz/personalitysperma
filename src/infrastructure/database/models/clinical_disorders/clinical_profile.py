from typing import Type

from sqlalchemy import ForeignKey, UUID, String, DateTime, Boolean, Text, Float, Integer, CheckConstraint
from sqlalchemy.orm import mapped_column, relationship

from infrastructure.database.models.base import IDMixin, S
from core.schemas.clinical_disorders.clinical_profile import ClinicalProfileSchema


class ClinicalProfile(IDMixin):
    """ОСНОВНОЙ КЛИНИЧЕСКИЙ ПРОФИЛЬ"""
    __tablename__ = "clinical_profiles"

    user_id = mapped_column(UUID, ForeignKey('users.id'), nullable=False, unique=True, comment="ID пользователя")
    user = relationship("User", back_populates="clinical_profile")

    # [ Общая информация ]
    overall_severity = mapped_column(String(20), default="NONE", comment="Общая тяжесть состояния")  # TODO: enum
    diagnosis_status = mapped_column(String(30), default="NOT_DIAGNOSED", comment="Статус диагностики")  # TODO: enum

    notes = mapped_column(Text, default=None, comment="Заметки и комментарии")

    # [ Суицидальность ]
    suicide_risk = mapped_column(Float, default=None, comment="Уровень суицидального риска (0-1)")
    suicide_ideation_frequency = mapped_column(String(20), default=None, comment="Частота суицидальных мыслей")  # TODO: enum

    __table_args__ = (
        CheckConstraint('suicide_risk >= 0 AND suicide_risk <= 1.00', name='ck_suicide_risk_range'),
    )

    @property
    def schema_class(self) -> Type[S]:
        return ClinicalProfileSchema
