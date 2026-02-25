from aiogram import Router, F
from aiogram.types import Message, ReplyKeyboardMarkup

from src.bot.keyboards.reply import MAIN_KEYBOARD_PSYCHO, MAIN_KEYBOARD_RESEARCH
from src.bot.lexicon.button_text import ButtonText
from src.bot.lexicon.message_text import MessageText
from src.core.enums.user import TALKING_MODES
from src.core.schemas.user_schemas import UserSchema
from src.core.services.api_client.personalityGPT_api import PersonalityGPT_APIClient
from src.core.services.cache_services.cache_service import CacheService

router = Router()


@router.message(F.text.in_([ButtonText.PSYCHO_MODE, ButtonText.RESEARCH_MODE]))
async def select_mode_from_reply(
        message: Message,
        access_token: str,
        cache_service: CacheService,
        api_client: PersonalityGPT_APIClient
):
    """ВЫБОР РЕЖИМА
    1. Изучение себя
    2. Общение
    """

    talk_mode: TALKING_MODES = TALKING_MODES.RESEARCH
    if message.text == ButtonText.PSYCHO_MODE:
        talk_mode = TALKING_MODES.INDIVIDUAL_PSYCHO
    elif message.text == ButtonText.RESEARCH_MODE:
        talk_mode = TALKING_MODES.RESEARCH

    user: UserSchema = await cache_service.get_user_profile(
        access_token,
        str(message.from_user.id)
    )
    text: str = MessageText.choose_talking_mode(talk_mode)

    await api_client.change_talk_mode(
        access_token,
        talk_mode=talk_mode
    )

    reply_keyboard: ReplyKeyboardMarkup = MAIN_KEYBOARD_PSYCHO if talk_mode == TALKING_MODES.RESEARCH else MAIN_KEYBOARD_RESEARCH

    await message.reply(
            text,
            reply_markup=reply_keyboard
    )
