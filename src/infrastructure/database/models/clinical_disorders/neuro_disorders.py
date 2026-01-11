from typing import Type

from sqlalchemy import UUID, ForeignKey, Float, Integer
from sqlalchemy.orm import mapped_column, relationship, Mapped

from core.schemas.clinical_disorders.neuro_disorders import NeuroDisordersSchema
from infrastructure.database.models.base import TimestampsMixin, S, IDMixin


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

    records: Mapped[int | None] = mapped_column(
        Integer,
        default=None,
        comment="количество записей"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return NeuroDisordersSchema
