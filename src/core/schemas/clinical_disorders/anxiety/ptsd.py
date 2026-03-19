from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, computed_field


class PTSDSchema(BaseModel):
    """ПТСР"""
    id: Optional[UUID] = Field(default_factory=uuid4)
    user_id: UUID = Field(description="Идентификатор пользователя")

    ptsd: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Общий уровень ПТСР / комплексного ПТСР (0-1)")
    ptsd_intrusions: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Интрузивные воспоминания, флэшбэки (0-1)")
    ptsd_cognition: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Негативные изменения в мышлении и настроении (0-1)")
    ptsd_arousal: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Гипервозбуждение при триггере (0-1)")

    ptsd_self: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Нарушения самооценки, чувство никчёмности (0-1)")  # напрямую формируется ПТСРом
    ptsd_avoidance: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Избегание триггеров, мыслей, мест (0-1)")
    ptsd_relations: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Нарушения в отношениях, недоверие (0-1)")  # напрямую формируется ПТСРом

    records: int | None = Field(default=None, description="Количество записей")

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
