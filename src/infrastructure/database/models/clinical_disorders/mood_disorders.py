from typing import Type

from sqlalchemy import Float, ForeignKey, UUID, Integer
from sqlalchemy.orm import mapped_column, relationship, Mapped

from core.schemas.clinical_disorders.mood_disorders import MoodDisordersSchema
from infrastructure.database.models.base import S, IDMixin, TimestampsMixin


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

    records: Mapped[int | None] = mapped_column(
        Integer,
        default=None,
        comment="количество записей"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return MoodDisordersSchema
