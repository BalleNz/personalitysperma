from contextlib import asynccontextmanager
from typing import Any, AsyncGenerator

from sqlalchemy.ext.asyncio import AsyncSession

from src.core.services.assistant_service import AssistantService
from src.core.services.cache_services.redis_service import RedisService
from src.core.services.dependencies.assistant_service_dep import get_assistant_service
from src.core.services.dependencies.redis_service_dep import get_redis_service
from src.core.services.dependencies.telegram_service_dep import get_telegram_service
from src.core.services.telegram_service import TelegramService
from src.core.services.user_service import UserService
from src.infrastructure.database.engine import get_async_session
from src.infrastructure.database.repository.user_repo import UserRepository


class ServiceContainer:
    """Контейнер сервисов"""

    def __init__(self, session: AsyncSession):
        self.session = session
        self._assistant_service = None
        self._telegram_service = None
        self._redis_service = None

    @property
    async def assistant_service(self) -> AssistantService:
        if self._assistant_service is None:
            self._assistant_service = await get_assistant_service()
        return self._assistant_service

    @property
    async def telegram_service(self) -> TelegramService:
        if self._telegram_service is None:
            self._telegram_service = await get_telegram_service()
        return self._telegram_service

    @property
    async def redis_service(self) -> RedisService:
        if self._redis_service is None:
            self._redis_service = get_redis_service()
        return self._redis_service

    async def get_user_service(self) -> UserService:
        return UserService(repo=UserRepository(self.session))

    async def get_user_repo(self) -> UserRepository:
        return UserRepository(self.session)


@asynccontextmanager
async def get_session():
    """Правильное использование асинхронного генератора сессии"""
    session_gen = get_async_session()
    session = await session_gen.__anext__()
    try:
        yield session
    finally:
        try:
            await session_gen.__anext__()
        except StopAsyncIteration:
            pass


@asynccontextmanager
async def get_service_container() -> AsyncGenerator[ServiceContainer, Any]:
    """Контекстный менеджер для контейнера сервисов"""
    async with get_session() as session:
        yield ServiceContainer(session)
