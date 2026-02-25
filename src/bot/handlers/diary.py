import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from src.bot.callbacks.callbacks import DiaryPaginationCallback, DiaryGetCallback
from src.bot.keyboards.inline.diary import get_diary_listing_keyboard, get_diary_entry_keyboard
from src.bot.lexicon.button_text import ButtonText
from src.bot.lexicon.message_text import MessageText
from src.core.schemas.user_schemas import UserSchema
from src.core.services.cache_services.cache_service import CacheService
from src.core.utils.text_formatters import format_russian_date

logger = logging.getLogger(__name__)

router = Router(name="diary")


@router.message(F.text == ButtonText.DIARY)
async def show_diary(
        message: Message,
        cache_service: CacheService,
        access_token: str,
):
    await show_diaries(
        message,
        cache_service=cache_service,
        access_token=access_token,
        page=0
    )


@router.callback_query(DiaryPaginationCallback.filter())
async def diary_pagination_handler(
        callback: CallbackQuery,
        callback_data: DiaryPaginationCallback,
        cache_service: CacheService,
        access_token: str,
):
    await callback.answer()

    page = callback_data.page
    arrow = callback_data.arrow

    await show_diaries(
        callback,
        cache_service=cache_service,
        access_token=access_token,
        page=page,
        arrow=arrow
    )


@router.callback_query(DiaryGetCallback.filter())
async def show_single_entry(
        callback: CallbackQuery,
        callback_data: DiaryGetCallback,
        cache_service: CacheService,
        access_token: str,
):
    """Показывает запись в дневнике"""
    await callback.answer()

    # [ vars ]
    current_diary = callback_data.current_diary
    diaries_count = callback_data.diaries_count
    page = callback_data.page

    diaries = await cache_service.get_diary(
        access_token,
        str(callback.from_user.id)
    )

    diary = diaries[current_diary]
    date_str: str = format_russian_date(diary.created_at)

    # [ params ]
    text = MessageText.DIARY_RECORD.format(
        diary_context=diary.context_text,
        text=diary.text,
        date_str=date_str
    )

    keyboard = get_diary_entry_keyboard(
        diaries_count=diaries_count,
        page=page,
        current_diary=current_diary
    )

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


async def show_diaries(
        message: Message | CallbackQuery,
        cache_service: CacheService,
        access_token: str,
        page: int = 0,
        arrow: ButtonText.ARROW_LEFT | ButtonText.ARROW_RIGHT = None
):
    """
    Показывает страницу списка записей
    """
    # [ logic ]
    if arrow == ButtonText.ARROW_RIGHT:
        page += 1
    elif arrow == ButtonText.ARROW_LEFT:
        page -= 1
    elif arrow is None:
        pass

    user_id: str
    if type(message) == Message:
        user_id = str(message.from_user.id)
    else:
        user_id = str(message.message.from_user.id)

    user: UserSchema = await cache_service.get_user_profile(telegram_id=user_id, access_token=access_token)

    diaries = await cache_service.get_diary(
        access_token,
        user_id
    )
    text: str = MessageText.get_diary_listing_text(user.gender)

    if diaries:
        keyboard = get_diary_listing_keyboard(
            diaries=diaries,
            page=page
        )
    else:
        text += "\n\n<u>сейчас твой дневник пуст</u>"
        keyboard = None

    if type(message) == CallbackQuery:
        await message.message.edit_text(
            text=text,
            reply_markup=keyboard
        )
        return

    await message.reply(
        text=text,
        reply_markup=keyboard
    )
