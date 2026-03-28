from datetime import datetime
from typing import Optional
from uuid import uuid4, UUID

from pydantic import BaseModel, Field


class HexacoSchema(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    user_id: UUID = Field(description="Идентификатор пользователя")

    honesty_humility: float | None = Field(None, description="H: 0=манипулятивный, нарциссичный, жадный → 1=искренний, скромный, бескорыстный")
    emotionality: float | None = Field(None, description="E: эмоциональность, тревожность, сентиментальность")
    extraversion: float | None = Field(None, description="X: экстраверсия, социальность")
    agreeableness: float | None = Field(None, description="A: согласность, терпимость, мягкость")
    conscientiousness: float | None = Field(None, description="C: добросовестность, организованность")
    openness: float | None = Field(None, description="O: открытость опыту, креативность")

    records: int | None = Field(
        default=None,
        description="Количество записей"
    )

    created_at: datetime | None = Field(None)
    updated_at: datetime | None = Field(None)
