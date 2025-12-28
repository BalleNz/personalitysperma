from typing import Type

from pydantic import BaseModel
from sqlalchemy import UUID, ForeignKey, Float, String, Text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models.base import IDMixin, TimestampsMixin
from core.schemas.personality_types.holland_codes import UserHollandCodesSchema


class UserHollandCodes(IDMixin, TimestampsMixin):
    """
    Holland Codes (RIASEC) — модель Джона Холланда для Профессиональных интересов и образа жизни.
    Шесть типов:
        — Realistic (R), Investigative (I), Artistic (A), Social (S), Enterprising (E), Conventional (C).
    Сумма всех шести шкал обычно ≈ 1.0 (или нормализуется до 1), чтобы показать распределение.
    Также храним топ-3 код (например, "RIA") для быстрого поиска похожих/противоположных.
    """

    __tablename__ = "user_holland_codes"

    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('users.id'), nullable=False, unique=True)
    user = relationship("User", back_populates="holland_codes")

    # Основные шесть шкал (0.0 — 1.0, где 1.0 = максимально выражено)
    realistic: Mapped[float | None] = mapped_column(Float, default=None, comment="R — Реалистичный: работа руками, техника, природа, спорт")
    investigative: Mapped[float | None] = mapped_column(Float, default=None, comment="I — Исследовательский: наука, анализ, решение сложных задач")
    artistic: Mapped[float | None] = mapped_column(Float, default=None, comment="A — Артистичный: творчество, самовыражение, искусство")
    social: Mapped[float | None] = mapped_column(Float, default=None, comment="S — Социальный: помощь людям, общение, обучение")
    enterprising: Mapped[float | None] = mapped_column(Float, default=None, comment="E — Предприимчивый: лидерство, продажи, убеждение")
    conventional: Mapped[float | None] = mapped_column(Float, default=None, comment="C — Конвенциональный: порядок, правила, структура, финансы")

    # Трёхбуквенный код в порядке убывания (например, "RIA", "SEC")
    holland_code: Mapped[str | None] = mapped_column(String(6), default=None, comment="Топ-3 типа, например 'RIA' или 'SEC'")

    confidence_level: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Уверенность в точности определения типа (0.0 — совсем не уверен, 1.0 — абсолютно уверен)"
    )
    differentiation_index: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Индекс дифференциации профиля (чем выше, тем более выражены различия между типами)"
    )
    consistency_index: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Индекс согласованности типов (чем выше, тем более согласован профиль)"
    )

    notes: Mapped[str | None] = mapped_column(
        Text,
        default=None,
        comment="Описание типа Холланда"
    )

    @property
    def schema_class(self) -> Type[BaseModel]:
        return UserHollandCodesSchema
