from typing import Type

from sqlalchemy import UUID, ForeignKey, Float, CheckConstraint
from sqlalchemy.orm import mapped_column, relationship

from infrastructure.database.models.base import TimestampsMixin, S, IDMixin
from core.schemas.clinical_disorders.neuro_disorders import NeuroDisordersSchema


class NeuroDisorders(IDMixin, TimestampsMixin):
    """НЕЙРОРАЗВИТИЯ И ПИЩЕВЫЕ РАССТРОЙСТВА"""
    __tablename__ = "neuro_disorders"

    user_id = mapped_column(UUID, ForeignKey('users.id'), nullable=False, unique=True, comment="ID пользователя")
    user = relationship("User", back_populates="neurodevelopmental_eating_disorder")

    # [ Нейроразвития и неврологические ]
    adhd = mapped_column(Float, default=None, comment="вероятность СДВГ (0-1)")
    adhd_inattention = mapped_column(Float, default=None, comment="Невнимательность (0-1)")
    adhd_hyperactivity = mapped_column(Float, default=None, comment="Гиперактивность (0-1)")
    adhd_impulsivity = mapped_column(Float, default=None, comment="Импульсивность (0-1)")

    autism = mapped_column(Float, default=None, comment="Аутистические черты (0-1)")
    autism_social = mapped_column(Float, default=None, comment="Нарушения социальной коммуникации (0-1)")
    autism_interests = mapped_column(Float, default=None, comment="Ограниченные интересы/ритуалы (0-1)")

    # [ Расстройства пищевого поведения ]
    eating = mapped_column(Float, default=None, comment="Общий уровень РПП (0-1)")
    anorexia = mapped_column(Float, default=None, comment="Нервная анорексия (0-1)")
    bulimia = mapped_column(Float, default=None, comment="Нервная булимия (0-1)")
    binge = mapped_column(Float, default=None, comment="Компульсивное переедание (0-1)")

    @property
    def schema_class(cls) -> Type[S]:
        return NeuroDisordersSchema

    __table_args__ = (
        CheckConstraint('adhd >= 0 AND adhd <= 1.00', name='ck_adhd_range'),
        CheckConstraint('adhd_inattention >= 0 AND adhd_inattention <= 1.00', name='ck_adhd_inattention_range'),
        CheckConstraint('adhd_hyperactivity >= 0 AND adhd_hyperactivity <= 1.00', name='ck_adhd_hyperactivity_range'),
        CheckConstraint('adhd_impulsivity >= 0 AND adhd_impulsivity <= 1.00', name='ck_adhd_impulsivity_range'),
        CheckConstraint('autism >= 0 AND autism <= 1.00', name='ck_autism_range'),
        CheckConstraint('autism_social >= 0 AND autism_social <= 1.00', name='ck_autism_social_range'),
        CheckConstraint('autism_interests >= 0 AND autism_interests <= 1.00', name='ck_autism_interests_range'),
        CheckConstraint('eating >= 0 AND eating <= 1.00', name='ck_eating_range'),
        CheckConstraint('anorexia >= 0 AND anorexia <= 1.00', name='ck_anorexia_range'),
        CheckConstraint('bulimia >= 0 AND bulimia <= 1.00', name='ck_bulimia_range'),
        CheckConstraint('binge >= 0 AND binge <= 1.00', name='ck_binge_range'),
    )
