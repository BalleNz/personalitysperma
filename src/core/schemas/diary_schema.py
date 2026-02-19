import datetime
from uuid import UUID

from pydantic import BaseModel, Field, ConfigDict


class DiarySchema(BaseModel):
    id: UUID
    user_id: UUID

    context_text: str = Field(..., description="Оглавление")
    text: str = Field(..., description="Запись в дневнике")

    created_at: datetime.date

    model_config = ConfigDict(from_attributes=True)
