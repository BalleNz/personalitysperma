import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, computed_field


class NeuroDisordersSchema(BaseModel):
    """Схема нейроразвития и пищевых расстройств"""

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID = Field(description="Идентификатор пользователя")

    # [ Нейроразвития и неврологические ]
    adhd: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="СДВГ (0-1)")
    adhd_inattention: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Невнимательность (0-1)")
    adhd_hyperactivity: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Гиперактивность (0-1)")
    adhd_impulsivity: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Импульсивность (0-1)")

    autism: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Аутистические черты (0-1)")
    autism_social: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Нарушения социальной коммуникации (0-1)")
    autism_interests: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Ограниченные интересы/ритуалы (0-1)")

    # [ Расстройства пищевого поведения ]
    eating: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Общий уровень РПП (0-1)")
    anorexia: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Нервная анорексия (0-1)")
    bulimia: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Нервная булимия (0-1)")
    binge: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Компульсивное переедание (0-1)")

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
