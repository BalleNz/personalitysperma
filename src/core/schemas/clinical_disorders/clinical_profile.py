from datetime import datetime
from typing import Optional
from uuid import uuid4, UUID

from pydantic import BaseModel, Field, computed_field


class ClinicalProfileSchema(BaseModel):
    """Базовая схема клинического профиля"""
    id: Optional[UUID] = Field(default_factory=uuid4)
    user_id: UUID = Field(description="Идентификатор пользователя")

    overall_severity: Optional[str] = Field(default="NONE", description="Общая тяжесть состояния")
    diagnosis_status: Optional[str] = Field(default="NOT_DIAGNOSED", description="Статус диагностики")
    notes: Optional[str] = Field(default=None, description="Заметки и комментарии")

    # Суицидальность
    suicide_risk: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Уровень суицидального риска (0-1)")
    suicide_ideation_frequency: Optional[str] = Field(default=None, description="Частота суицидальных мыслей")

    records: int | None = Field(
        default=None,
        description="Количество записей"
    )

    @computed_field
    @property
    def accuracy_percent(self) -> float:
        """Процент точности"""
        records_count: int | None = self.records
        if records_count is None or records_count <= 0:
            return 0.0
        elif records_count == 1:
            return 0.04
        elif records_count == 2:
            return 0.09
        else:
            # при 7 записях: 42%
            # при 17 записях: 63%
            # при 27 записях: 71%
            # при 50 записях: 78%
            margin = 1.5081 / (records_count ** 0.5)
            return 1 - margin

    created_at: datetime | None = Field(None)
    updated_at: datetime | None = Field(None)
