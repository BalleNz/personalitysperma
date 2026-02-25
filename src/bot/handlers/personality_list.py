from typing import Callable

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import Message, InlineKeyboardMarkup, CallbackQuery

from src.bot.callbacks.callbacks import GetPersonalityCallback, BackToListingPersonalityCallback
from src.bot.callbacks.callbacks import SocionicsReininCallback
from src.bot.keyboards.inline.personality import get_personality_types_keyboard, back_to_personality_listing_keyboard
from src.bot.keyboards.inline.personality import get_socionics_keyboard
from src.bot.lexicon.button_text import ButtonText
from src.bot.lexicon.message_text import MessageText
from src.bot.message_formatters.characteristic_formatters import CharacteristicMessageFormatter
from src.bot.message_formatters.formatters import Formatter
from src.core.schemas.personality_types.socionics_type import UserSocionicsSchema
from src.core.schemas.user_schemas import UserSchema
from src.core.services.cache_services.cache_service import CacheService
from src.infrastructure.database.models.base import S
from src.infrastructure.database.repository.characteristic_repo import CharacteristicFormat

router = Router()

VALID_MBTI_TYPES = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]

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
    """Открывает меню с листингом характеристик"""

    await callback_query.answer()

    await show_listing(
        callback_query,
    )


@router.message(F.text == ButtonText.MY_PERSONALITY)
async def personality_listing_menu(
        message: Message
):
    """Открывает меню с листингом типов личности"""

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
    telegram_id: str = str(callback.from_user.id)

    characteristic_name: str | None = callback_data.characteristic_name
    characteristic_type: type[S] = CharacteristicFormat.get_cls_from_schema_name(characteristic_name)

    characteristic: S | list[S] = await cache_service.get_characteristic(
        access_token=access_token,
        telegram_id=telegram_id,
        characteristic_type=characteristic_type,
    )

    characteristic_formatter: Callable[[S], str] = (
        CharacteristicMessageFormatter.characteristic_formatter.get_characteristic_text_by_schema(
            formatter_name=characteristic_type.__name__
        )
    )

    user: UserSchema = await cache_service.get_user_profile(
        access_token, telegram_id
    )

    text = characteristic_formatter(characteristic)  # сделать чище

    keyboard: InlineKeyboardMarkup
    match characteristic_name:
        case "UserSocionicsSchema":
            keyboard = get_socionics_keyboard()
        case _:
            keyboard = back_to_personality_listing_keyboard

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


# [ SOCIONICS ]


@router.callback_query(SocionicsReininCallback.filter())
async def show_reinin(
        callback: CallbackQuery,
        access_token: str,
        cache_service: CacheService
):
    """признаки рейнина в зависимости от mbti букв"""
    mbti: UserSocionicsSchema = await cache_service.get_characteristic(
        characteristic_type="UserSocionicsSchema",
        telegram_id=str(callback.from_user.id),
        access_token=access_token
    )

    text: str = Formatter.format_reinin_socionics(
        mbti=mbti
    )

    keyboard: InlineKeyboardMarkup = back_to_personality_listing_keyboard

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


@router.message()  # TODO state filter
async def show_relationships(
        message: Message,
        access_token: str,
        cache_service: CacheService,
        state: FSMContext
):
    """взаимоотношения между двумя"""
    mbti_1: UserSocionicsSchema = await cache_service.get_characteristic(
        characteristic_type="UserSocionicsSchema",
        telegram_id=str(message.from_user.id),
        access_token=access_token
    )

    mbti_2 = message.text

    # [ если сообщение не содержит mbti тип ]
    if mbti_2 not in VALID_MBTI_TYPES:
        await state.clear()
        return

    text: str = Formatter.format_relationships_socionics(
        mbti_1=mbti_1.primary_type,
        mbti_2=mbti_2
    )

    await message.answer(
        text=text
    )
