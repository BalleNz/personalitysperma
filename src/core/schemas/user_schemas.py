from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field, BaseModel


class UserSchema(BaseModel):
    telegram_id: str = Field(..., description="Уникальный идентификатор пользователя в Telegram")
    username: str = Field(..., description="Имя пользователя в Telegram")
    first_name: Optional[str] = Field(None, description="Имя пользователя")
    last_name: Optional[str] = Field(None, description="Фамилия пользователя")
    age: int = Field(..., description="приблизительный возраст пользователя")

    created_at: datetime | None = Field(None)
    updated_at: datetime | None = Field(None)


class CharacteristicHistorySchema(BaseModel):
    user_id: UUID = Field(..., description="ID пользователя, которому принадлежит характеристика")
    profile_type: str = Field(..., description="название таблицы")
    characteristic_name: str = Field(..., description="Название характеристики")
    old_value: float = Field(..., description="Предыдущее значение характеристики")
    new_value: float = Field(..., description="Новое значение характеристики")

    created_at: datetime | None = Field(None)
    updated_at: datetime | None = Field(None)
