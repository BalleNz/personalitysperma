import asyncio
import io
import logging

from aiogram import Router, F
from aiogram.types import Message, CallbackQuery

from src.api.request_schemas.research import ResearchSurveyFinishRequest
from src.api.response_schemas.psycho import PsychoResponse
from src.api.response_schemas.research import Characteristic
from src.bot.bot_instance import bot
from src.bot.callbacks.callbacks import SurveyAnswerCallback
from src.bot.handlers.main.main import main
from src.bot.keyboards.inline.start import get_full_access_keyboard
from src.bot.lexicon.message_text import MessageText
from src.core.consts import FREE_VOICE_MESSAGES_COUNT
from src.core.schemas.user_schemas import UserSchema
from src.core.services.api_client.personalityGPT_api import PersonalityGPT_APIClient
from src.core.services.cache_services.cache_service import CacheService
from src.core.services.dependencies.speech_service_dep import get_speech_service
from src.core.services.speech_to_text_service import SpeechService
from src.infrastructure.database.models.base import S
from src.infrastructure.database.repository.characteristic_repo import SHORT_TO_FULL_SCHEMA, get_schema_type_from_name

router = Router()
logger = logging.getLogger(__name__)


@router.message(F.voice)
async def main_voice(
        message: Message,
        api_client: PersonalityGPT_APIClient,
        access_token: str,
        cache_service: CacheService
):
    """обработка голосового сообщения"""
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
        await message.reply(text or "Не удалось распознать речь")
        return

    await main(
        message,
        api_client,
        access_token,
        user,
        cache_service
    )


@router.message()
async def main_handler(
        message: Message,
        api_client: PersonalityGPT_APIClient,
        access_token: str,
        cache_service: CacheService
):
    """Главное действие пользователя"""
    user: UserSchema = await cache_service.get_user_profile(
        access_token,
        str(message.from_user.id),
    )

    await main(
        message,
        api_client,
        access_token,
        user,
        cache_service
    )


@router.callback_query(SurveyAnswerCallback.filter())
async def survey_final(
        callback_query: CallbackQuery,
        callback_data: SurveyAnswerCallback,
        api_client: PersonalityGPT_APIClient,
        access_token: str,
        cache_service: CacheService
):
    """после тапа на ответ в SURVEY"""
    await callback_query.answer()

    await callback_query.message.edit_text(
        text=MessageText.get_process_message(),
        reply_markup=None
    )

    # [ deps ]
    user: UserSchema = await cache_service.get_user_profile(
        access_token=access_token,
        telegram_id=str(callback_query.from_user.id)
    )

    # [ callback ]
    question = callback_query.message.text.split("\n\n")[-1]

    answer = await cache_service.redis_service.redis.get(
        f"survey:answer:{callback_data.answer_hash}"
    )

    characteristics_name = [
        SHORT_TO_FULL_SCHEMA.get(short.strip(), short)
        for short in callback_data.characteristic_names.split(" ")
    ]

    # Получаем все характеристики параллельно
    characteristics_tasks = {
        name: cache_service.get_characteristic_row(
            access_token=access_token,
            telegram_id=str(callback_query.from_user.id),
            characteristic_type=name
        )
        for name in characteristics_name
    }

    characteristics_results = await asyncio.gather(*characteristics_tasks.values(), return_exceptions=True)

    characteristics = []
    for name, result in zip(characteristics_tasks.keys(), characteristics_results):
        if isinstance(result, Exception):
            logger.error(f"Ошибка получения {name}: {result}")
            continue

        schema_obj: S = result if type(result) != list else result[0]

        # Если None — создаём пустую схему
        if schema_obj is None:
            schema_cls = get_schema_type_from_name(name)
            schema_obj = schema_cls(
                user_id=user.id
            ) if schema_cls else None  # пустая с дефолтами

        if schema_obj:
            characteristics.append(
                Characteristic(
                    characteristic_name=name,
                    characteristic=schema_obj.model_dump(
                        exclude={"id", "user_id", "created_at", "updated_at", "telegram_id", "GROUP"},
                        exclude_none=False
                    )  # dict, все поля
                )
            )

    request = ResearchSurveyFinishRequest(
        question=question,
        answer=answer,
        characteristics=characteristics
    )

    response: PsychoResponse = await api_client.research_survey_finish(
        access_token=access_token,
        request=request
    )

    await callback_query.message.edit_text(
        text=response.user_answer
    )
