from typing import Callable

from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery

from src.bot.callbacks.callbacks import GetCharacteristicCallback
from src.bot.keyboards.inline import get_characteristic_listing_keyboard
from src.bot.lexicon.button_text import ButtonText
from src.bot.lexicon.message_text import MessageText
from src.bot.utils.message_formatters import PersonalityMessageFormatter
from src.core.services.api_client.personalityGPT_api import PersonalityGPT_APIClient
from src.core.services.cache_services.cache_service import CacheService
from src.infrastructure.database.models.base import S
from src.infrastructure.database.repository.characteristic_repo import CharacteristicFormat

router = Router()


async def show_listing(
        message: Message | CallbackQuery,
        api_client: PersonalityGPT_APIClient,
        access_token: str
):
    keyboard: InlineKeyboardMarkup = get_characteristic_listing_keyboard()

    if type(message) == Message:
        await message.reply(
            text=MessageText.CHARACTERISTIC_LISTING_MESSAGE,
            reply_markup=keyboard
        )
    else:
        await message.message.reply(
            text=MessageText.CHARACTERISTIC_LISTING_MESSAGE,
            reply_markup=keyboard
        )

    # TODO:
    #   - USER:
    #       - unlocked_<table_name>: bool
    #   - по этому полю проверять в formatters, если генерация существует, то показывать её лишь первые 2-3 строки — остальное ???


@router.callback_query()
async def back(
        callback_query: CallbackQuery,
        api_client: PersonalityGPT_APIClient,
        access_token: str
):
    await show_listing(
        callback_query,
        api_client,
        access_token
    )


@router.message(F.text == ButtonText.CHARACTETISTIC_LISTING)
async def characteristic_listing_menu(
        message: Message,
        api_client: PersonalityGPT_APIClient,
        access_token: str
):
    """Открывает меню с inline листингом характеристик"""
    await show_listing(
        message,
        api_client,
        access_token
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

    characteristic: S = await cache_service.get_characteristic(
        access_token=access_token,
        telegram_id=telegram_id,
        characteristic_type=characteristic_type
    )

    characteristic_formatter: Callable[
        [S], str] = PersonalityMessageFormatter.characteristic_formatter.get_characteristic_text_by_schema(
        schema_type=characteristic_type.__name__
    )

    text = characteristic_formatter(characteristic)

    keyboard =

    await callback.message.reply(
        text=text,
        reply_markup=None
    )
