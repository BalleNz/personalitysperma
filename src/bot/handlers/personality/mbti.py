from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from src.core.schemas.user_schemas import UserSchema
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
        callback_query: CallbackQuery,
        access_token: str,
        cache_service: CacheService
):
    """признаки рейнина в зависимости от mbti букв"""
    await callback_query.answer()

    mbti: UserSocionicsSchema = await cache_service.get_characteristic_row(
        characteristic_type="UserSocionicsSchema",
        telegram_id=str(callback_query.from_user.id),
        access_token=access_token
    )

    text: str = Formatter.format_reinin_socionics(
        mbti=mbti
    )

    keyboard: InlineKeyboardMarkup = back_to_personality_listing_keyboard

    await callback_query.message.edit_text(
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
    mbti_1: UserSocionicsSchema = await cache_service.get_characteristic_row(
        characteristic_type="UserSocionicsSchema",
        telegram_id=str(message.from_user.id),
        access_token=access_token
    )

    mbti_2 = message.text.upper()

    # [ если сообщение не содержит mbti тип ]
    if mbti_2 not in VALID_MBTI_TYPES:
        await state.clear()

        # [ deps ]
        user: UserSchema = await cache_service.get_user_profile(
            access_token=access_token,
            telegram_id=str(message.from_user.id)
        )

        # [ главное действие ]
        await main(
            api_client=api_client,
            user=user,
            access_token=access_token,
            message=message,
            cache_service=cache_service
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
