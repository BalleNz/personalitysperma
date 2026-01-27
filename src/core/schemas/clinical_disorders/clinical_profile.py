from datetime import datetime
from typing import Optional
from uuid import uuid4, UUID

from pydantic import BaseModel, Field


class ClinicalProfileSchema(BaseModel):
    """Базовая схема клинического профиля"""
    id: Optional[UUID] = Field(default_factory=uuid4)
    user_id: str = Field(description="Идентификатор пользователя")

    overall_severity: Optional[str] = Field(default="NONE", description="Общая тяжесть состояния")
    diagnosis_status: Optional[str] = Field(default="NOT_DIAGNOSED", description="Статус диагностики")
    notes: Optional[str] = Field(default=None, description="Заметки и комментарии")

    # Суицидальность
    suicide_risk: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Уровень суицидального риска (0-1)")
    suicide_ideation_frequency: Optional[str] = Field(default=None, description="Частота суицидальных мыслей")

    created_at: datetime | None = Field(None)
    updated_at: datetime | None = Field(None)
