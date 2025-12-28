from datetime import datetime

from pydantic import BaseModel, Field


class UserHexacoSchema(BaseModel):
    honesty_humility: float | None = Field(None, description="H: 0=манипулятивный, нарциссичный, жадный → 1=искренний, скромный, бескорыстный")
    emotionality: float | None = Field(None, description="E: эмоциональность, тревожность, сентиментальность")
    extraversion: float | None = Field(None, description="X: экстраверсия, социальность")
    agreeableness: float | None = Field(None, description="A: согласность, терпимость, мягкость")
    conscientiousness: float | None = Field(None, description="C: добросовестность, организованность")
    openness: float | None = Field(None, description="O: открытость опыту, креативность")

    created_at: datetime | None = Field(None)
    updated_at: datetime | None = Field(None)
