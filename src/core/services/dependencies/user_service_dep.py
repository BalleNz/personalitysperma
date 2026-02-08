from typing import AsyncGenerator

from fastapi import Depends
from sqlalchemy.ext.asyncio import AsyncSession

from src.core.services.user_service import UserService
from src.infrastructure.database.engine import get_async_session
from src.infrastructure.database.repository.user_repo import UserRepository


async def get_user_repository(
        session_generator: AsyncGenerator[AsyncSession, None] = Depends(get_async_session)
) -> UserRepository:
    """
    :return: UserRepository obj with AsyncSession for onion service layer
    """
    async with session_generator as session:
        return UserRepository(session=session)


async def get_user_service(
        repo: UserRepository = Depends(get_user_repository)
) -> UserService:
    return UserService(repo=repo)
