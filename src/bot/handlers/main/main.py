import logging

from aiogram.types import Message, InlineKeyboardMarkup

from src.api.request_schemas.check_in import CheckInRequest
from src.api.response_schemas.check_in import AssistantResponse
from src.bot.keyboards.inline.personality import get_about_mbti
from src.bot.keyboards.inline.survey import get_survey_keyboard
from src.bot.lexicon.message_text import MessageText
from src.core.schemas.user_schemas import UserSchema
from src.core.services.api_client.personalityGPT_api import PersonalityGPT_APIClient
from src.core.services.cache_services.cache_service import CacheService

logger = logging.getLogger(__name__)


async def main(
        message: Message,
        api_client: PersonalityGPT_APIClient,
        access_token: str,
        cache_service: CacheService,
        voice_text: str | None = None
):
    """
    Главное действие пользователя:
        — generation (with notification)
        — add to batches
    """

    user: UserSchema = await cache_service.get_user_profile(access_token, telegram_id=str(message.from_user.id))

    # [ уведомляем пользователя об обработке сообщения ]
    if message.voice:
        message_obj = await message.reply(
            MessageText.get_process_voice(gender=user.gender)
        )
    else:
        message_obj = await message.reply(
            MessageText.get_process_message(gender=user.gender)
        )

    user_text: str = message.text or voice_text

    # [ выбор режима ]
    response: AssistantResponse = await api_client.check_in(
        access_token,
        request=CheckInRequest(
            message=user_text,
            talk_mode_input=user.talk_mode
        )
    )

    if response.question_pack:
        await research_survey(
            message_obj=message_obj,
            response=response,
            cache_service=cache_service
        )
        return

    logger.info(f"ABOUT MBTI: {response.about_mbti}")

    text: str = response.user_answer
    if not user.passed_personality_core:
        text += "\n\n<i>после типирования шиза дневник будет отвечать лучше</i>"

    user: UserSchema = await cache_service.get_user_profile(
        access_token,
        str(message.from_user.id)
    )
    await message_obj.edit_text(
        text,
        reply_markup=get_about_mbti(
            passed_first_typification=user.passed_personality_core
        ) if response.about_mbti else None  # about mbti (можно потом дополнить другими клавами)
    )


async def research_survey(
        message_obj: Message,
        response: AssistantResponse,
        cache_service: CacheService
) -> None:
    """
    Ответ юзеру:
        — survey
    """
    keyboard: InlineKeyboardMarkup = await get_survey_keyboard(
        question_pack=response.question_pack,
        redis_service=cache_service.redis_service
    )

    answers: str = ""
    for i, answer in enumerate(response.question_pack.answer_packs, start=1):
        answers += f"{i}. {answer.answer}\n"

    text: str = MessageText.SURVEY_MESSAGE.format(
        question=response.question_pack.question,
        answers=answers
    )

    await message_obj.edit_text(
        text=text,
        reply_markup=keyboard
    )
