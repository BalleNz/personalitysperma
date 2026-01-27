from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.services.dependencies.cache_service_dep import get_cache_service
from src.core.services.assistant_service import AssistantService
from src.core.services.characteristic_service import CharacteristicService
from src.core.services.dependencies.assistant_service_dep import get_assistant_service
from src.infrastructure.database.engine import get_async_session
from src.infrastructure.database.repository.characteristic_repo import CharacteristicRepository


async def get_characteristic_repo(
        session_generator: AsyncGenerator[AsyncSession, None] = Depends(get_async_session)
) -> CharacteristicRepository:
    cache_service = await get_cache_service()
    async with session_generator as session:
        return CharacteristicRepository(session, cache_service)


async def get_characteristic_service(
        repo: CharacteristicRepository = Depends(get_characteristic_repo),
        assistant_service: AssistantService = Depends(get_assistant_service),
) -> CharacteristicService:
    return CharacteristicService(
        repo=repo,
        assistant_service=assistant_service
    )
