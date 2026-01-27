from aiogram.types import User

from src.core.schemas.user_schemas import UserTelegramDataSchema


async def get_telegram_schema_from_data(user: User) -> UserTelegramDataSchema:
    return UserTelegramDataSchema(
        telegram_id=str(user.id),
        username=user.username or "",
        first_name=user.first_name,
        last_name=user.last_name,
        auth_date=None
    )
