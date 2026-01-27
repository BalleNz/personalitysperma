from datetime import datetime
from typing import Optional
from uuid import uuid4, UUID

from pydantic import BaseModel, Field


class UserHollandCodesSchema(BaseModel):
    """Схема для кодов Холланда (RIASEC)"""
    id: Optional[UUID] = Field(default_factory=uuid4)
    user_id: str = Field(description="Идентификатор пользователя")

    # Основные шкалы (0.0 — 1.0)
    realistic: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="R — Реалистичный тип: работа с инструментами, техникой, природой, спортом. Практические навыки, конкретные задачи."
    )
    investigative: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="I — Исследовательский тип: наука, анализ данных, решение сложных задач. Любознательность, аналитическое мышление."
    )
    artistic: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="A — Артистичный тип: творчество, самовыражение, искусство, дизайн. Воображение, нестандартное мышление."
    )
    social: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="S — Социальный тип: помощь людям, общение, обучение, консультирование. Эмпатия, коммуникативные навыки."
    )
    enterprising: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="E — Предприимчивый тип: лидерство, продажи, убеждение, бизнес. Амбициозность, организаторские способности."
    )
    conventional: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="C — Конвенциональный тип: порядок, правила, структура, финансы, администрирование. Точность, системность."
    )

    # Код Холланда и метаданные
    holland_code: str | None = Field(
        default=None,
        max_length=6,
        description="Трёхбуквенный код в порядке убывания значимости (например, 'RIA', 'SEC'). Автоматически вычисляется из оценок."
    )

    confidence_level: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Уверенность в точности определения типа (0.0 — совсем не уверен, 1.0 — абсолютно уверен)"
    )

    consistency_index: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Индекс согласованности типов (чем выше, тем более согласован профиль)"
    )

    differentiation_index: float | None = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Индекс дифференциации профиля (чем выше, тем более выражены различия между типами)"
    )

    notes: str | None = Field(
        default=None,
        description="Описание типа Холланда"
    )

    created_at: datetime | None = Field(None)
    updated_at: datetime | None = Field(None)
