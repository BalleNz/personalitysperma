import hashlib

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.core.services.cache_services.redis_service import RedisService
from src.infrastructure.database.repository.characteristic_repo import SCHEMA_SHORT_NAMES
from src.api.response_schemas.research import QuestionPack
from src.bot.callbacks.callbacks import SurveyAnswerCallback


def get_answer_hash(answer: str) -> str:
    """Генерирует короткий уникальный ключ для текста ответа"""
    return hashlib.sha256(answer.encode('utf-8')).hexdigest()[:16]  # 16 hex символов — 16 байт


async def get_survey_keyboard(
        question_pack: QuestionPack,
        redis_service: RedisService
) -> InlineKeyboardMarkup:
    """клавиатура с ответами на вопросы"""
    buttons: list[InlineKeyboardButton] = []

    for i, answer_pack in enumerate(question_pack.answer_packs, start=1):
        answer_hash = get_answer_hash(answer_pack.answer)
        char_names = " ".join([SCHEMA_SHORT_NAMES.get(char_name) for char_name in answer_pack.characteristics])

        await redis_service.redis.set(
            f"survey:answer:{answer_hash}",
            answer_pack.answer,
            ex=86400
        )

        buttons.append(
            InlineKeyboardButton(
                text=f"{i}",
                callback_data=SurveyAnswerCallback(
                    answer_hash=answer_hash,
                    characteristic_names=char_names
                ).pack()
            )
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[buttons]
    )
