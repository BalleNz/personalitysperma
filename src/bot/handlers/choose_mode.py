import io

from aiogram import Router, F
from aiogram.types import Message

from lexicon.button_text import ButtonText
from src.api.request_schemas.generation import CheckInRequest
from src.api.response_schemas.generation import CheckInResponse
from src.bot.bot_instance import bot
from src.bot.keyboards.inline import get_full_access_keyboard
from src.bot.lexicon.message_text import MessageText
from src.core.consts import FREE_VOICE_MESSAGES_COUNT
from src.core.schemas.user_schemas import UserSchema
from src.core.services.api_client.personalityGPT_api import PersonalityGPT_APIClient
from src.core.services.cache_services.cache_service import CacheService
from src.core.services.dependencies.speech_service_dep import get_speech_service
from src.core.services.speech_to_text_service import SpeechService

router = Router()


@router.message(F.text == ButtonText.CHOOSE_MODE)
async def main_voice(
        message: Message,
        api_client: PersonalityGPT_APIClient,
        access_token: str,
        cache_service: CacheService
):
    """ВЫБОР РЕЖИМА:
    1. Изучение себя
    2. Общение
    """
    MessageText.
    ...
