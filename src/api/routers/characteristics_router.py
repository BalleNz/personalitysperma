from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.response_schemas.characteristic import GetAllCharacteristicResponse
from src.api.utils.auth import get_auth_user
from src.core.schemas.user_schemas import UserSchema
from src.core.services.characteristic_service import CharacteristicService
from src.core.services.dependencies.characteristic_service_dep import get_characteristic_service

router = APIRouter(prefix="/characteristic")


@router.get(path="/", response_model=GetAllCharacteristicResponse)
async def get_all_characteristics(
        user: Annotated[UserSchema, Depends(get_auth_user)],
        characteristic_service: Annotated[CharacteristicService, Depends(get_characteristic_service)]
):
    """Получает все схемы характеристик"""
    characteristics_info = await characteristic_service.repo.get_all_characteristics(user.id)
    return {
        "response": characteristics_info
    }
