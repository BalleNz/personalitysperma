from typing import Callable, Any

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery

from src.bot.callbacks.callbacks import GetCharacteristicAfterTypificationPassedCallback, GetCharacteristicCallback, \
    BackToListingCharacteristicCallback
from src.bot.keyboards.inline.characteristics import get_characteristic_listing_keyboard, \
    back_to_characteristic_listing_keyboard
from src.bot.keyboards.inline.typification import get_return_to_listing_after_typification_keyboard
from src.bot.lexicon.button_text import ButtonText
from src.bot.lexicon.message_text import MessageText
from src.bot.message_formatters.characteristic_formatters import CharacteristicMessageFormatter
from src.core.lexicon.typifications import TypificationPack
from src.core.schemas.user_schemas import UserSchema
from src.core.services.cache_services.cache_service import CacheService
from src.infrastructure.database.models.base import S

router = Router()


async def show_listing(
        message: Message | CallbackQuery,
        user_characteristics: dict[str, dict[str, Any]]
) -> None:
    keyboard: InlineKeyboardMarkup = get_characteristic_listing_keyboard(
        user_characteristics
    )

    if type(message) == Message:
        await message.reply(
            text=MessageText.CHARACTERISTIC_LISTING_MESSAGE,
            reply_markup=keyboard
        )
    else:
        await message.message.edit_text(
            text=MessageText.CHARACTERISTIC_LISTING_MESSAGE,
            reply_markup=keyboard
        )


@router.callback_query(BackToListingCharacteristicCallback.filter())
async def back(
        callback_query: CallbackQuery,
        cache_service: CacheService,
        access_token: str
):
    """Открывает меню с листингом характеристик"""
    await callback_query.answer()

    user_characteristics: dict[str, dict[str, Any]] = await cache_service.get_all_characteristics(
        access_token,
        str(callback_query.message.from_user.id)
    )

    await show_listing(
        callback_query,
        user_characteristics
    )


@router.message(F.text == ButtonText.MY_CHARACTERISTIC)
async def characteristic_listing_menu(
        message: Message,
        cache_service: CacheService,
        access_token: str
):
    """Открывает меню с листингом характеристик"""

    user_characteristics: dict[str, dict[str, Any]] = await cache_service.get_all_characteristics(
        access_token,
        str(message.from_user.id)
    )

    await show_listing(
        message,
        user_characteristics
    )


@router.callback_query(GetCharacteristicCallback.filter())
async def show_characteristic_from_listing(
        callback_query: CallbackQuery,
        callback_data: GetCharacteristicCallback,
        access_token: str,
        cache_service: CacheService
):
    """показывает характеристику после обычного листинга"""

    await show_characteristic(
        callback_query,
        callback_data,
        access_token,
        cache_service
    )


async def show_characteristic(
        callback_query: CallbackQuery,
        callback_data: GetCharacteristicCallback | GetCharacteristicAfterTypificationPassedCallback,
        access_token: str,
        cache_service: CacheService,
        from_typification_end_name: TypificationPack = ""
):
    """Показывает характеристику"""
    await callback_query.answer()

    telegram_id: str = str(callback_query.from_user.id)

    characteristic_group: str | None = callback_data.characteristic_group

    user: UserSchema = await cache_service.get_user_profile(access_token, telegram_id)

    characteristics: list[S] | list[list[S]] | None = await cache_service.get_characteristic_row(
        access_token=access_token,
        telegram_id=telegram_id,
        characteristic_group=characteristic_group
    )

    characteristic_formatter: Callable[[list[list[S]], bool], str] = (
        CharacteristicMessageFormatter.characteristic_formatter.get_characteristic_text_by_schema(
            formatter_name=characteristic_group
        )
    )

    full_access: bool = user.full_access
    text: str = characteristic_formatter(characteristics, full_access)  # сделать чище

    keyboard: InlineKeyboardMarkup
    if not from_typification_end_name:
        keyboard = back_to_characteristic_listing_keyboard
    else:
        keyboard = get_return_to_listing_after_typification_keyboard(
            typification_name=from_typification_end_name
        )

    await callback_query.message.edit_text(
        text=text,
        reply_markup=keyboard
    )
