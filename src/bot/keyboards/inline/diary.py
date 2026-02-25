from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.callbacks.callbacks import DiaryGetCallback, DiaryPaginationCallback
from src.bot.lexicon.button_text import ButtonText
from src.core.consts import DIARIES_ROW_COUNT_AT_KEYBOARD
from src.core.schemas.diary_schema import DiarySchema


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
