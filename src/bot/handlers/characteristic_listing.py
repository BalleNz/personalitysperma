from typing import Callable

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery

from src.bot.callbacks.callbacks import GetCharacteristicCallback, BackToListingCallback
from src.bot.keyboards.inline import get_characteristic_listing_keyboard, back_from_listing_keyboard
from src.bot.lexicon.button_text import ButtonText
from src.bot.lexicon.message_text import MessageText
from src.bot.utils.message_formatters import PersonalityMessageFormatter
from src.core.schemas.user_schemas import UserSchema
from src.core.services.api_client.personalityGPT_api import PersonalityGPT_APIClient
from src.core.services.cache_services.cache_service import CacheService
from src.infrastructure.database.models.base import S
from src.infrastructure.database.repository.characteristic_repo import CharacteristicFormat

router = Router()


async def show_listing(
        message: Message | CallbackQuery
):
    keyboard: InlineKeyboardMarkup = get_characteristic_listing_keyboard()

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


@router.callback_query(BackToListingCallback.filter())
async def back(
        callback_query: CallbackQuery
):
    await callback_query.answer()

    await show_listing(
        callback_query
    )


@router.message(F.text == ButtonText.CHARACTETISTIC_LISTING)
async def characteristic_listing_menu(
        message: Message
):
    """Открывает меню с inline листингом характеристик"""
    await show_listing(
        message
    )


@router.callback_query(GetCharacteristicCallback.filter())
async def show_characteristic(
        callback: CallbackQuery,
        callback_data: GetCharacteristicCallback,
        access_token: str,
        cache_service: CacheService
):
    telegram_id: str = str(callback.from_user.id)
    characteristic_name: str = callback_data.characteristic_name
    characteristic_type: type[S] = CharacteristicFormat.get_schema_type_from_schema_name(characteristic_name)

    user: UserSchema = await cache_service.get_user_profile(access_token, telegram_id)

    characteristic: S | list[S] = await cache_service.get_characteristic(
        access_token=access_token,
        telegram_id=telegram_id,
        characteristic_type=characteristic_type
    )

    characteristic_formatter: Callable[[S], str] = (
        PersonalityMessageFormatter.characteristic_formatter.get_characteristic_text_by_schema(
            schema_type=characteristic_type.__name__
        )
    )

    text = characteristic_formatter(characteristic, user.full_access)

    keyboard = back_from_listing_keyboard

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )
