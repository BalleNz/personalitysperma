from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, Field, ConfigDict


class CharacteristicBatchLogSchema(BaseModel):
    id: Optional[UUID] = Field(default_factory=uuid4)
    user_id: UUID
    characteristic_type: str = Field(max_length=64)
    message: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)


class UserLogSchema(BaseModel):
    id: UUID
    user_id: UUID
    log: str
    created_at: datetime
    updated_at: datetime

    model_config = ConfigDict(from_attributes=True)
