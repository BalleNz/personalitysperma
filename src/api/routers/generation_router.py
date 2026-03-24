import logging
from typing import Annotated, Any, Type

from fastapi import APIRouter, Depends, Header, BackgroundTasks

from src.api.request_schemas.psycho import PsychoRequest
from src.api.request_schemas.research import ResearchSurveyFinishRequest, ResearchSurveyRequest, ResearchDefaultRequest
from src.api.response_schemas.characteristic import CheckInResponse, CharacteristicResponseRaw
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
from src.core.utils.funcs import clean_characteristic_json, clean_characteristics_json, \
    get_characteristics_raw_most_diff
from src.infrastructure.database.models.base import S
from src.infrastructure.database.repository.characteristic_repo import get_schema_type_from_name

router = APIRouter(prefix="/generation")
logger = logging.getLogger(__name__)


@router.post(path="/research/default", response_model=ResearchDefaultResponse)
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
    check_in_response: CheckInResponse = await assistant_service.get_check_in(request.user_message)
    user_characteristics: str | None = await get_critical_profiles_to_assistant(
        user=user,
        characteristics_name=check_in_response.characteristics_list,
        characteristic_service=characteristic_service
    )
    response: ResearchDefaultResponse = await assistant_service.get_research_default_response(
        user_message=request.user_message,
        user_characteristics=user_characteristics,
        user_id=user.id,
        redis_service=cache_service.redis_service
    )

    if response.classifications:
        # [ background ]
        access_token = authorization.split(" ")[1]
        background_tasks.add_task(
            process_generation_background,
            user=user,
            message=request.user_message,
            classifications=response.classifications,
            characteristic_service=characteristic_service,
            cache_service=cache_service,
            telegram_service=telegram_service,
            access_token=access_token,
            assistant_service=assistant_service
        )

    return response


