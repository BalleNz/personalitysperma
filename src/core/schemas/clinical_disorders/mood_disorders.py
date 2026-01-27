from datetime import datetime
from typing import Optional
from uuid import uuid4, UUID

from pydantic import BaseModel, Field


class MoodDisordersSchema(BaseModel):

    id: Optional[UUID] = Field(default_factory=uuid4)
    user_id: str = Field(description="Идентификатор пользователя")

    # [ Депрессия ]
    depression: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Уровень депрессии (0-1)")
    depression_sadness: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Грусть (0-1)")
    depression_anhedonia: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Ангедония (0-1)")
    depression_appetite: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Нарушение аппетита (0-1)")
    depression_sleep: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Нарушения сна (0-1)")
    depression_fatigue: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Усталость (0-1)")
    depression_worthlessness: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Чувство никчемности (0-1)")
    depression_concentration: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Нарушения концентрации (0-1)")
    depression_suicidal: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Суицидальные мысли (0-1)")

    # [ Биполярное расстройство ]
    bipolar: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Биполярное расстройство (0-1)")
    bipolar_mania: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Маниакальные эпизоды (0-1)")
    bipolar_hypomania: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Гипоманиакальные эпизоды (0-1)")
    bipolar_depression: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Депрессивные эпизоды (0-1)")
    bipolar_rapid: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Быстрая смена фаз (0-1)")
    bipolar_psychotic: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Психотические черты (0-1)")

    # [ Циклотимия ]
    cyclothymia: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Циклотимия (0-1)")

    created_at: datetime | None = Field(None)
    updated_at: datetime | None = Field(None)
