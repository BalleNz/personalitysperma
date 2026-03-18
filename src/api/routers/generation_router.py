import json
import logging
from typing import Annotated, Any

from fastapi import APIRouter, Depends, Header, BackgroundTasks

from src.api.request_schemas.psycho import PsychoRequest
from src.api.request_schemas.research import ResearchSurveyFinishRequest, ResearchSurveyRequest, ResearchDefaultRequest
from src.api.response_schemas.characteristic import CharacteristicResponseRaw
from src.api.response_schemas.psycho import PsychoResponse
from src.api.response_schemas.research import ResearchSurveyFinishResponse, ResearchSurveyResponse, \
    ResearchDefaultResponse
from src.api.utils.auth import get_auth_user
from src.core.schemas.user_schemas import UserSchema
from src.core.services.assistant_service import AssistantService
from src.core.services.cache_services.cache_service import CacheService
from src.core.services.cache_services.redis_service import RedisService
from src.core.services.characteristic_service import CharacteristicService
from src.core.services.dependencies.assistant_service_dep import get_assistant_service
from src.core.services.dependencies.cache_service_dep import get_cache_service
from src.core.services.dependencies.characteristic_service_dep import get_characteristic_service
from src.core.services.dependencies.redis_service_dep import get_redis_service
from src.core.services.dependencies.telegram_service_dep import get_telegram_service
from src.core.services.dependencies.user_service_dep import get_user_service
from src.core.services.telegram_service import TelegramService
from src.core.services.user_service import UserService
from src.infrastructure.database.repository.characteristic_repo import get_schema_type_from_name

router = APIRouter(prefix="/generation")
logger = logging.getLogger(__name__)


@router.post(path="/research/default/check_in", response_model=ResearchDefaultResponse)
async def research_default_check_in(
        user: Annotated[UserSchema, Depends(get_auth_user)],
        characteristic_service: Annotated[CharacteristicService, Depends(get_characteristic_service)],
        request: ResearchDefaultRequest,
        assistant_service: Annotated[AssistantService, Depends(get_assistant_service)],
        cache_service: Annotated[CacheService, Depends(get_cache_service)],
        user_service: Annotated[UserService, Depends(get_user_service)],
        background_tasks: BackgroundTasks,
        telegram_service: Annotated[TelegramService, Depends(get_telegram_service)],
        authorization: Annotated[str | None, Header()] = None
):
    """РЕЖИМ ПОЗНАНИЕ: DEFAULT"""
    await user_service.repo.create_log(
        user_id=user.id,
        log_text=request.user_message
    )

    # [ assistant ]
    critical_characteristics = await get_characteristics_json_to_assistant(
        characteristic_service,
        user
    )
    response: ResearchDefaultResponse = await assistant_service.get_research_default_response(
        user_message=request.user_message,
        user_characteristics=critical_characteristics or {},
        user_id=user.id,
        redis_service=cache_service.redis_service
    )

    if response.classifications:
        # [ background ]
        access_token = authorization.split(" ")[1]
        background_tasks.add_task(
            process_check_in_background,
            user=user,
            message=request.user_message,
            classifications=response.classifications,
            characteristic_service=characteristic_service,
            cache_service=cache_service,
            telegram_service=telegram_service,
            access_token=access_token
        )

    return response


@router.post(path="/research/survey/check_in", response_model=ResearchSurveyResponse)
async def research_survey_check_in(
        request: ResearchSurveyRequest,
        user: Annotated[UserSchema, Depends(get_auth_user)],
        assistant_service: Annotated[AssistantService, Depends(get_assistant_service)],
        cache_service: Annotated[CacheService, Depends(get_cache_service)],
        user_service: Annotated[UserService, Depends(get_user_service)],
        background_tasks: BackgroundTasks,
        telegram_service: Annotated[TelegramService, Depends(get_telegram_service)],
        characteristic_service: Annotated[CharacteristicService, Depends(get_characteristic_service)],
        authorization: Annotated[str | None, Header()] = None,  # get access token
):
    """РЕЖИМ ПОЗНАНИЕ: SURVEY"""
    await user_service.repo.create_log(
        user_id=user.id,
        log_text=request.user_message
    )

    characteristics = await get_characteristics_json_to_assistant(
        characteristic_service, user
    )

    response: ResearchSurveyResponse = await assistant_service.get_research_survey_response(
        user_message=request.user_message,
        redis_service=cache_service.redis_service,
        user_id=user.id
    )

    # [ background ]
    access_token = authorization.split(" ")[1]
    background_tasks.add_task(
        process_check_in_with_getting_psycho_response,
        user=user,
        user_message=request.user_message,
        characteristic_service=characteristic_service,
        cache_service=cache_service,
        telegram_service=telegram_service,
        access_token=access_token,
        assistant_service=assistant_service,
        background_tasks=background_tasks
    )

    return response


@router.post(path="/research/survey/finish", response_model=PsychoResponse)
async def research_survey_finish(
        request: ResearchSurveyFinishRequest,
        user: Annotated[UserSchema, Depends(get_auth_user)],
        assistant_service: Annotated[AssistantService, Depends(get_assistant_service)],
        characteristic_service: Annotated[CharacteristicService, Depends(get_characteristic_service)],
        telegram_service: Annotated[TelegramService, Depends(get_telegram_service)],
        redis_service: Annotated[RedisService, Depends(get_redis_service)],
        background_tasks: BackgroundTasks,
):
    """SURVEY: завершить и обновить характеристики"""
    characteristics = await get_characteristics_json_to_assistant(
        user=user,
        characteristic_service=characteristic_service
    )
    response: PsychoResponse = await assistant_service.get_psycho_response(
        user_message=request.answer,
        user_characteristics=characteristics,
        redis_service=redis_service,
        user_id=user.id
    )

    background_tasks.add_task(
        process_survey_finish_in_background,
        user=user,
        characteristic_service=characteristic_service,
        request=request,
        telegram_service=telegram_service,
        assistant_service=assistant_service,
        redis_service=redis_service
    )

    return response


