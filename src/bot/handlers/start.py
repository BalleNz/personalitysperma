import logging

from aiogram import Router
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, CallbackQuery

from src.bot.callbacks.callbacks import SelectGenderCallback
from src.bot.keyboards.inline import gender_select_keyboard
from src.bot.keyboards.reply import MAIN_KEYBOARD_PSYCHO
from src.bot.lexicon.message_text import MessageText
from src.core.enums.user import GENDER
from src.core.services.api_client.personalityGPT_api import PersonalityGPT_APIClient
from src.core.services.cache_services.cache_service import CacheService

router = Router(name=__name__)
logger = logging.getLogger(name=__name__)


@router.callback_query(SelectGenderCallback.filter())
async def select_gender(
        callback: CallbackQuery,
        callback_data: SelectGenderCallback,
        api_client: PersonalityGPT_APIClient,
        cache_service: CacheService,
        access_token: str,
):
    await callback.answer()

    gender = callback_data.gender

    await api_client.change_gender(
        gender,
        access_token
    )

    text: str = MessageText.HELLO_MALE if gender == GENDER.MALE else MessageText.HELLO_GIRL

    await callback.message.delete()
    await callback.message.answer(
        text,
        reply_markup=MAIN_KEYBOARD_PSYCHO
    )


@router.message(CommandStart())
async def start_dialog(
        message: Message,
        state: FSMContext
):
    await state.clear()

    user_id = str(message.from_user.id)

    await message.answer(text=MessageText.HELLO_GENDER_SELECT, reply_markup=gender_select_keyboard)
    logger.info(f"User {user_id} has started dialog.")
