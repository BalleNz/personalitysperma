from typing import Any

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
