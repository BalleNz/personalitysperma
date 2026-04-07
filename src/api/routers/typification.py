import logging
from typing import Annotated

from fastapi import APIRouter, Depends, HTTPException, Header

from src.api.request_schemas.typification import TypificationRequest, TypificationAssistantRequest, \
    TypificationGetQuestion, DeleteTypificationRequest, TypificationGetStatisticsRequest
from src.api.utils.auth import get_auth_user
from src.core.lexicon.typifications import TypificationPack
from src.core.prompts.typifications.get_next_question import GET_NEXT_QUESTION
from src.core.prompts.typifications.mid_stats import CAREER_HOLLAND_MID_PROMPT, NEURO_DIVERSITY_MID_PROMPT, \
    MOOD_ANXIETY_MID_PROMPT, LOOKS_DISORDERS_MID_PROMPT, PERSONALITY_CORE_MID_PROMPT
from src.core.schemas.user_schemas import UserSchema
from src.core.services.assistant_service import AssistantService
from src.core.services.characteristic_service import CharacteristicService
from src.core.services.dependencies.assistant_service_dep import get_assistant_service
from src.core.services.dependencies.characteristic_service_dep import get_characteristic_service
from src.core.services.dependencies.user_service_dep import get_user_service
from src.core.services.user_service import UserService

router = APIRouter(prefix="/typification")
logger = logging.getLogger(__name__)


async def delete_progress(
        typification_name: TypificationPack,
        user: Annotated[UserSchema, Depends(get_auth_user)],
        user_service: Annotated[UserService, Depends(get_user_service)],
):
    """Удалить прогресс типирования"""
    typification_to_field_name: dict = {
        TypificationPack.PERSONALITY_CORE: "passed_personality_core",
        TypificationPack.CAREER_HOLLAND: "passed_holland",
        TypificationPack.NEURO_DIVERSITY: "passed_neurodiversity",
        TypificationPack.MOOD_ANXIETY: "passed_mood_anxiety",
        TypificationPack.LOOKS_DISORDERS: "passed_body_image_eating",
        TypificationPack.SEX: "passed_sex_romance",
    }
    field_name: str = typification_to_field_name[typification_name]

    if field_name not in user.model_fields:
        raise HTTPException(
            status_code=500,
            detail=f"Ошибка конфигурации: поле {field_name} отсутствует в UserSchema"
        )
    update_data = {field_name: False}

    await user_service.repo.update(user.id, **update_data)


@router.get(path="/get_stats_on_middle_of_test")
async def get_stats_on_middle_of_test(
        request: TypificationGetStatisticsRequest,
        assistant_service: Annotated[AssistantService, Depends(get_assistant_service)],
        user: Annotated[UserSchema, Depends(get_auth_user)],
):
    """ВОЗВРАЩАЕТ ПРЕДВАРИТЕЛЬНУЮ СТАТИСТИКУ / ТИП ЛИЧНОСТИ НА СЕРЕДИНЕ ТЕСТА"""
    prompt: str = ""
    match request.typification_name:
        case TypificationPack.PERSONALITY_CORE:
            prompt = PERSONALITY_CORE_MID_PROMPT
        case TypificationPack.CAREER_HOLLAND:
            prompt = CAREER_HOLLAND_MID_PROMPT
        case TypificationPack.NEURO_DIVERSITY:
            prompt = NEURO_DIVERSITY_MID_PROMPT
        case TypificationPack.MOOD_ANXIETY:
            prompt = MOOD_ANXIETY_MID_PROMPT
        case TypificationPack.LOOKS_DISORDERS:
            prompt = LOOKS_DISORDERS_MID_PROMPT
        case TypificationPack.SEX:
            prompt = ...  # TODO

    if not prompt:
        return HTTPException(404, detail="не найден тип типификации")

    assistant_request = TypificationAssistantRequest(
        answers=request.answers,
        user_name=user.real_name
    )

    stats: str = await assistant_service.get_response(
        input_query=assistant_request.model_dump_json(),
        prompt=prompt
    )
    return stats


@router.get(path="/get_question")
async def get_question(
        request: TypificationGetQuestion,
        assistant_service: Annotated[AssistantService, Depends(get_assistant_service)]
):
    """Склеивает прошлый ответ с текущим вопросом"""
    return await assistant_service.get_response(
        input_query=request.model_dump_json(),
        prompt=GET_NEXT_QUESTION
    )


@router.post(path="/end_typification")
async def end_typification(
        request: TypificationRequest,
        characteristic_service: Annotated[CharacteristicService, Depends(get_characteristic_service)],
        user_service: Annotated[UserService, Depends(get_user_service)],
        user: Annotated[UserSchema, Depends(get_auth_user)],
        authorization: Annotated[str | None, Header()] = None
):
    """ЗАКАНЧИВАЕТ ТЕСТ И ЗАПИСЫВАЕТ НОВУЮ ХАРАКТЕРИСТИКУ / ХАРАКТЕРИСТИКИ"""

    # [ vars ]
    access_token = authorization.split(" ")[1]
    typification_name: TypificationPack = request.typification_name

    #  [ обнуляет факт пройденности ]
    await delete_progress(
        typification_name,
        user,
        user_service
    )

    # [ generation ]
    characteristics_to_generate: list[str] = request.characteristics
    for characteristic_name in characteristics_to_generate:
        await characteristic_service.typification_end(
            user.id,
            answers=request.answers,
            characteristic_name=characteristic_name,
            access_token=access_token,
            user_telegram_id=user.telegram_id
        )


@router.put(path="/delete_progress")
async def delete_progress_from_request(
        request: DeleteTypificationRequest,
        user: Annotated[UserSchema, Depends(get_auth_user)],
        user_service: Annotated[UserService, Depends(get_user_service)],
):
    await delete_progress(
        request.typification_name,
        user,
        user_service
    )
