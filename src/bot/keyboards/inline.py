from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.callbacks.callbacks import GetCharacteristicCallback, BackToListingCallback, GetFullAccessCallback
from src.bot.lexicon.button_text import ButtonText

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


def get_characteristic_listing_keyboard() -> InlineKeyboardMarkup:
    CHARACTERISTIC_LISTING_KEYBOARD: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=ButtonText.TRAITS_CORE,
                    callback_data=GetCharacteristicCallback(
                        characteristic_name="EmotionalProfileSchema"  # мб потом сделать чище
                    ).pack()
                ),
            ],
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
