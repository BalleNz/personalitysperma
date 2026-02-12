from typing import Annotated

from fastapi import APIRouter, HTTPException, status
from fastapi.params import Depends

from src.api.utils.auth import get_auth_user
from src.core import consts
from src.core.schemas.user_schemas import UserSchema
from src.core.services.cache_services.redis_service import RedisService
from src.core.services.dependencies.redis_service_dep import get_redis_service
from src.core.services.dependencies.user_service_dep import get_user_service
from src.core.services.user_service import UserService

router = APIRouter(prefix="/user")


@router.get("/", response_model=UserSchema)
async def get_user_profile(
        user: Annotated[UserSchema, Depends(get_auth_user)],
):
    return user


@router.put("/increase_used_voices")
async def increase_used_voices(
        user: Annotated[UserSchema, Depends(get_auth_user)],
        user_service: Annotated[UserService, Depends(get_user_service)],
        redis_service: Annotated[RedisService, Depends(get_redis_service)],
):
    """Увеличивает количество используемых голосовых на 1 и инвалидирует кэш"""
    if not user.full_access and user.used_voice_messages > consts.FREE_VOICE_MESSAGES_COUNT:
        raise HTTPException(
            status_code=status.HTTP_402_PAYMENT_REQUIRED,
            detail="Лимит голосовых кончился"
        )

    await user_service.repo.increase_used_voice_message(user.id)
    await redis_service._invalidate_user_profile(user.telegram_id)
