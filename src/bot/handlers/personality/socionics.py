from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from src.bot.callbacks.callbacks import SocionicsReininCallback, SocionicsRelationshipsWaitingCallback
from src.bot.handlers.main.main import main
from src.bot.keyboards.inline.personality import back_to_personality_listing_keyboard
from src.bot.message_formatters.formatters import Formatter
from src.bot.states import States
from src.core.schemas.personality_types.socionics_type import UserSocionicsSchema
from src.core.services.api_client.personalityGPT_api import PersonalityGPT_APIClient
from src.core.services.cache_services.cache_service import CacheService

router = Router()

VALID_MBTI_TYPES = [
    "ISTJ", "ISFJ", "INFJ", "INTJ",
    "ISTP", "ISFP", "INFP", "INTP",
    "ESTP", "ESFP", "ENFP", "ENTP",
    "ESTJ", "ESFJ", "ENFJ", "ENTJ"
]


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


@router.callback_query(SocionicsRelationshipsWaitingCallback.filter())
async def show_relationships_briefly(
        callback: CallbackQuery,
        callback_data: SocionicsRelationshipsWaitingCallback,
        state: FSMContext
):
    """
    взаимоотношения c другими типа

    + возможность написать определенный тип для глубокого анализа совместимости
    """
    await callback.answer()

    text: str = Formatter.format_relationships_socionics_briefly(
        mbti=callback_data.mbti_type
    )

    keyboard: InlineKeyboardMarkup = back_to_personality_listing_keyboard

    await state.set_state(
        States.MBTI_RELATIONSHIPS_STATE
    )
    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


@router.message(States.MBTI_RELATIONSHIPS_STATE)
async def show_relationships(
        message: Message,
        access_token: str,
        cache_service: CacheService,
        api_client: PersonalityGPT_APIClient,
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

        # [ главное действие ]
        await main(
            api_client=api_client,
            access_token=access_token,
            message=message
        )

        return

    text: str = Formatter.format_relationships_socionics(
        mbti_1=mbti_1.primary_type,
        mbti_2=mbti_2
    )

    keyboard: InlineKeyboardMarkup = back_to_personality_listing_keyboard

    await message.answer(
        text=text,
        reply_markup=keyboard
    )
