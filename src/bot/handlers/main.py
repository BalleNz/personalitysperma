import io

from aiogram import Router, F
from aiogram.types import Message

from src.api.request_schemas.generation import CheckInRequest
from src.api.response_schemas.generation import CheckInResponse
from src.bot.bot_instance import bot
from src.bot.keyboards.inline.start import get_full_access_keyboard
from src.bot.lexicon.message_text import MessageText
from src.core.consts import FREE_VOICE_MESSAGES_COUNT
from src.core.schemas.user_schemas import UserSchema
from src.core.services.api_client.personalityGPT_api import PersonalityGPT_APIClient
from src.core.services.cache_services.cache_service import CacheService
from src.core.services.dependencies.speech_service_dep import get_speech_service
from src.core.services.speech_to_text_service import SpeechService

router = Router()


@router.message(F.voice)
async def main_voice(
        message: Message,
        api_client: PersonalityGPT_APIClient,
        access_token: str,
        cache_service: CacheService
):
    """обработка голосового сообщения"""
    user_telegram_id: str = str(message.from_user.id)
    user: UserSchema = await cache_service.get_user_profile(access_token=access_token, telegram_id=user_telegram_id)

    if not user.full_access and user.used_voice_messages > FREE_VOICE_MESSAGES_COUNT:
        """закончился лимит голосовых, купить доступ"""
        keyboard = get_full_access_keyboard()
        await message.reply(MessageText.VOICE_LIMIT, reply_markup=keyboard)
        return

    await api_client.increase_used_voices(access_token)

    buffer = io.BytesIO()
    await bot.download(message.voice, destination=buffer)
    buffer.seek(0)

    message_reply = await message.reply(MessageText.VOICE_PROCESS)

    service: SpeechService = get_speech_service()
    text: str = await service.transcribe_bytes(buffer.getvalue())

    if not text:
        await message.reply(text or "Не удалось распознать речь")
        return

    api_request: CheckInRequest = CheckInRequest(
        message=text
    )

    check_in_response: CheckInResponse = await api_client.check_in(access_token, api_request)
    await message.reply(check_in_response.precise_question)
    await message_reply.delete()


@router.message()
async def main(
        message: Message,
        api_client: PersonalityGPT_APIClient,
        access_token: str
):
    """Главное действие пользователя:
    — check_in:
    —— generation (with notification) / add to batches"""

    message_reply = await message.reply("Ожидание ответа..")

    api_request: CheckInRequest = CheckInRequest(
        message=message.text
    )

    check_in_response: CheckInResponse = await api_client.check_in(access_token, api_request)
    await message.reply(check_in_response.precise_question)
    await message_reply.delete()
