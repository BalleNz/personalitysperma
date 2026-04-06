import logging
from typing import Annotated, Any, Type

from fastapi import APIRouter, Depends, Header, BackgroundTasks, HTTPException
from starlette import status

from src.api.request_schemas.check_in import CheckInRequest
from src.api.request_schemas.survey import ResearchSurveyFinishRequest
from src.api.response_schemas.characteristic import CharacteristicResponseRaw
from src.api.response_schemas.check_in import CheckInResponse, AssistantResponse
from src.api.response_schemas.survey import ResearchSurveyFinishResponse
from src.api.utils.auth import get_auth_user
from src.core.enums.user import GENDER, TALKING_MODES_CHECK_IN, TALKING_MODES
from src.core.lexicon.instructions_prompt import get_dark_triads_instruction, get_humor_profile_instruction, MBTI_PROMPT
from src.core.prompts.generation.survey import SURVEY_PROMPT, TO_LEARN_SURVEY_FINISH
from src.core.prompts.main.long import LONG_PROMPT
from src.core.prompts.main.psycho import PSYCHO_PROMPT
from src.core.prompts.main.research import RESEARCH_DEFAULT_PROMPT
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

router = APIRouter(prefix="/main")
logger = logging.getLogger(__name__)


@router.post(path="/check_in", response_model=AssistantResponse)
async def check_in(
        user: Annotated[UserSchema, Depends(get_auth_user)],
        characteristic_service: Annotated[CharacteristicService, Depends(get_characteristic_service)],
        request: CheckInRequest,
        assistant_service: Annotated[AssistantService, Depends(get_assistant_service)],
        cache_service: Annotated[CacheService, Depends(get_cache_service)],
        user_service: Annotated[UserService, Depends(get_user_service)],
        background_tasks: BackgroundTasks,
        telegram_service: Annotated[TelegramService, Depends(get_telegram_service)],
        authorization: Annotated[str | None, Header()] = None
):
    """CHECK_IN"""
    await user_service.repo.create_log(
        user_id=user.id,
        log_text=request.message
    )

    check_in_response: CheckInResponse = await assistant_service.get_check_in(
        request.message
    )
    logger.info(f"выбранный режим {user.telegram_id}: {check_in_response.talk_mode}")

    all_chars: list[CharacteristicResponseRaw] | None = await characteristic_service.repo.get_all_characteristics(
        user.id
    )
    critical_profiles, mbti_prompt = await get_critical_profiles_to_assistant(
        all_chars=all_chars,
        characteristics_name=check_in_response.characteristics_list,
        real_name=user.real_name,
        gender=user.gender
    )

    prompt: str = ""
    match check_in_response.talk_mode:
        case TALKING_MODES_CHECK_IN.RESEARCH:
            prompt = mbti_prompt + RESEARCH_DEFAULT_PROMPT
        case TALKING_MODES_CHECK_IN.SURVEY:
            prompt = mbti_prompt + SURVEY_PROMPT
        case TALKING_MODES_CHECK_IN.INDIVIDUAL_PSYCHO:
            prompt = mbti_prompt + PSYCHO_PROMPT
        case TALKING_MODES_CHECK_IN.LONG:
            prompt = mbti_prompt + LONG_PROMPT

    response: AssistantResponse | None = await assistant_service.get_shiza_response(
        user_message=request.message,
        user_id=user.id,
        prompt=prompt,
        redis_service=cache_service.redis_service,
        user_profile=critical_profiles
    )
    response.about_mbti = check_in_response.about_mbti

    if not response:
        raise HTTPException(
            status_code=status.HTTP_404_NOT_FOUND,
            detail=f"Ошибка в ручке check_in: response from assistant not found"
        )

    if response.classifications:
        # [ background ]
        access_token = authorization.split(" ")[1]
        background_tasks.add_task(
            process_generation_background,
            user=user,
            message=request.message,
            classifications=response.classifications,
            characteristic_service=characteristic_service,
            cache_service=cache_service,
            telegram_service=telegram_service,
            access_token=access_token,
            assistant_service=assistant_service,
            talk_mode=user.talk_mode,
            user_service=user_service
        )

    return response


