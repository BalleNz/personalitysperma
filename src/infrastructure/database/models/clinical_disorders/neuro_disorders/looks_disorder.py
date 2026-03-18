from typing import Type

from sqlalchemy import Float, ForeignKey
from sqlalchemy.dialects.postgresql import UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.schemas.clinical_disorders.neuro_disorders.looks_disorder import LooksSchema
from src.infrastructure.database.models.base import S, IDMixin, TimestampsMixin


class LooksDisorder(IDMixin, TimestampsMixin):
    """Расстройства образа тела / дисморфофобические симптомы"""
    __tablename__ = "looks_disorder"

    user_id: Mapped[UUID] = mapped_column(
        UUID(as_uuid=True),
        ForeignKey("users.id", ondelete="CASCADE"),
        nullable=False
    )
    user = relationship("User", back_populates="looks_disorder")

    bdd_general = mapped_column(Float, default=None, comment="Общий уровень дисморфофобии (0-1)")

    muscle_dysmorphia = mapped_column(Float, default=None, comment="Мышечная дисморфия / bigorexia (0-1)")
    skin_hair_focus = mapped_column(Float, default=None, comment="Кожа, акне (0-1)")
    hair_focus = mapped_column(Float, default=None, comment="Облысение / растительность на лице (0-1)")
    facial_features = mapped_column(Float, default=None,
                                    comment="Черты лица (нос, губы, глаза, симметрия, луксмаксинг) (0-1)")

    body_fat = mapped_column(Float, default=None, comment="Жир, целлюлит, вес (0-1)")
    genitals_size = mapped_column(Float, default=None, comment="Размер / форма гениталий (0-1)")
    height_stature = mapped_column(Float, default=None, comment="Рост, пропорции тела, осанка (0-1)")
    aging = mapped_column(Float, default=None, comment="Старение (0-1)")

    reassurance = mapped_column(Float, default=None,
                                comment="Частота поиска подтверждения / вопросов о внешности (0-1)")
    impairment = mapped_column(Float, default=None,
                               comment="Нарушение жизни / избегание из-за озабоченности внешностью (0-1)")

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return LooksSchema
