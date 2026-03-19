from typing import Type

from sqlalchemy import Float, UUID, ForeignKey
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.schemas.clinical_disorders.neuro_disorders.eating import EatingSchema
from src.infrastructure.database.models.base import TimestampsMixin, IDMixin, S


class EatingDisorder(IDMixin, TimestampsMixin):
    """Пищевое поведение"""
    __tablename__ = "eating_disorder"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False,
        index=True
    )
    user = relationship("User", back_populates="eating_disorder")

    eating = mapped_column(Float, default=None, comment="Общий уровень РПП (0-1)")
    anorexia = mapped_column(Float, default=None, comment="Нарушение аппетита / анорексия (0-1)")
    bulimia = mapped_column(Float, default=None, comment="Слишком сильный аппетит / булимия (0-1)")
    binge = mapped_column(Float, default=None, comment="Компульсивное переедание (0-1)")

    body_image_distress = mapped_column(Float, default=None,
                                        comment="Дистресс от образа тела / недовольство внешностью (0-1)")
    compensatory_behaviors = mapped_column(Float, default=None,
                                           comment="Компенсаторное поведение (рвота, слабительные, чрезмерные тренировки) (0-1)")

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return EatingSchema
