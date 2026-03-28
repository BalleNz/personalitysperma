from aiogram import Router, F
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery

from src.bot.callbacks.callbacks import GetPersonalityCallback, \
    BackToListingPersonalityCallback
from src.bot.keyboards.inline.personality import get_personality_types_keyboard, back_to_personality_listing_keyboard, \
    get_mbti_keyboard
from src.bot.lexicon.button_text import ButtonText
from src.bot.lexicon.message_text import MessageText
from src.bot.message_formatters.personality_formatters import PersonalityMessageFormatter
from src.core.services.cache_services.cache_service import CacheService
from src.infrastructure.database.models.base import S
from src.infrastructure.database.repository.characteristic_repo import CharacteristicFormat

router = Router()


async def show_listing(
        message: Message | CallbackQuery,
):
    keyboard: InlineKeyboardMarkup = get_personality_types_keyboard()

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


@router.callback_query(BackToListingPersonalityCallback.filter())
async def back(
        callback_query: CallbackQuery
):
    """Возврат в листинг типов личности"""
    await callback_query.answer()

    await show_listing(
        callback_query,
    )


@router.message(F.text == ButtonText.MY_PERSONALITY)
async def personality_listing_menu(
        message: Message,
        cache_service: CacheService
):
    """Открывает меню с листингом типов личности"""
    # TODO if user.typing_passed ...

    await show_listing(
        message
    )


@router.callback_query(GetPersonalityCallback.filter())
async def show_personality(
        callback: CallbackQuery,
        callback_data: GetPersonalityCallback,
        access_token: str,
        cache_service: CacheService
):
    await callback.answer()

    telegram_id: str = str(callback.from_user.id)

    characteristic_name: str | None = callback_data.characteristic_name
    characteristic_type: type[S] = CharacteristicFormat.get_cls_from_schema_name(characteristic_name)

    personality_row: list[S] | None = await cache_service.get_characteristic_row(
        access_token=access_token,
        telegram_id=telegram_id,
        characteristic_name=characteristic_type,
    )
    personality: S | None = personality_row[0] if personality_row else None

    text: str = PersonalityMessageFormatter.get_personality_text_by_schema_name(
        schema_name=characteristic_name,
        schema=personality
    )

    keyboard: InlineKeyboardMarkup
    match characteristic_name:
        case "MBTISchema":
            keyboard = get_mbti_keyboard(
                personality.primary_type
            )
        case _:
            keyboard = back_to_personality_listing_keyboard

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )
