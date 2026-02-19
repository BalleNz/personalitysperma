import asyncio
import json
import logging  # noqa
from uuid import UUID

from aiogram import Dispatcher
from aiogram.fsm.storage.redis import RedisStorage

from src.bot.bot_instance import bot
from src.bot.handlers.main import router as main_router
from src.bot.handlers.start import router as start_router
from src.bot.handlers.characteristic_listing import router as characteristic_listing_router
from src.bot.handlers.choose_talking_mode import router as choose_mode_router
from src.bot.handlers.diary import router as diary_router
from src.bot.middlewares.depends_injectors import DependencyInjectionMiddleware
from src.core.services.dependencies.redis_service_dep import redis_client
from src.infrastructure.config.loggerConfig import configure_logging


def setup_auth(dp: Dispatcher):
    # Регистрация middleware
    dp.update.outer_middleware(DependencyInjectionMiddleware())

    # Регистрация хендлеров (порядок важен)
    for router in [
        start_router,
        characteristic_listing_router,
        choose_mode_router,
        diary_router,
        main_router,
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
dp = Dispatcher(storage=None)

if __name__ == "__main__":
    setup_auth(dp)
    configure_logging()
    logging.basicConfig(
        level=logging.INFO,
        format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
    )
    asyncio.run(start_polling(dp))
