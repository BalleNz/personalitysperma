from typing import Optional
from uuid import uuid4, UUID

from pydantic import BaseModel, Field


class PersonalityDisordersSchema(BaseModel):
    """Базовая схема расстройств личности и настроения"""
    id: Optional[UUID] = Field(default_factory=uuid4)
    user_id: str = Field(description="Идентификатор пользователя")

    # [ ПРЛ ]
    bpd_severity: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Тяжесть ПРЛ (0-1)")
    bpd_abandonment: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Страх брошенности (0-1)")
    bpd_unstable_relations: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Нестабильные отношения (0-1)")
    bpd_identity: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Нарушение идентичности (0-1)")
    bpd_impulsivity: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Импульсивность (0-1)")
    bpd_suicidal: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Суицидальное поведение (0-1)")
    bpd_mood_swings: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Перепады настроения (0-1)")
    bpd_emptiness: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Чувство пустоты (0-1)")
    bpd_anger: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Неадекватный гнев (0-1)")
    bpd_paranoia: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Параноидные идеи (0-1)")

    # [ Другие РЛ ]
    npd: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Нарциссическое РЛ (0-1)")
    aspd: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Антисоциальное РЛ (0-1)")
    avpd: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Избегающее РЛ (0-1)")
    dpd: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Зависимое РЛ (0-1)")
    ocpd: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Обсессивно-компульсивное РЛ (0-1)")
    ppd: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Параноидное РЛ (0-1)")
    szpd: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Шизоидное РЛ (0-1)")
    stpd: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Шизотипическое РЛ (0-1)")
