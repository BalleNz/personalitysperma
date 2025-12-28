from typing import Union, Type

from sqlalchemy import CheckConstraint, Float, ForeignKey, UUID
from sqlalchemy.orm import mapped_column, relationship

from infrastructure.database.models.base import S, IDMixin, TimestampsMixin
from core.schemas.clinical_disorders.mood_disorders import MoodDisordersSchema


class MoodDisorders(IDMixin, TimestampsMixin):
    """РАССТРОЙСТВА НАСТРОЕНИЯ"""
    __tablename__ = "mood_disorders"

    user_id = mapped_column(UUID, ForeignKey('users.id'), nullable=False, unique=True, comment="ID пользователя")
    user = relationship("User", back_populates="mood_disorder")

    # [ Депрессия ]
    depression = mapped_column(Float, default=None, comment="Уровень депрессии (0-1)")
    depression_sadness = mapped_column(Float, default=None, comment="Грусть (0-1)")
    depression_anhedonia = mapped_column(Float, default=None, comment="Ангедония (0-1)")
    depression_appetite = mapped_column(Float, default=None, comment="Нарушение аппетита (0-1)")
    depression_sleep = mapped_column(Float, default=None, comment="Нарушения сна (0-1)")
    depression_fatigue = mapped_column(Float, default=None, comment="Усталость (0-1)")
    depression_worthlessness = mapped_column(Float, default=None, comment="Чувство никчемности (0-1)")
    depression_concentration = mapped_column(Float, default=None, comment="Нарушения концентрации (0-1)")
    depression_suicidal = mapped_column(Float, default=None, comment="Суицидальные мысли (0-1)")

    # [ Биполярное расстройство ]
    bipolar = mapped_column(Float, default=None, comment="Биполярное расстройство (0-1)")
    bipolar_mania = mapped_column(Float, default=None, comment="Маниакальные эпизоды (0-1)")
    bipolar_hypomania = mapped_column(Float, default=None, comment="Гипоманиакальные эпизоды (0-1)")
    bipolar_depression = mapped_column(Float, default=None, comment="Депрессивные эпизоды (0-1)")
    bipolar_rapid = mapped_column(Float, default=None, comment="Быстрая смена фаз (0-1)")
    bipolar_psychotic = mapped_column(Float, default=None, comment="Психотические черты (0-1)")

    # [ Циклотимия ]
    cyclothymia = mapped_column(Float, default=None, comment="Циклотимия (0-1)")

    @property
    def schema_class(cls) -> Type[S]:
        return MoodDisordersSchema

    __table_args__ = (
        CheckConstraint('depression >= 0 AND depression <= 1.00', name='ck_depression_range'),
        CheckConstraint('depression_sadness >= 0 AND depression_sadness <= 1.00', name='ck_depression_sadness_range'),
        CheckConstraint('depression_anhedonia >= 0 AND depression_anhedonia <= 1.00', name='ck_depression_anhedonia_range'),
        CheckConstraint('depression_appetite >= 0 AND depression_appetite <= 1.00', name='ck_depression_appetite_range'),
        CheckConstraint('depression_sleep >= 0 AND depression_sleep <= 1.00', name='ck_depression_sleep_range'),
        CheckConstraint('depression_fatigue >= 0 AND depression_fatigue <= 1.00', name='ck_depression_fatigue_range'),
        CheckConstraint('depression_worthlessness >= 0 AND depression_worthlessness <= 1.00', name='ck_depression_worthlessness_range'),
        CheckConstraint('depression_concentration >= 0 AND depression_concentration <= 1.00', name='ck_depression_concentration_range'),
        CheckConstraint('depression_suicidal >= 0 AND depression_suicidal <= 1.00', name='ck_depression_suicidal_range'),
        CheckConstraint('bipolar >= 0 AND bipolar <= 1.00', name='ck_bipolar_range'),
        CheckConstraint('bipolar_mania >= 0 AND bipolar_mania <= 1.00', name='ck_bipolar_mania_range'),
        CheckConstraint('bipolar_hypomania >= 0 AND bipolar_hypomania <= 1.00', name='ck_bipolar_hypomania_range'),
        CheckConstraint('bipolar_depression >= 0 AND bipolar_depression <= 1.00', name='ck_bipolar_depression_range'),
        CheckConstraint('bipolar_rapid >= 0 AND bipolar_rapid <= 1.00', name='ck_bipolar_rapid_range'),
        CheckConstraint('bipolar_psychotic >= 0 AND bipolar_psychotic <= 1.00', name='ck_bipolar_psychotic_range'),
        CheckConstraint('cyclothymia >= 0 AND cyclothymia <= 1.00', name='ck_cyclothymia_range'),
    )
