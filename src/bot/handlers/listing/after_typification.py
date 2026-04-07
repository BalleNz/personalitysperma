from aiogram import Router
from aiogram.types import InlineKeyboardMarkup, CallbackQuery

from src.bot.callbacks.callbacks import GetCharacteristicAfterTypificationPassedCallback, \
    GetPersonalityAfterTypificationPassedCallback, ReturnToCharacteristicListingAfterTypificationPassedCallback
from src.bot.handlers.listing.characteristic_listing import show_characteristic
from src.bot.handlers.listing.personality_list import show_personality
from src.bot.keyboards.inline.typification import get_characteristics_list_after_typification_end_keyboard
from src.core.lexicon.typifications import TypificationPack, get_typification_pack
from src.core.services.cache_services.cache_service import CacheService

router = Router()


@router.callback_query(GetCharacteristicAfterTypificationPassedCallback.filter())
async def get_characteristic_after_typification_end(
        callback: CallbackQuery,
        callback_data: GetCharacteristicAfterTypificationPassedCallback,
        access_token: str,
        cache_service: CacheService
):
    """показывает характеристику со стрелкой возврата в листинг полученных хар-ик после типирования"""
    await show_characteristic(
        callback,
        callback_data,
        access_token,
        cache_service,
        from_typification_end_name=callback_data.typification_name
    )


@router.callback_query(GetPersonalityAfterTypificationPassedCallback.filter())
async def get_personality_after_typification_end(
        callback: CallbackQuery,
        callback_data: GetPersonalityAfterTypificationPassedCallback,
        access_token: str,
        cache_service: CacheService
):
    """показывает тип личности со стрелкой возврата в листинг полученных хар-ик после типирования"""
    await show_personality(
        callback,
        callback_data,
        access_token,
        cache_service,
        typification_name=GetPersonalityAfterTypificationPassedCallback.typification_name
    )


@router.callback_query(ReturnToCharacteristicListingAfterTypificationPassedCallback.filter())
async def back_to_listing_after_typification_passed(
        callback: CallbackQuery,
        callback_data: ReturnToCharacteristicListingAfterTypificationPassedCallback,
):
    """возврат к листингу характеристик после типирования"""
    pack_name: TypificationPack = callback_data.typification_pack
    typification_pack: dict = get_typification_pack(
        pack_name=pack_name
    )

    characteristic_groups: list[str] = typification_pack["characteristic_groups"]

    keyboard: InlineKeyboardMarkup = get_characteristics_list_after_typification_end_keyboard(
        characteristic_groups
    )

    await callback.message.edit_text(
        text="какую характеристику смотрим? ^^",
        reply_markup=keyboard
    )
