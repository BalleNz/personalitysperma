from typing import Optional

from pydantic import BaseModel, Field


class NeuroDisordersSchema(BaseModel):
    """Схема нейроразвития и пищевых расстройств"""
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
