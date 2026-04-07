import logging

from aiogram import Router
from aiogram.filters import Command
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from src.api.request_schemas.typification import DeleteTypificationRequest
from src.bot.callbacks.callbacks import DeleteTypificationCallback, TypificationAlreadyPassedCallback, \
    TypificationListingCallback
from src.bot.handlers.typifications.main import typification_preroll
from src.bot.keyboards.inline.typification import get_typification_listing_keyboard, \
    get_typification_delete_progress_keyboard
from src.bot.lexicon.message_text import MessageText
from src.core.enums.user import GENDER
from src.core.lexicon.typifications import TypificationPack
from src.core.schemas.user_schemas import UserSchema
from src.core.services.api_client.personalityGPT_api import PersonalityGPT_APIClient
from src.core.services.cache_services.cache_service import CacheService

logger = logging.getLogger(__name__)

router = Router(name="typification_listing")


@router.callback_query(TypificationListingCallback.filter())
async def typification_listing_from_callback(
        callback: CallbackQuery,
        cache_service: CacheService,
        access_token: str
):
    await typification_listing(
        callback,
        cache_service,
        access_token
    )


@router.message(Command("typification"))
async def typification_listing_from_command(
        callback: CallbackQuery,
        cache_service: CacheService,
        access_token: str
):
    await typification_listing(
        callback,
        cache_service,
        access_token
    )


async def typification_listing(
        message: CallbackQuery | Message,
        cache_service: CacheService,
        access_token: str
):
    """
    хендлер просмотра листинга типификаций

    кнопка после выбора гендера и имени в /start

    и командой /typifications  (иногда давать подсказки в автоматических расслках)

    TODO: также в каждом сообщении будет клавиатура + текст курсивом снизу с просьбой пройти тест
    """
    if type(message) is CallbackQuery:
        await message.answer()

    user: UserSchema = await cache_service.get_user_profile(access_token, str(message.from_user.id))

    keyboard: InlineKeyboardMarkup = get_typification_listing_keyboard(user)

    text: str = MessageText.TYPIFICATION_LISTING

    if type(message) is CallbackQuery:
        await message.message.edit_text(
            text=text,
            reply_markup=keyboard
        )
        return

    await message.reply(
        text,
        reply_markup=keyboard
    )


@router.callback_query(TypificationAlreadyPassedCallback.filter())
async def typification_already_passed(
        callback: CallbackQuery,
        callback_data: TypificationAlreadyPassedCallback,
        cache_service: CacheService,
        access_token: str
):
    """Предупреждает юзера, что данный тест уже пройден"""
    await callback.answer()

    keyboard: InlineKeyboardMarkup = get_typification_delete_progress_keyboard(
        typification_pack_name=callback_data.typification_name
    )

    user: UserSchema = await cache_service.get_user_profile(
        access_token,
        str(callback.from_user.id)
    )

    text = "эта типификация уже пройдена.\n\nхочешь сбросить прогресс?\nнапиши /reset"
    if user.gender in (GENDER.WOMAN, GENDER.GIRL):
        text = "ты уже проходила это типирование ^^\n\nхочешь сбросить прогресс?\nнапиши /reset"

    await callback.message.answer(
        text=text,
        reply_markup=keyboard
    )


@router.callback_query(DeleteTypificationCallback.filter())
async def delete_typification_progress_from_callback(
        callback: CallbackQuery,
        callback_data: DeleteTypificationCallback,
        api_client: PersonalityGPT_APIClient,
        access_token: str
):
    await delete_typification_progress(
        callback=callback,
        typification_pack_name=callback_data.typification_name,
        api_client=api_client,
        access_token=access_token
    )


async def delete_typification_progress(
        callback: CallbackQuery,
        typification_pack_name: TypificationPack,
        api_client: PersonalityGPT_APIClient,
        access_token: str
):
    """Удалить пройденную типификацию"""
    await callback.answer()

    request = DeleteTypificationRequest(
        typification_name=typification_pack_name
    )

    await api_client.delete_typification(
        access_token=access_token,
        request=request
    )

    await typification_preroll(
        callback,
        typification_pack_name=typification_pack_name
    )
