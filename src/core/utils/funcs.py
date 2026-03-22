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


SOCIONICS_BANNED_FIELDS = {
    "ENTP", "ISFJ", "ESFJ", "INTP", "positivist", "process", "aristocratic", "merry", "yielding",
    "ENFJ", "ISTP", "ESTP", "INFJ", "ESFP", "INTJ", "ENTJ", "ISFP", "ENFP", "INFP", "ESTJ", "ISTJ",
    "primary_type", "quadra", "club", "extraversion", "intuition", "logic", "rationality", "static",
    "declaring", "constructivist", "careful", "farsighted", "judicious", "tactical", "questioning", "merging",
}


def clean_characteristic_json(
        schema_instance: S | Type[S],
        need_socionics_ban: bool = True
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
        "telegram_id", "accuracy_percent", "GROUP"
    }
    if need_socionics_ban:
        exclude.update(SOCIONICS_BANNED_FIELDS)

    if isinstance(schema_instance, type) and issubclass(schema_instance, BaseModel):
        # Случай: передан класс схемы → все поля неизвестны
        model = schema_instance
        data = {}
    else:
        # Случай: передан экземпляр
        model = schema_instance.__class__
        data = schema_instance.model_dump(exclude_none=False)

        # [ SOCIONICS ]
        if need_socionics_ban:
            if hasattr(schema_instance, 'top_3'):
                data['top_3'] = schema_instance.top_3
                data['top_2'] = schema_instance.top_2
                data['top_1'] = schema_instance.top_1
                data['records'] = schema_instance.records

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


def get_characteristics_raw_most_diff(characteristics_raw: list[S]) -> tuple[float, str, str] | None:
    """ВОЗВРАЩАЕТ
    —> (процент изменения, направление, название поля)

    Не работает для типов личности
    """
    if characteristics_raw and len(characteristics_raw) >= 2:
        # предполагаем, что список отсортирован по убыванию даты (новые первыми)
        latest = characteristics_raw[0]  # самая свежая
        previous = characteristics_raw[1]  # предыдущая

        max_diff = 0.0
        max_field = None
        max_direction = ""

        # Сравниваем только числовые поля (float / int)
        for field, value_now in latest.model_dump(exclude_none=False).items():
            if field in {"id", "user_id", "accuracy_percent", "created_at", "updated_at", "GROUP", "records"}:
                continue

            value_prev = getattr(previous, field, None)
            if not isinstance(value_now, (int, float)) or not isinstance(value_prev, (int, float)):
                continue

            diff = abs(value_now - value_prev)
            if diff > max_diff:
                max_diff = diff
                max_field = field
                if value_now > value_prev:
                    max_direction = "выросла"
                else:
                    max_direction = "снизилась"

        field_title, diff_percent = None, ""
        if max_diff > 0.05 and max_field:
            # форматируем красиво
            field_title = max_field.replace("_", " ").title()
            diff_percent = round(max_diff * 100, 1)
            return diff_percent, max_direction, field_title

        return None
