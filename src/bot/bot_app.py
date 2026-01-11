import asyncio
import json
from uuid import UUID

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage
from bot.handlers.start import router as start_router
from bot.bot_instance import bot
from config.loggerConfig import configure_logging
from core.services.dependencies.redis_service_dep import redis_client


def setup_auth(dp: Dispatcher):
    # Регистрация middleware

    # Регистрация хендлеров (порядок важен)
    for router in [
        start_router
    ]:
        dp.include_router(router)


async def start_polling(dp: Dispatcher):
    await dp.start_polling(bot)


class UUIDEncoder(json.JSONEncoder):
    def default(self, obj):
        if isinstance(obj, UUID):
            return str(obj)
        return super().default(obj)


storage = RedisStorage(
    redis_client,
    state_ttl=60 * 60 * 6,  # 6 часов
    json_dumps=lambda obj: json.dumps(obj, cls=UUIDEncoder),
    json_loads=json.loads
)
# dp = Dispatcher(storage=storage)
dp = Dispatcher(storage=None)

if __name__ == "__main__":
    setup_auth(dp)
    configure_logging()
    asyncio.run(start_polling(dp))
