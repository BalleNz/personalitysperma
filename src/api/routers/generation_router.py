import logging
import random
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Header, BackgroundTasks

import prompts.check_in.learn
import src.core.prompts
from src.core.enums.user import TALKING_MODES
from src.core.services.assistant_service import AssistantService
from src.api.request_schemas.generation import CheckInRequest
from src.api.response_schemas.generation import CheckInResponse
from src.api.utils.auth import get_auth_user
from src.core.schemas.user_schemas import UserSchema
from src.core.services.cache_services.cache_service import CacheService
from src.core.services.characteristic_service import CharacteristicService
from src.core.services.dependencies.cache_service_dep import get_cache_service
from src.core.services.dependencies.assistant_service_dep import get_assistant_service
from src.core.services.dependencies.characteristic_service_dep import get_characteristic_service
from src.core.services.dependencies.telegram_service_dep import get_telegram_service
from src.core.services.dependencies.user_service_dep import get_user_service
from src.core.services.telegram_service import TelegramService
from src.core.services.user_service import UserService
from src.infrastructure.database.repository.characteristic_repo import get_schema_type_from_name

router = APIRouter(prefix="/generation")
logger = logging.getLogger(__name__)


@router.post(path="/check_in", response_model=CheckInResponse)
async def check_in(
        user: Annotated[UserSchema, Depends(get_auth_user)],
        characteristic_service: Annotated[CharacteristicService, Depends(get_characteristic_service)],
        request: CheckInRequest,
        telegram_service: Annotated[TelegramService, Depends(get_telegram_service)],
        cache_service: Annotated[CacheService, Depends(get_cache_service)],
        user_service: Annotated[UserService, Depends(get_user_service)],
        assistant_service: Annotated[AssistantService, Depends(get_assistant_service)],
        background_tasks: BackgroundTasks,
        authorization: Annotated[str | None, Header()] = None,  # get access token
):
    """смотрит
    — какие характеристики можно извлечь из сообщения юзера
    — последовательно генерирует их / добавляет в батч-очереди.
    """

    # [ создание лога ]
    await user_service.repo.create_log(
        user_id=user.id,
        log_text=request.message
    )

    critical_characteristics: dict[str, dict[str, Any]] = {}

    if user.talk_mode == TALKING_MODES.RESEARCH:
        """ПОЗНАНИЕ"""
        i: int = random.randint(0, 1)
        match i:
            case 0:
                """RESEARCH"""
                critical_characteristics = await get_characteristics(
                    characteristic_service,
                    user
                )
                prompt: str = prompts.check_in.learn.TO_LEARN
                check_in_response: CheckInResponse = await assistant_service.get_check_in_response(
                    user_message=request.message,
                    user_characteristics=critical_characteristics or {},  # передаём профиль
                    prompt=prompt
                )

            case 1:
                """SURVEY"""

                # TODO:
                #   1. TO_LEARN prompt (assistant service) (создать новую схему pydantic ToLearnResponse)
                #   2. bot frontend: юзер отвечает -> деграем ручку to_learn_finish:  (pydantic: ToLearnFinishRequest / Response)
                #       — Меняем характеристику
                #       — Уведомляем пользователя, что именно поменялось (сделать словарь key: characteristic_name; value: читабельное название)

    elif user.talk_mode == TALKING_MODES.INDIVIDUAL_PSYCHO:
        """Индивидуальный психолог"""

        access_token = authorization.split(" ")[1]

        critical_characteristics = await get_characteristics(
            characteristic_service,
            user
        )
        check_in_response: CheckInResponse = await characteristic_service.c

        background_tasks.add_task(
            process_check_in_background,
            user=user,
            message=request.message,
            classifications=check_in_response.classifications,
            characteristic_service=characteristic_service,
            cache_service=cache_service,
            telegram_service=telegram_service,
            access_token=access_token
        )

    return check_in_response
    # TODO: special_classifications


async def get_characteristics(
        characteristic_service: CharacteristicService,
        user: UserSchema
) -> dict[str, dict[str, Any]]:
    # [ самые важные профили для входных данных ]
    all_characteristics: list[dict] | None = await characteristic_service.repo.get_all_characteristics(
        user.id
    )

    CRITICAL_SCHEMAS = {
        "SocialProfileSchema",
        "CognitiveProfileSchema",
        "EmotionalProfileSchema",
        "BehavioralProfileSchema",
        'HumorProfileSchema',  # юмор — главный крючок
        'DarkTriadsSchema',  # нарциссизм, макиавеллизм — даём подыгрывание и лесть
        #  'UserHexacoSchema',  # экстраверсия / эмоциональность — задаём тон и энергию
        'UserSocionicsSchema',  # соционический тип — стиль общения, логика/этика и т.д.
    }

    critical_characteristics: dict[str, dict[str, Any]] = {}
    if all_characteristics:
        # преобразуем список в удобный словарь по имени типа
        char_dict = {
            item["type"]: item["characteristic"]
            for item in all_characteristics
        }

        for schema_name in CRITICAL_SCHEMAS:
            if schema_name in char_dict:
                schema_instance = char_dict[schema_name]

                data = schema_instance.model_dump(exclude_none=True)
                cleaned = {
                    k: v for k, v in data.items()
                    if k not in {
                        "id", "user_id", "created_at", "updated_at", "telegram_id", "records"
                    }
                }
                if cleaned:
                    critical_characteristics[schema_name] = cleaned
    return critical_characteristics


async def process_check_in_background(
        user: UserSchema,
        message: str,
        classifications: list[str],
        characteristic_service: CharacteristicService,
        cache_service: CacheService,
        telegram_service: TelegramService,
        access_token: str | None,
):
    for characteristic_name in classifications:
        try:
            schema_type = get_schema_type_from_name(characteristic_name)

            generated = await characteristic_service.should_generate_characteristic(
                user_id=user.id,
                message_text=message,
                schema_type=schema_type,
                access_token=access_token,
                telegram_id=user.telegram_id
            )

            if generated:
                await cache_service.redis_service._invalidate_characteristics(user.telegram_id)

                await telegram_service.send_message(
                    message=f"У вас появилась новая характеристика: {characteristic_name}!",
                    user_telegram_id=user.telegram_id
                )

        except Exception as e:
            # Важно: логировать, но не падать — фоновая задача
            logger.exception(
                f"Ошибка обработки характеристики {characteristic_name} для пользователя {user.id}",
                extra={"error": str(e)}
            )