@router.post(path="/research/survey/finish", response_model=AssistantResponse)
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
    response: AssistantResponse = await assistant_service.get_shiza_response(
        user_message=request.answer,
        redis_service=redis_service,
        user_id=user.id,
        prompt=PSYCHO_PROMPT
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


async def get_critical_profiles_to_assistant(
        all_chars: list[CharacteristicResponseRaw],
        characteristics_name: list[str],
        real_name: str | None = None,
        gender: GENDER | None = None
) -> tuple[str, str]:
    """
        Возвращает:
        - text: форматированные характеристики (cleaned)
        - mbti_prompt: строка с "О пользователе:" + стиль общения (MBTI + Humor + DarkTriads)
        """

    critical_schemas = {
        'MBTISchema', 'HumorProfileSchema', 'DarkTriadsSchema'
    }
    for name in characteristics_name:
        critical_schemas.add(name)

    critical_characteristics: dict[str, dict[str, Any]] = {}
    prompt_parts: list[str] = []

    if not all_chars:
        return "", ""

    all_chars_dict = {
        schema.type: schema.characteristics[0]
        for schema in all_chars
    }

    # [ ОПИСАНИЕ ЮЗЕРА ]
    # TODO: вынести в отдельную функцию get_prompt_parts(dark_triads, humor_profile, real_name, gender)
    if "MBTISchema" in all_chars_dict:
        schema_instance = all_chars_dict["MBTISchema"]

        prompt_parts.append("О пользователе:\n")
        prompt_parts.append(MBTI_PROMPT[schema_instance.primary_type])

        if real_name:
            prompt_parts.append(f"Пользователя зовут: {real_name}")

        if gender:
            # TODO: get_gender_text(gender)
            ...

    # [ стиль общения ]
    style_instructions: list[str] = []
    if "HumorProfileSchema" in all_chars_dict:
        humor_text = get_humor_profile_instruction(all_chars_dict["HumorProfileSchema"])
        if humor_text:
            style_instructions.append(humor_text)
    if "DarkTriadsSchema" in all_chars_dict:
        dark_text = get_dark_triads_instruction(all_chars_dict["DarkTriadsSchema"])
        if dark_text:
            style_instructions.append(dark_text)
    if style_instructions:
        prompt_parts.append("\nКак нужно разговаривать с пользователем:\n")
        prompt_parts.extend(style_instructions)

    for schema_name in critical_schemas:
        if schema_name in all_chars_dict and schema_name not in ["MBTISchema", "HumorProfileSchema",
                                                                 "DarkTriadsSchema"]:
            schema_instance = all_chars_dict[schema_name]
            cleaned = clean_characteristic_json(schema_instance, generate=False)
            if cleaned:
                critical_characteristics[schema_name] = cleaned

    text: str = clean_characteristics_json(critical_characteristics)

    mbti_prompt = "".join(prompt_parts).strip()
    return text, mbti_prompt


async def process_survey_finish_in_background(
        user: UserSchema,
        request: ResearchSurveyFinishRequest,
        characteristic_service: CharacteristicService,
        assistant_service: AssistantService,
        redis_service: RedisService,
        telegram_service: TelegramService
):
    """SURVEY: FINISH"""
    survey_finish_response: ResearchSurveyFinishResponse = await assistant_service.get_shiza_response(
        user_message=request.model_dump_json(),
        user_id=user.id,
        redis_service=redis_service,
        prompt=TO_LEARN_SURVEY_FINISH,
        pydantic_model=ResearchSurveyFinishResponse
    )

    await characteristic_service.research_survey_finish(
        user_id=user.id,
        telegram_id=user.telegram_id,
        new_characteristics=survey_finish_response.new_characteristics
    )

    #  Уведомляем пользователя, что именно поменялось (сделать словарь key: characteristic_name; value: читабельное название)
    # await telegram_service.


async def process_generation_background(
        user: UserSchema,
        message: str,
        classifications: list[str],
        characteristic_service: CharacteristicService,
        cache_service: CacheService,
        telegram_service: TelegramService,
        assistant_service: AssistantService,
        access_token: str | None,
        talk_mode: TALKING_MODES,
        user_service: UserService | None
):
    """
    смотрит
    — какие характеристики можно извлечь из сообщения юзера
    — последовательно генерирует их / добавляет в батч-очереди.
    """
    notification_was_send: bool = False

    for characteristic_name in classifications:
        if characteristic_name == "ChangeName":
            # [ смена имени юзера ]
            history: list[dict] = await cache_service.redis_service.get_history(
                user_id=user.id,
                max_messages=5
            )
            history_str: str = "".join([message["content"] for message in history])

            new_name: str = await assistant_service.extract_user_name(message + history_str)
            await user_service.repo.update(user.id, real_name=new_name)
            await cache_service.redis_service.invalidate_user_profile(user.telegram_id)

            continue

        try:
            schema_type: Type[S] | None = get_schema_type_from_name(characteristic_name)

            generated: bool = await characteristic_service.should_generate_characteristic(
                user_id=user.id,
                message_text=message,
                schema_type=schema_type,
                access_token=access_token,
                telegram_id=user.telegram_id,
                talk_mode=talk_mode
            )

            if generated:
                await cache_service.redis_service.invalidate_characteristics(user.telegram_id)

                characteristics_raw: list[S] = await cache_service.get_characteristic_row(
                    access_token,
                    user.telegram_id,
                    characteristic_name=characteristic_name,
                )

                if notification_was_send:  # [ только одно уведомление за цикл ]
                    continue

                if characteristic_name not in ["MBTISchema", "HollandCodesSchema", "HexacoSchema"]:
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
