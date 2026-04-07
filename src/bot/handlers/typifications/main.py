import logging

from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from src.api.request_schemas.typification import TypificationGetStatisticsRequest, TypificationGetQuestion, \
    TypificationRequest
from src.bot.keyboards.inline.typification import get_typification_may_end_on_mid_keyboard, \
    get_typification_start_keyboard, get_characteristics_list_after_typification_end_keyboard
from src.bot.lexicon.message_text import MessageText
from src.bot.states import States
from src.core.enums.user import GENDER
from src.core.lexicon.typifications import get_typification_pack, TypificationPack
from src.core.schemas.user_schemas import UserSchema
from src.core.services.api_client.personalityGPT_api import PersonalityGPT_APIClient
from src.core.services.cache_services.cache_service import CacheService

logger = logging.getLogger(__name__)


async def typification_preroll(
        callback: CallbackQuery,
        typification_pack_name: TypificationPack,
        from_message: bool | None
):
    # [ vars ]
    pack: dict = get_typification_pack(typification_pack_name)

    # [ pack vars ]
    typification_name_text: str = pack["name_ru"]
    typification_length: int = pack["pack_length"]
    characteristics_list: list[str] = pack["characteristics_text"]
    characteristics_text: str = "— " + "\n— ".join(characteristics_list)

    text: str = MessageText.TYPIFICATION_PREROLL.format(
        typification_name=typification_name_text,
        typification_length=typification_length,
        characteristics_text=characteristics_text
    )

    keyboard: InlineKeyboardMarkup = get_typification_start_keyboard(
        typification_pack_name
    )

    if from_message:  # проходит типирования после просьбы пройти тк это увеличит точность
        await callback.message.delete_reply_markup()
        await callback.message.reply(
            text=text,
            reply_markup=keyboard
        )
        return

    await callback.message.edit_text(
        text=text,
        reply_markup=keyboard
    )


async def typification_end(
        api_client: PersonalityGPT_APIClient,
        cache_service: CacheService,
        message: Message | CallbackQuery,
        access_token: str,
        typification_name: TypificationPack
):
    """ЗАКОНЧИТЬ ТИПИРОВАНИЕ С ОТПРАВКОЙ ОТВЕТОВ"""
    if type(message) is Message:
        user_tg_id: str = str(message.from_user.id)
    else:
        user_tg_id: str = str(message.message.from_user.id)

    # [ vars ]
    user: UserSchema = await cache_service.get_user_profile(
        access_token,
        user_tg_id
    )
    typification_pack: dict = get_typification_pack(typification_name)
    characteristics: list[str] = typification_pack["characteristic_groups"]

    answers: list[str] = await cache_service.redis_service.get_typification_answers(
        user_tg_id,
        typification_key=typification_name
    )
    request = TypificationRequest(
        answers=answers,
        characteristics=characteristics,
        typification_name=typification_name
    )

    await api_client.post_typification_results(
        access_token=access_token,
        request=request
    )

    typification_name_text: str = typification_pack["name_ru"]
    text: str = MessageText.get_typification_end_message(
        user.gender,
        typification_name_text=typification_name_text
    )

    keyboard: InlineKeyboardMarkup = get_characteristics_list_after_typification_end_keyboard(
        characteristic_groups=characteristics
    )

    if type(message) is Message:
        await message.answer(
            text=text,
            keyboard=keyboard
        )
    else:
        await message.message.edit_text(
            text=text,
            keyboard=keyboard
        )


async def typification_process(
        user_text: str,
        message: Message,
        cache_service: CacheService,
        access_token: str,
        state: FSMContext,
        api_client: PersonalityGPT_APIClient
):
    """ТИПИРОВАНИЕ процесс"""

    # [ vars ]
    user_tg_id: str = str(message.from_user.id)
    user: UserSchema = await cache_service.get_user_profile(
        access_token,
        user_tg_id
    )

    typification_pack_name: TypificationPack = await state.get_value("typification_pack_name")
    question_pack: dict = get_typification_pack(typification_pack_name)

    answers: list[str] = await cache_service.redis_service.get_typification_answers(user_tg_id, typification_pack_name)
    answer: str = user_text

    question_index: int = len(answers) + 1
    this_question: str = question_pack[question_index]

    # [ cache ]
    await cache_service.redis_service.add_typification_answer(
        tg_id=user_tg_id,
        typification_key=typification_pack_name,
        answer=answer
    )

    # [ state ]
    if question_index == question_pack['pack_length']:
        await state.set_state(States.TypificationEnd)

    # [ vars ]
    additional_text: str | None = None
    keyboard: InlineKeyboardMarkup | None = None

    # [ additional_text + keyboard ]
    if question_index in question_pack["may_end"]:
        additional_text: str = await api_client.get_additional_text_on_mid_test(
            access_token=access_token,
            request=TypificationGetStatisticsRequest(
                answers=answers,
                typification_name=typification_pack_name,
            )
        )
        keyboard: InlineKeyboardMarkup = get_typification_may_end_on_mid_keyboard()  # <закончить типирование!>

    gender: str
    if user.gender in (GENDER.MALE, GENDER.MAN):
        gender = "male"
    elif user.gender in (GENDER.WOMAN, GENDER.GIRL):
        gender = "girl"
    else:
        gender = "non_binary"

    # [ api: get_question ]
    request = TypificationGetQuestion(
        last_answer=question_pack[question_index] + f" {answer}",
        this_question=this_question,
        gender=gender
    )
    question: str = await api_client.get_next_question(access_token, request=request)

    await message.answer(
        text=question,
        reply_markup=keyboard
    )
