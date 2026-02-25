from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from callbacks.callbacks import GetFullAccessCallback
from lexicon.button_text import ButtonText

from src.bot.callbacks.callbacks import SelectGenderCallback
from src.core.enums.user import GENDER

gender_select_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text="парень",
                callback_data=SelectGenderCallback(gender=GENDER.MALE).pack()
            ),
            InlineKeyboardButton(
                text="девочка ^^",
                callback_data=SelectGenderCallback(gender=GENDER.GIRL).pack()
            ),
            InlineKeyboardButton(
                text="walking glitch",
                callback_data=SelectGenderCallback(gender=GENDER.NEUTRAL).pack()
            )
        ]
    ]
)


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
