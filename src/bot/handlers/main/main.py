import random

from aiogram.types import Message, InlineKeyboardMarkup

from src.api.request_schemas.psycho import PsychoRequest
from src.api.request_schemas.research import ResearchDefaultRequest, ResearchSurveyRequest
from src.api.response_schemas.psycho import PsychoResponse
from src.api.response_schemas.research import ResearchSurveyResponse, \
    ResearchDefaultResponse
from src.bot.keyboards.inline.survey import get_survey_keyboard
from src.bot.lexicon.message_text import MessageText
from src.core.enums.user import TALKING_MODES
from src.core.schemas.user_schemas import UserSchema
from src.core.services.api_client.personalityGPT_api import PersonalityGPT_APIClient
from src.core.services.cache_services.cache_service import CacheService


async def main(
        message: Message,
        api_client: PersonalityGPT_APIClient,
        access_token: str,
        user: UserSchema,
        cache_service: CacheService
):
    """Главное действие пользователя

    — check_in:
    —— generation (with notification) / add to batches
    """

    # [ уведомляем пользователя об обработке сообщения ]
    if message.voice:
        message_reply = await message.reply(
            MessageText.get_process_voice()
        )
    else:
        message_reply = await message.reply(
            MessageText.get_process_message()
        )

    # [ выбор режима ]
    if user.talk_mode == TALKING_MODES.INDIVIDUAL_PSYCHO:
        await individual_psycho(
            message=message,
            api_client=api_client,
            access_token=access_token
        )
    elif user.talk_mode == TALKING_MODES.RESEARCH:
        await research_check_in(
            message=message,
            api_client=api_client,
            access_token=access_token,
            cache_service=cache_service
        )

    # [ удаляем сообщение об обработке ]  # TODO возможно удалять в функциях
    await message_reply.delete()


async def research_check_in(
        message: Message,
        api_client: PersonalityGPT_APIClient,
        access_token: str,
        cache_service: CacheService
) -> None:
    """режим познание:
    — DEFAULT: 60% - обычные вопросы
    — SURVEY: 40% - паки вопросов с клавиатурой
    — LONG: ..% - структурный ответ с просьбой прислать длинное голосовое сообщение
    """
    modes = ("default", "survey")
    numbers = [x for x in range(0, 10)]
    match random.choice(numbers):
        case x if x in range(0, 6):
            # [ RESEARCH: обычный режим ]
            await research_default(
                message=message,
                api_client=api_client,
                access_token=access_token
            )

        case x if x in range(6, 10):
            # [ RESEARCH: режим опроса ]
            await research_survey(
                message=message,
                api_client=api_client,
                access_token=access_token,
                cache_service=cache_service
            )

        case x if x in ...:  # FUTURE
            ...


async def research_default(
        message: Message,
        api_client: PersonalityGPT_APIClient,
        access_token: str
) -> None:
    """РЕЖИМ ПОЗНАНИЕ: DEFAULT"""
    request = ResearchDefaultRequest(
        user_message=message.text
    )

    response: ResearchDefaultResponse = await api_client.research_default_check_in(
        access_token=access_token,
        request=request
    )

    await message.reply(
        response.precise_question,
    )


async def research_survey(
        message: Message,
        api_client: PersonalityGPT_APIClient,
        access_token: str,
        cache_service: CacheService
) -> None:
    """РЕЖИМ ПОЗНАНИЕ: SURVEY"""
    request = ResearchSurveyRequest(
        user_message=message.text
    )

    response: ResearchSurveyResponse = await api_client.research_survey_check_in(
        request=request,
        access_token=access_token
    )

    keyboard: InlineKeyboardMarkup = await get_survey_keyboard(
        question_pack=response.question_pack,
        redis_service=cache_service.redis_service
    )

    answers: str = ""
    for i, answer in enumerate(response.question_pack.answer_packs, start=1):
        answers += f"{i}. {answer.answer}\n"

    text: str = MessageText.SURVEY_MESSAGE.format(
        user_answer=response.user_answer,
        question=response.question_pack.question,
        answers=answers
    )

    await message.reply(
        text=text,
        reply_markup=keyboard
    )


async def individual_psycho(
        message: Message,
        api_client: PersonalityGPT_APIClient,
        access_token: str
) -> None:
    """режим психолога"""
    api_request: PsychoRequest = PsychoRequest(
        message=message.text
    )

    response: PsychoResponse = await api_client.individual_psycho_check_in(
        access_token,
        api_request
    )
    await message.reply(response.user_answer)
