import io

from aiogram import Router, F
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, Message

from src.bot.bot_instance import bot
from src.bot.callbacks.callbacks import TypificationPreRollCallback, TypificationEndOnMidCallback, TypificationCallback
from src.bot.handlers.typifications.listing import delete_typification_progress
from src.bot.handlers.typifications.main import typification_process, typification_preroll, typification_end
from src.bot.keyboards.inline.start import get_full_access_keyboard
from src.bot.lexicon.message_text import MessageText
from src.bot.states import States
from src.core.consts import FREE_VOICE_MESSAGES_COUNT
from src.core.lexicon.typifications import TypificationPack, get_typification_pack
from src.core.schemas.user_schemas import UserSchema
from src.core.services.api_client.personalityGPT_api import PersonalityGPT_APIClient
from src.core.services.cache_services.cache_service import CacheService
from src.core.services.dependencies.speech_service_dep import get_speech_service
from src.core.services.speech_to_text_service import SpeechService

router = Router(name="typification_main")


@router.callback_query(TypificationPreRollCallback.filter())
async def typification_preroll_from_callback(
        callback: CallbackQuery,
        callback_data: TypificationPreRollCallback,
        api_client: PersonalityGPT_APIClient,
        access_token: str
):
    if callback_data.is_passed:
        # [ просьба удалить прогресс ]
        await delete_typification_progress(
            callback=callback,
            typification_pack_name=callback_data.typification_name,
            api_client=api_client,
            access_token=access_token
        )
        return

    await typification_preroll(
        callback,
        typification_pack_name=callback_data.typification_name,
        from_message=callback_data.from_message
    )


@router.callback_query(TypificationEndOnMidCallback.filter())  # закончить преждевременно
async def typification_end_mid_callback(
        callback: CallbackQuery,
        api_client: PersonalityGPT_APIClient,
        cache_service: CacheService,
        state: FSMContext,
        access_token: str
):
    """ЗАКОНЧИТЬ НА СЕРЕДИНЕ"""
    await callback.answer()

    # [ state ]
    typification_key: TypificationPack = await state.get_value("typification_pack_name")
    await state.clear()

    await typification_end(
        api_client=api_client,
        cache_service=cache_service,
        message=callback,
        access_token=access_token,
        typification_name=typification_key
    )


@router.callback_query(TypificationCallback.filter())
async def typification_start(
        callback: CallbackQuery,
        callback_data: TypificationCallback,
        state: FSMContext
):
    """ТИПИРОВАНИЕ старт"""
    await callback.answer()

    typification_pack_name: TypificationPack = callback_data.typification_name

    await state.set_state(States.Typification)
    await state.set_data(
        {
            "typification_pack_name": typification_pack_name
        }
    )

    pack: dict = get_typification_pack(typification_pack_name)
    question: str = pack[1]  # первый вопрос

    await callback.message.edit_text(
        text=question
    )


@router.message(States.Typification, F.voice)
async def typification_process_voice(
        message: Message,
        api_client: PersonalityGPT_APIClient,
        access_token: str,
        cache_service: CacheService,
        state: FSMContext
):
    user_telegram_id: str = str(message.from_user.id)
    user: UserSchema = await cache_service.get_user_profile(access_token=access_token, telegram_id=user_telegram_id)

    if not user.full_access and user.used_voice_messages > FREE_VOICE_MESSAGES_COUNT:
        """закончился лимит голосовых, купить доступ"""
        keyboard = get_full_access_keyboard()
        await message.reply(MessageText.VOICE_LIMIT, reply_markup=keyboard)
        return

    await api_client.increase_used_voices(access_token)

    buffer = io.BytesIO()
    await bot.download(message.voice, destination=buffer)
    buffer.seek(0)

    service: SpeechService = get_speech_service()
    text: str = await service.transcribe_bytes(buffer.getvalue())

    if not text:
        await message.reply(text or "не удалось распознать речь. попробуй текстом.")
        return

    await typification_process(
        user_text=text,
        message=message,
        cache_service=cache_service,
        access_token=access_token,
        state=state,
        api_client=api_client
    )


@router.message(States.Typification)
async def typification_process_text(
        message: Message,
        cache_service: CacheService,
        access_token: str,
        state: FSMContext,
        api_client: PersonalityGPT_APIClient
):
    await typification_process(
        user_text=message.text,
        message=message,
        cache_service=cache_service,
        access_token=access_token,
        state=state,
        api_client=api_client
    )


@router.message(States.TypificationEnd)
async def typification_end_callback(
        api_client: PersonalityGPT_APIClient,
        cache_service: CacheService,
        message: Message,
        state: FSMContext,
        access_token: str
):
    """ЗАКОНЧИТЬ НА ПОСЛЕДНЕМ ВОПРОСЕ"""
    # [ state ]
    typification_key: TypificationPack = await state.get_value("typification_pack_name")
    await state.clear()

    await typification_end(
        api_client=api_client,
        message=message,
        cache_service=cache_service,
        access_token=access_token,
        typification_name=typification_key
    )
