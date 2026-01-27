from typing import Annotated

from fastapi import APIRouter, Depends, Header

from src.api.request_schemas.generation import CheckInRequest
from src.api.response_schemas.generation import CheckInResponse
from src.api.utils.auth import get_auth_user
from src.core.schemas.user_schemas import UserSchema
from src.core.services.characteristic_service import CharacteristicService
from src.core.services.dependencies.characteristic_service_dep import get_characteristic_service
from src.core.services.dependencies.telegram_service_dep import get_telegram_service
from src.core.services.telegram_service import TelegramService
from src.infrastructure.database.models.base import S
from src.infrastructure.database.repository.characteristic_repo import get_schema_type_from_name

router = APIRouter(prefix="/generation")


# TODO:
#   - обработка батча и получение характеристики (просмотр таблицы с пре-логами (пре-батчи) )

# TODO: ручка generate_characteristic
#   — user (from token)
#   — message
#   Что делает:
#       1) определяет какие таблицы обновить
#       2) characteristic_service.should_update в цикле в каждом полученном ответе из 1)
#       3) если ответ от 2) True: arq_worker: сообщение о создании новой характеристики

# TODO: ручка get_characteristic (в боте из кеш сервиса)
#   — получить характеристику по user_id и characteristic_model (__name__)

@router.post(path="/check_in", response_model=CheckInResponse)
async def check_in(
        user: Annotated[UserSchema, Depends(get_auth_user)],
        characteristic_service: Annotated[CharacteristicService, Depends(get_characteristic_service)],
        request: CheckInRequest,
        telegram_service: Annotated[TelegramService, Depends(get_telegram_service)],
        authorization: Annotated[str | None, Header()] = None,  # ← вот так
):
    """смотрит
    — какие характеристики можно извлечь из сообщения юзера
    — последовательно генерирует их / добавляет в батч-очереди.
    """

    check_in_response: CheckInResponse = await characteristic_service.check_in(
        request.message
    )

    # TODO: special_classifications

    access_token = authorization.split(" ")[1]

    for characteristic_name in check_in_response.classifications:
        """проходим по циклу таблиц, которые можно извлечь из текста"""
        schema_type: type[S] = get_schema_type_from_name(characteristic_name)
        is_generated: bool = await characteristic_service.should_generate_characteristic(
            user_id=user.id,
            message_text=request.message,
            schema_type=schema_type,
            access_token=access_token,
            telegram_id=user.telegram_id
        )

        if is_generated:
            await telegram_service.send_message(
                message=f"У вас появилось новая характеристика: {characteristic_name}!",
                user_telegram_id=user.telegram_id
            )

    return check_in_response
