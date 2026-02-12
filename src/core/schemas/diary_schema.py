from uuid import UUID

from pydantic import BaseModel, Field


class DiarySchema(BaseModel):
    id: UUID
    user_id: UUID

    text: str = Field(..., description="Запись в дневнике")
