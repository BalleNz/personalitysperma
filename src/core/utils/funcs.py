from typing import Type, Any

from aiogram.types import User
from pydantic import BaseModel

from src.core.schemas.user_schemas import UserTelegramDataSchema
from src.infrastructure.database.models.base import S


async def get_telegram_schema_from_data(user: User) -> UserTelegramDataSchema:
    return UserTelegramDataSchema(
        telegram_id=str(user.id),
        username=user.username or "",
        first_name=user.first_name,
        last_name=user.last_name,
        auth_date=None
    )


def clean_characteristic_json(
        schema_instance: S | Type[S]
) -> dict[str, str]:
    """
    Возвращает словарь в формате:
    {
        "<field_name>": "<value> — <description>"
    }

    - Если передан экземпляр → использует реальные значения (None → "неизвестно")
    - Если передан класс схемы → все поля считаются "неизвестно"
    """
    exclude = {
        "id", "user_id", "created_at", "updated_at",
        "telegram_id", "records", "accuracy_percent", "GROUP"
    }

    if isinstance(schema_instance, type) and issubclass(schema_instance, BaseModel):
        # Случай: передан класс схемы → все поля неизвестны
        model = schema_instance
        data = {}
    else:
        # Случай: передан экземпляр
        model = schema_instance.__class__
        data = schema_instance.model_dump(exclude_none=False)

    result: dict[str, str] = {}

    for field_name, field_info in model.model_fields.items():
        if field_name in exclude:
            continue

        description = getattr(field_info, "description", "").strip()
        if not description:
            description = field_name.replace("_", " ").title()

        if isinstance(schema_instance, type):
            value = "неизвестно"
        else:
            value = data.get(field_name)
            if value is None:
                value = "неизвестно"

        result[field_name] = f"{value} — {description}"

    return result


def clean_characteristics_json(characteristics: dict[str, dict[str, Any]]) -> str:
    """очищает схемы для красивого запроса ассистенту"""
    text: str = ""

    for schema_name, characteristic in characteristics.items():
        # Заголовок схемы
        text += f"{schema_name}:\n"

        # поле: значение — описание
        for field_name, formatted_value in characteristic.items():
            text += f"{field_name}: {formatted_value}\n"
        text += "\n"

    text = text.rstrip()

    return text
