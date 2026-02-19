from typing import Any

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.callbacks.callbacks import GetCharacteristicCallback, BackToListingCallback, GetFullAccessCallback, \
    DiaryPaginationCallback, DiaryGetCallback
from src.bot.lexicon.button_text import ButtonText
from src.core.consts import DIARIES_ROW_COUNT_AT_KEYBOARD
from src.core.schemas.diary_schema import DiarySchema

back_from_listing_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=ButtonText.ARROW_LEFT,
                callback_data=BackToListingCallback().pack()
            )
        ]
    ]
)


def get_diary_listing_keyboard(
        diaries: list[DiarySchema],
        page: int,
        per_page: int = DIARIES_ROW_COUNT_AT_KEYBOARD,
) -> InlineKeyboardMarkup:
    """Листинг записей дневника"""
    buttons: list = []

    buttons_row: list = []
    for i in range(len(diaries)):
        if buttons_row.__len__() > per_page:
            buttons += [buttons_row]
            buttons_row = []

        # [ vars ]
        diary = diaries[i]
        date_str = diary.created_at.strftime("%d.%m")

        buttons_row.append(
            InlineKeyboardButton(
                text=date_str,
                callback_data=DiaryGetCallback(
                    page=page,
                    diaries_count=diaries.__len__(),
                    current_diary=diaries.index(diary)
                ).pack()
            )
        )

        if i == len(diaries) - 1:
            buttons += [buttons_row]

    buttons_pagination = []
    if len(buttons) > 1:
        if page < len(buttons) - 1:
            buttons_pagination += [
                InlineKeyboardButton(
                    text=ButtonText.ARROW_LEFT,
                    callback_data=DiaryPaginationCallback(
                        arrow=ButtonText.ARROW_RIGHT,
                        page=page
                    ).pack())
            ]
        if page > 0:
            buttons_pagination += [
                InlineKeyboardButton(
                    text=ButtonText.ARROW_RIGHT,
                    callback_data=DiaryPaginationCallback(
                        arrow=ButtonText.ARROW_LEFT,
                        page=page
                    ).pack()
                )]

    return InlineKeyboardMarkup(
        inline_keyboard=[buttons[page][::-1]] + [buttons_pagination]
    )


def get_diary_entry_keyboard(
        diaries_count: int,
        page: int,
        current_diary: int  # текущая запись
) -> InlineKeyboardMarkup:
    """Клавиатура при просмотре одной записи дневника
    кнопки:
    — листинг
    — назад"""
    buttons = []

    pagination_row = []
    if current_diary < diaries_count - 1:
        pagination_row.append(
            InlineKeyboardButton(
                text=ButtonText.ARROW_LEFT,
                callback_data=DiaryGetCallback(
                    current_diary=current_diary + 1,
                    diaries_count=diaries_count,
                    page=page
                ).pack()
            )
        )

    if current_diary > 0:
        pagination_row.append(
            InlineKeyboardButton(
                text=ButtonText.ARROW_RIGHT,
                callback_data=DiaryGetCallback(
                    current_diary=current_diary - 1,
                    diaries_count=diaries_count,
                    page=page
                ).pack()
            )
        )

    if pagination_row:
        buttons.append(pagination_row)

    buttons.append(
        [
            InlineKeyboardButton(
                text="Вернуться в листинг",
                callback_data=DiaryPaginationCallback(page=0).pack()
            )
        ]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


def get_characteristic_listing_keyboard(
        user_characteristics: dict[str, dict[str, Any]]  # schema_name: schema_json
) -> InlineKeyboardMarkup:
    # [ проверка на существование характеристик ]

    buttons: list[InlineKeyboardButton] = []

    # [ если есть хоть одна хар-ка из basic ]
    base_traits: list[str] = [
        "EmotionalProfileSchema",
        "SocialProfileSchema",
        "CognitiveProfileSchema",
        "BehavioralProfileSchema"
    ]
    if any(
            any(sub in key for sub in base_traits) for key in user_characteristics
    ):  # [ для TRAITS BASIC ]
        buttons.append(
            InlineKeyboardButton(
                text=ButtonText.TRAITS_BASIC,
                callback_data=GetCharacteristicCallback(
                    characteristic_group="basic"
                ).pack()
            ),
        )

    CHARACTERISTIC_LISTING_KEYBOARD: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            buttons
        ]
    )

    return CHARACTERISTIC_LISTING_KEYBOARD


def get_full_access_keyboard() -> InlineKeyboardMarkup:
    GET_FULL_ACCESS_KEYBOARD: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=ButtonText.GET_FULL_ACCESS,
                    callback_data=GetFullAccessCallback().pack()
                )
            ]
        ]
    )

    return GET_FULL_ACCESS_KEYBOARD
