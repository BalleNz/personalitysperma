from datetime import datetime
from typing import Optional
from uuid import uuid4, UUID

from pydantic import BaseModel, Field, computed_field


class BPDSchema(BaseModel):
    """borderline personal disorder - ПРЛ"""
    id: Optional[UUID] = Field(default_factory=uuid4)
    user_id: UUID = Field(description="Идентификатор пользователя")

    bpd_severity: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Уровень ПРЛ (0-1)")
    bpd_abandonment: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Страх брошенности (0-1)")
    bpd_unstable_relations: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Нестабильные отношения (0-1)")
    bpd_identity: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Нарушение идентичности (0-1)")
    bpd_impulsivity: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Импульсивность (0-1)")
    bpd_mood_swings: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Перепады настроения (0-1)")
    bpd_emptiness: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Чувство пустоты (0-1)")
    bpd_anger: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Неадекватный гнев (0-1)")
    bpd_paranoia: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Параноидные идеи (0-1)")

    bpd_suicidal: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Суицидальное поведение, угрозы о суициде, самоповреждения (0-1)")

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
