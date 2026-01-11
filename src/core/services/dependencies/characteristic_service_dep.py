from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from core.services.characteristic_service import CharacteristicService
from infrastructure.database.engine import get_async_session
from infrastructure.database.repository.characteristic_repo import CharacteristicRepository


async def get_characteristic_repo(
        session_generator: AsyncGenerator[AsyncSession, None] = Depends(get_async_session)
) -> CharacteristicRepository:
    async with session_generator as session:
        return CharacteristicRepository(session)


async def get_characteristic_service(
        repo: CharacteristicRepository = Depends(get_characteristic_repo)
) -> CharacteristicService:
    return CharacteristicService(
        repo=repo
    )
