import logging

from aiogram import Router
from aiogram.fsm.context import FSMContext
from aiogram.types import CallbackQuery, InlineKeyboardMarkup, Message

from callbacks.callbacks import TypificationEndOnMidCallback
from keyboards.inline.typification import get_characteristics_list_after_typification_end_keyboard
from src.api.request_schemas.typification import TypificationGetStatisticsRequest, DeleteTypificationRequest, \
    TypificationGetQuestion, TypificationRequest
from src.bot.callbacks.callbacks import DeleteTypificationCallback, TypificationCallback
from src.bot.keyboards.inline.typification import get_typification_may_end_on_mid_keyboard
from src.bot.lexicon.message_text import MessageText
from src.bot.states import States
from src.core.lexicon.typifications import get_typification_pack, TypificationPack
from src.core.schemas.user_schemas import UserSchema
from src.core.services.api_client.personalityGPT_api import PersonalityGPT_APIClient
from src.core.services.cache_services.cache_service import CacheService

logger = logging.getLogger(__name__)

router = Router(name="typification_main")


@router.callback_query(TypificationCallback.filter())
async def typification_start(
        callback: CallbackQuery,
        callback_data: TypificationCallback,
        cache_service: CacheService,
        access_token: str,
        state: FSMContext
):
    """ТИПИРОВАНИЕ старт"""
    await callback.answer()

    typification_pack_name: TypificationPack = callback_data.question_pack

    await state.set_state(States.Typification)
    await state.set_data(
        {
            "typification_pack_name": typification_pack_name
        }
    )

    user: UserSchema = await cache_service.get_user_profile(
        access_token,
        str(callback.from_user.id)
    )

    pack: dict = get_typification_pack(typification_pack_name)
    question: str = pack["1"]  # первый вопрос

    message: str = MessageText.get_typification_process_message(
        True,
        question,
        gender=user.gender
    )

    await callback.message.edit_text(
        text=message
    )


@router.message(States.Typification)
async def typification_process(
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
    answer: str = message.text

    question_index: int = len(answers) + 1
    this_question: str = question_pack[question_index + 1]

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
        additional_text = await api_client.get_additional_text_on_mid_test(
            access_token=access_token,
            request=TypificationGetStatisticsRequest(
                answers=answers,
                typification_name=typification_pack_name,
            )
        )
        keyboard: InlineKeyboardMarkup = get_typification_may_end_on_mid_keyboard()  # <закончить типирование!>

    # [ api: get_question ]
    request = TypificationGetQuestion(
        last_answer=question_pack[question_index - 1] + f" {answer}",
        this_question=this_question
    )
    question: str = await api_client.get_next_question(access_token, request=request)

    message_text: str = MessageText.get_typification_process_message(
        False,
        question,
        gender=user.gender,
        additional_text=additional_text
    )

    await message.answer(
        text=message_text,
        reply_markup=keyboard
    )


async def typification_end(
        api_client: PersonalityGPT_APIClient,
        cache_service: CacheService,
        message: Message | CallbackQuery,
        access_token: str,
        typification_key: TypificationPack
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
    typification_pack: dict = get_typification_pack(typification_key)
    characteristics: list[str] = typification_pack["characteristic_groups"]

    answers: list[str] = await cache_service.redis_service.get_typification_answers(
        user_tg_id,
        typification_key=typification_key
    )
    request = TypificationRequest(
        answers=answers,
        characteristics=characteristics
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


@router.callback_query(TypificationEndOnMidCallback.filter())  # закончить преждевременно
async def typification_end_callback(
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
        typification_key=typification_key
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
        typification_key=typification_key
    )


@router.callback_query(DeleteTypificationCallback.filter())
async def delete_typification_progress(
        callback: CallbackQuery,
        callback_data: DeleteTypificationCallback,
        api_client: PersonalityGPT_APIClient,
        access_token: str
):
    """Удалить пройденную типификацию"""
    await callback.answer()

    request = DeleteTypificationRequest(
        typification_name=callback_data.typification_name
    )

    await api_client.delete_typification(
        access_token=access_token,
        request=request
    )