@router.post(path="/individual_psycho", response_model=PsychoResponse)
async def psycho(
        user: Annotated[UserSchema, Depends(get_auth_user)],
        characteristic_service: Annotated[CharacteristicService, Depends(get_characteristic_service)],
        request: PsychoRequest,
        telegram_service: Annotated[TelegramService, Depends(get_telegram_service)],
        cache_service: Annotated[CacheService, Depends(get_cache_service)],
        user_service: Annotated[UserService, Depends(get_user_service)],
        assistant_service: Annotated[AssistantService, Depends(get_assistant_service)],
        background_tasks: BackgroundTasks,
        authorization: Annotated[str | None, Header()] = None,  # get access token
):
    """ИНДИВИДУАЛЬНЫЙ ПСИХОЛОГ"""

    # [ создание лога ]
    await user_service.repo.create_log(
        user_id=user.id,
        log_text=request.message
    )

    access_token = authorization.split(" ")[1]

    critical_characteristics = await get_characteristics_json_to_assistant(
        characteristic_service,
        user
    )

    response: PsychoResponse = await assistant_service.get_psycho_response(
        user_message=request.message,
        user_characteristics=critical_characteristics or {},  # передаём профиль
        redis_service=cache_service.redis_service,
        user_id=user.id
    )

    background_tasks.add_task(
        process_check_in_background,
        user=user,
        message=request.message,
        classifications=response.classifications,
        characteristic_service=characteristic_service,
        cache_service=cache_service,
        telegram_service=telegram_service,
        access_token=access_token
    )

    return response


async def get_characteristics_json_to_assistant(
        characteristic_service: CharacteristicService,
        user: UserSchema
) -> str:
    """
    ВОЗВРАЩАЕТ В ФОРМАТЕ:
    <field_name>: <value> — <description>
    """

    all_characteristics: list[CharacteristicResponseRaw] | None = await characteristic_service.repo.get_all_characteristics(
        user.id
    )

    # [ самые важные профили для входных данных ]
    CRITICAL_SCHEMAS = {
        "SocialProfileSchema",
        "CognitiveProfileSchema",
        "EmotionalProfileSchema",
        "BehavioralProfileSchema",
        'HumorProfileSchema',  # юмор — главный крючок
        'DarkTriadsSchema',  # нарциссизм, макиавеллизм — даём подыгрывание и лесть
        #  'UserHexacoSchema', # экстраверсия / эмоциональность — задаём тон и энергию
        'UserSocionicsSchema',  # соционический тип — стиль общения, логика/этика и т.д.
    }

    critical_characteristics: dict[str, dict[str, Any]] = {}
    if all_characteristics:
        # преобразуем список в удобный словарь по имени типа
        char_dict = {
            schema.type: schema.characteristics[0]
            for schema in all_characteristics
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
                for field_name, value in cleaned.items():
                    field_info = schema_instance.model_fields.get(field_name)
                    description = getattr(field_info, "description", "").strip()
                    if not description:
                        # запасной вариант — human-readable название поля
                        description = field_name.replace("_", " ").title()

                    key = field_name
                    value_str = f"{value} — {description}"

                    cleaned[key] = value_str

                if cleaned:
                    critical_characteristics[schema_name] = cleaned
    return json.dumps(critical_characteristics, ensure_ascii=False, indent=2)


async def process_survey_finish_in_background(
        user: UserSchema,
        request: ResearchSurveyFinishRequest,
        characteristic_service: CharacteristicService,
        assistant_service: AssistantService,
        redis_service: RedisService,
        telegram_service: TelegramService
):
    """SURVEY: FINISH"""
    survey_finish_response: ResearchSurveyFinishResponse = await assistant_service.get_to_learn_survey_finish_response(
        request=request,
        user_id=user.id,
        redis_service=redis_service
    )

    await characteristic_service.research_survey_finish(
        user_id=user.id,
        telegram_id=user.telegram_id,
        new_characteristics=survey_finish_response.new_characteristics
    )

    #  Уведомляем пользователя, что именно поменялось (сделать словарь key: characteristic_name; value: читабельное название)
    # await telegram_service.


async def process_check_in_with_getting_psycho_response(
        user: UserSchema,
        user_message: str,
        characteristic_service: CharacteristicService,
        cache_service: CacheService,
        telegram_service: TelegramService,
        assistant_service: AssistantService,
        access_token: str | None,
        background_tasks: BackgroundTasks,
) -> None:
    response_for_back: PsychoResponse = await assistant_service.get_psycho_response(
        user_message=user_message,
        user_characteristics={},  # передаём профиль
        user_id=user.id,
        redis_service=cache_service.redis_service
    )

    background_tasks.add_task(
        process_check_in_background,
        user=user,
        message=user_message,
        classifications=response_for_back.classifications,
        characteristic_service=characteristic_service,
        cache_service=cache_service,
        telegram_service=telegram_service,
        access_token=access_token
    )


async def process_check_in_background(
        user: UserSchema,
        message: str,
        classifications: list[str],
        characteristic_service: CharacteristicService,
        cache_service: CacheService,
        telegram_service: TelegramService,
        access_token: str | None,
):
    """
    смотрит
    — какие характеристики можно извлечь из сообщения юзера
    — последовательно генерирует их / добавляет в батч-очереди.
    """

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

                # TODO: сделать более красивое сообщение (возможно, структурное.)
                #   — Ваша "Любознательность" увеличивась на 30%
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
