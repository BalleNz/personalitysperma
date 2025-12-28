import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field


class AnxietyDisordersSchema(BaseModel):
    """Схема тревожных, ОКР и травматических расстройств"""
    # [ IDs ]
    id: uuid.UUID = Field(..., description="id")
    user_id: uuid.UUID = Field(..., description="user id")

    # [ ГТР ]
    gad: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Генерализованное тревожное расстройство (0-1)")
    gad_worry: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Беспокойство (0-1)")
    gad_restlessness: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Беспокойство/нервозность (0-1)")
    gad_fatigue: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Утомляемость (0-1)")
    gad_concentration: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Нарушения концентрации (0-1)")
    gad_irritability: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Раздражительность (0-1)")
    gad_muscle: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Мышечное напряжение (0-1)")
    gad_sleep: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Нарушения сна (0-1)")

    # [ Паническое ]
    panic: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Паническое расстройство (0-1)")
    panic_frequency: Optional[str] = Field(default=None, description="Частота панических атак")
    panic_anticipatory: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Тревога ожидания (0-1)")

    # [ Социальное ]
    social_anxiety: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Социальная тревога (0-1)")
    social_avoidance: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Избегание социальных ситуаций (0-1)")

    # [ Фобии ]
    agoraphobia: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Агорафобия (0-1)")
    specific_phobia: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Специфическая фобия (0-1)")
    phobia_type: Optional[str] = Field(default=None, description="Тип фобии")

    # [ ОКР и родственные ]
    ocd: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Обсессивно-компульсивное расстройство (0-1)")
    ocd_obsessions: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Навязчивые мысли (0-1)")
    ocd_compulsions: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Компульсивные действия (0-1)")
    ocd_insight: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Критичность к симптомам (0-1)")
    body_dysmorphia: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Дисморфофобия (0-1)")
    bfrb: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Повторяющееся поведение (0-1)")

    # [ Травма и стрессовые расстройства ]
    ptsd: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Посттравматическое стрессовое расстройство (0-1)")
    ptsd_intrusions: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Интрузивные воспоминания (0-1)")
    ptsd_avoidance: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Избегание триггеров (0-1)")
    ptsd_cognition: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Негативные мысли (0-1)")
    ptsd_arousal: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Гипервозбуждение (0-1)")
    acute_stress: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Острое стрессовое расстройство (0-1)")

    # [ Комплексное ПТСР ]
    cptsd: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Комплексное ПТСР (0-1)")
    cptsd_emotion: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Нарушения эмоциональной регуляции (0-1)")
    cptsd_self: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Нарушения самооценки (0-1)")
    cptsd_relations: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Нарушения в отношениях (0-1)")

    # [ Диссоциативные расстройства ]
    dissociative: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Диссоциативные симптомы (0-1)")
    amnesia: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Амнезия (0-1)")
    did: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Диссоциативное расстройство идентичности (0-1)")
    depersonalization: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Деперсонализация/дереализация (0-1)")

    created_at: datetime | None = Field(None)
    updated_at: datetime | None = Field(None)
