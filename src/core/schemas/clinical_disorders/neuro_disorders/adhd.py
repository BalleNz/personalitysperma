import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, computed_field


class ADHDSchema(BaseModel):
    """СДВГ схема"""
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID = Field(description="Идентификатор пользователя")

    adhd: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="уровень СДВГ (0-1)")
    adhd_inattention: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Невнимательность (0-1)")
    adhd_hyperactivity: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Гиперактивность (0-1)")

    hyperfocus: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Склонность к гиперфокусу (осознанная защитная реакция) (0-1)")
    internal_hyperactivity: Optional[float] = Field(default=None, ge=0.0, le=1.0,
                                                    description="Внутренняя гиперактивность / постоянный внутренний шум (0-1)")
    time_blindness: Optional[float] = Field(default=None, ge=0.0, le=1.0,
                                            description="Нарушение чувства времени / тайм-слепота (0-1)")
    motivation_problems: Optional[float] = Field(default=None, ge=0.0, le=1.0,
                                                 description="Проблемы с внутренней мотивацией / прокрастинация при отсутствии дофаминового 'пинка' (0-1)")

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
