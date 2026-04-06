from aiogram import Router
from aiogram.types import InlineKeyboardMarkup, CallbackQuery

from src.bot.callbacks.callbacks import ReturnToCharacteristicListingAfterTypificationPassedCallback
from src.bot.keyboards.inline.typification import get_characteristics_list_after_typification_end_keyboard
from src.core.lexicon.typifications import TypificationPack, get_typification_pack

router = Router()


@router.callback_query()
async def get_characteristic_after_typification_end(
        callback: CallbackQuery,
        callback_data: ...,

):
    """показывает характеристику со стрелкой возврата в листинг полученных хар-ик после типирования"""
    ...


@router.callback_query()
async def get_personality_after_typification_end(
        callback: CallbackQuery,
        callback_data: ...,

):
    """показывает характеристику со стрелкой возврата в листинг полученных хар-ик после типирования"""
    ...


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
