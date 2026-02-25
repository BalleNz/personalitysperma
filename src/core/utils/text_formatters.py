import datetime
from datetime import datetime, date
from typing import Optional

from database.models.base import S
from schemas.clinical_disorders.anxiety_disorders import AnxietyDisordersSchema
from schemas.clinical_disorders.mood_disorders import MoodDisordersSchema
from schemas.clinical_disorders.neuro_disorders import NeuroDisordersSchema
from schemas.clinical_disorders.personality_disorders import PersonalityDisordersSchema
from schemas.personality_types.hexaco import UserHexacoSchema
from schemas.personality_types.holland_codes import UserHollandCodesSchema
from schemas.personality_types.socionics_type import UserSocionicsSchema
from schemas.traits.traits_basic import SocialProfileSchema, CognitiveProfileSchema, EmotionalProfileSchema, \
    BehavioralProfileSchema
from schemas.traits.traits_dark import DarkTriadsSchema
from schemas.traits.traits_humor import HumorProfileSchema


def format_russian_date(dt: datetime | date) -> str:
    """
    Преобразует дату в красивый русский формат: "19 ноября", "1 мая", "31 декабря"

    Примеры:
        datetime(2025, 11, 19) → "19 ноября"
        date(2024, 5, 1)       → "1 мая"
        datetime(2026, 2, 9)   → "9 февраля"
    """
    if isinstance(dt, datetime):
        day = dt.day
        month = dt.month
    else:
        day = dt.day
        month = dt.month

    months = [
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря"
    ]

    month_name = months[month - 1]
    return f"{day} {month_name}"


def get_last_update(date: Optional[datetime.datetime]) -> str:
    """Последнее обновление в строчном виде (вчера, неделю назад, ...)"""
    if date is None:
        return "N/A"

    now = datetime.datetime.now(datetime.timezone.utc)
    delta = now - date

    if delta.days == 0:
        return "сегодня"
    if delta.days == 1:
        return "вчера"
    if 2 <= delta.days <= 6:
        return f"{delta.days} дня назад"
    if 7 <= delta.days <= 13:
        return "неделю назад"
    if 14 <= delta.days <= 29:
        return "больше недели назад"
    if delta.days >= 30:
        return "больше месяца назад"
    return "N/A"


def get_characteristic_name(schema_name: type[S]):
    """
    Возвращает человеко-ориентированное название характеристики/профиля
    """
    names = {
        SocialProfileSchema: "Социальность",
        CognitiveProfileSchema: "Мышление",
        EmotionalProfileSchema: "Эмоциональность",
        BehavioralProfileSchema: "Поведение",
        DarkTriadsSchema: "Тёмная триада",
        HumorProfileSchema: "Чувство юмора",
        MoodDisordersSchema: "Настроение",
        AnxietyDisordersSchema: "Тревожность",
        NeuroDisordersSchema: "Нейрокогнитивные нарушения",
        PersonalityDisordersSchema: "Личностные расстройства",
        UserHexacoSchema: "HEXACO",
        UserHollandCodesSchema: "Коды Холланда",
        UserSocionicsSchema: "Соционический тип",
    }
    return names[schema_name]

    # RelationshipPreferenceSchema
    # LoveLanguageSchema
    # SexualPreferenceSchema


def get_date_word_from_iso(date: datetime.datetime | datetime.date | str | None) -> str:
    """
    Возвращает дату на русском языке
    Примеры:
        datetime(..) → "4 марта"
    """
    if isinstance(date, datetime.datetime):
        date = date.date()

    day = date.day
    month_names = [
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря"
    ]

    month = month_names[date.month - 1]

    return f"{day} {month}"
