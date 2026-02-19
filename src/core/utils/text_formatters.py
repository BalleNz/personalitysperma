from datetime import datetime, date


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
