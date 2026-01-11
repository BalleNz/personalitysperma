from datetime import datetime
from typing import Optional
from uuid import UUID

from pydantic import Field, BaseModel


class UserTelegramDataSchema(BaseModel):
    telegram_id: str = Field(..., description="Телеграм айди")  # telegram id
    username: str = Field(..., description="Имя пользователя (логин) для идентификации.")
    first_name: Optional[str] = Field(None, description="first name")
    last_name: Optional[str] = Field(None, description="last name")
    auth_date: datetime | None = Field(datetime.now(), description="дата авторизации")

    class Config:
        from_attributes = True


class UserSchema(BaseModel):
    telegram_id: str = Field(..., description="Уникальный идентификатор пользователя в Telegram")
    username: str = Field(..., description="Имя пользователя в Telegram")
    first_name: Optional[str] = Field(None, description="Имя пользователя")
    last_name: Optional[str] = Field(None, description="Фамилия пользователя")
    age: int = Field(..., description="приблизительный возраст пользователя")

    created_at: datetime | None = Field(None)
    updated_at: datetime | None = Field(None)