@router.post(path="/research/survey", response_model=ResearchSurveyResponse)
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

    check_in_response: CheckInResponse = await assistant_service.get_check_in(request.user_message)
    user_characteristics: str | None = await get_critical_profiles_to_assistant(
        user=user,
        characteristics_name=check_in_response.characteristics_list,
        characteristic_service=characteristic_service
    )
    response: ResearchSurveyResponse = await assistant_service.get_research_survey_response(
        user_message=request.user_message,
        user_characteristics=user_characteristics,
        redis_service=cache_service.redis_service,
        user_id=user.id
    )

    # [ background ]
    access_token = authorization.split(" ")[1]
    background_tasks.add_task(
        process_generation_with_getting_psycho_response,
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
    """
    SURVEY:
    — завершить
    — ВСЕГДА обновить характеристики
    """

    # тут характеристики юзера не нужны — они будут в контексте
    response: PsychoResponse = await assistant_service.get_psycho_response(
        user_message=request.answer,
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

    check_in_response: CheckInResponse = await assistant_service.get_check_in(request.message)
    user_characteristics: str | None = await get_critical_profiles_to_assistant(
        user=user,
        characteristics_name=check_in_response.characteristics_list,
        characteristic_service=characteristic_service
    )
    response: PsychoResponse = await assistant_service.get_psycho_response(
        user_message=request.message,
        user_characteristics=user_characteristics or {},  # передаём профиль
        redis_service=cache_service.redis_service,
        user_id=user.id
    )

    background_tasks.add_task(
        process_generation_background,
        user=user,
        message=request.message,
        classifications=response.classifications,
        characteristic_service=characteristic_service,
        cache_service=cache_service,
        telegram_service=telegram_service,
        access_token=access_token,
        assistant_service=assistant_service
    )

    return response


async def get_critical_profiles_to_assistant(
        characteristic_service: CharacteristicService,
        characteristics_name: list[str],
        user: UserSchema
) -> str:
    """
    ВОЗВРАЩАЕТ ТЕКУЩИЕ ХАРАКТЕРИСТИКИ В ФОРМАТЕ:
    <field_name>: <value> — <description>
    """

    all_characteristics: list[CharacteristicResponseRaw] | None = await characteristic_service.repo.get_all_characteristics(
        user.id
    )

    # [ ПЕРЕДАЮТСЯ ВСЕГДА ]
    CRITICAL_SCHEMAS = {
        'HumorProfileSchema',
        'UserSocionicsSchema'
    }
    for characteristic_name in characteristics_name:
        CRITICAL_SCHEMAS.add(characteristic_name)  # [ уникальность соблюдается ]

    critical_characteristics: dict[str, dict[str, Any]] = {}
    if all_characteristics:
        all_characteristics_dict = {
            schema.type: schema.characteristics[0]
            for schema in all_characteristics
        }

        for schema_name in CRITICAL_SCHEMAS:
            if schema_name in all_characteristics_dict:
                schema_instance: S = all_characteristics_dict[schema_name]
                cleaned: dict = clean_characteristic_json(schema_instance)

                if cleaned:
                    critical_characteristics[schema_name] = cleaned

    text: str = clean_characteristics_json(critical_characteristics)
    return text


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


async def process_generation_with_getting_psycho_response(
        user: UserSchema,
        user_message: str,
        characteristic_service: CharacteristicService,
        cache_service: CacheService,
        telegram_service: TelegramService,
        assistant_service: AssistantService,
        access_token: str | None,
        background_tasks: BackgroundTasks,
) -> None:
    """Генерация характеристик (возможная) для SURVEY: CHECK IN"""
    response_for_back: PsychoResponse = await assistant_service.get_psycho_response(
        user_message=user_message,
        user_characteristics=None,
        user_id=user.id,
        redis_service=cache_service.redis_service
    )

    background_tasks.add_task(
        process_generation_background,
        user=user,
        message=user_message,
        classifications=response_for_back.classifications,
        characteristic_service=characteristic_service,
        cache_service=cache_service,
        telegram_service=telegram_service,
        access_token=access_token,
        assistant_service=assistant_service
    )


async def process_generation_background(
        user: UserSchema,
        message: str,
        classifications: list[str],
        characteristic_service: CharacteristicService,
        cache_service: CacheService,
        telegram_service: TelegramService,
        assistant_service: AssistantService,
        access_token: str | None,
):
    """
    смотрит
    — какие характеристики можно извлечь из сообщения юзера
    — последовательно генерирует их / добавляет в батч-очереди.
    """
    notification_was_send: bool = False

    for characteristic_name in classifications:
        try:
            schema_type: Type[S] | None = get_schema_type_from_name(characteristic_name)

            generated: bool = await characteristic_service.should_generate_characteristic(
                user_id=user.id,
                message_text=message,
                schema_type=schema_type,
                access_token=access_token,
                telegram_id=user.telegram_id,
                user_mode=user.talk_mode
            )

            if generated:
                await cache_service.redis_service.invalidate_characteristics(user.telegram_id)

                characteristics_raw: list[S] = await cache_service.get_characteristic_row(
                    access_token,
                    user.telegram_id,
                    characteristic_name=characteristic_name,
                )

                if notification_was_send:
                    continue

                if characteristic_name not in ["UserSocionicsSchema", "UserHollandCodesSchema", "UserHexacoSchema"]:
                    percent_diff, diff_type, field_name = get_characteristics_raw_most_diff(characteristics_raw)

                    message_text = await assistant_service.generate_telegram_message_characteristic_diff(
                        str(percent_diff) + diff_type + field_name
                    )
                    await telegram_service.send_message(
                        message=f"{message_text}",
                        user_telegram_id=user.telegram_id
                    )
                else:
                    await telegram_service.send_message(
                        message=f"<b>твой тип личности стал точнее з:</b>",
                        user_telegram_id=user.telegram_id
                    )

                notification_was_send = True

        except Exception as e:
            # Важно: логировать, но не падать — фоновая задача
            logger.exception(
                f"Ошибка обработки характеристики {characteristic_name} для пользователя {user.id}",
                extra={"error": str(e)}
            )
