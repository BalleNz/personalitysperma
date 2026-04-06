import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup

from src.bot.callbacks.callbacks import TypificationAlreadyPassedCallback, TypificationCallback, \
    TypificationListingCallback
from src.bot.keyboards.inline.typification import get_typification_listing_keyboard, \
    get_typification_delete_progress_keyboard
from src.bot.lexicon.message_text import MessageText
from src.core.schemas.user_schemas import UserSchema
from src.core.services.cache_services.cache_service import CacheService

logger = logging.getLogger(__name__)

router = Router(name="typification_listing")


@router.callback_query(TypificationListingCallback.filter())
async def typification_listing(
        callback: CallbackQuery,
        callback_data: TypificationCallback,
        cache_service: CacheService,
        access_token: str,
        state: FSMContext
):
    """
    хендлер просмотра листинга типификаций

    кнопка после выбора гендера и имени в /start

    TODO: также в каждом сообщении будет клавиатура + текст курсивом снизу с просьбой пройти тест
    """
    await callback.answer()

    user: UserSchema = await cache_service.get_user_profile(access_token, str(callback.from_user.id))

    keyboard: InlineKeyboardMarkup = get_typification_listing_keyboard(user)

    text: str = MessageText.TYPIFICATION_LISTING

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


@router.callback_query(TypificationAlreadyPassedCallback.filter())
async def typification_already_passed(
        callback: CallbackQuery,
):
    """Предупреждает юзера, что данный тест уже пройден"""
    await callback.answer()

    keyboard: InlineKeyboardMarkup = get_typification_delete_progress_keyboard()

    await callback.message.answer(
        text="ты уже проходил этот тест, хочешь пройти еще раз? ^^",
        reply_markup=keyboard
    )
