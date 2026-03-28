from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.callbacks.callbacks import (
    SocionicsRelationshipsWaitingCallback, BackToListingPersonalityCallback, GetPersonalityCallback,
    SocionicsReininCallback
)
from src.bot.lexicon.button_text import ButtonText

back_to_personality_listing_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=ButtonText.ARROW_LEFT,
                callback_data=BackToListingPersonalityCallback().pack()
            )
        ]
    ]
)
back_to_socionics_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=ButtonText.ARROW_LEFT,
                callback_data=GetPersonalityCallback(characteristic_name="UserSocionicsSchema").pack()
            )
        ]
    ]
)


def get_personality_types_keyboard() -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=ButtonText.MBTI,
                callback_data=GetPersonalityCallback(
                    characteristic_name="MBTISchema"
                ).pack()
            )],
        [
            InlineKeyboardButton(
                text=ButtonText.HEXACO,
                callback_data=GetPersonalityCallback(
                    characteristic_name="HexacoSchema"
                ).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text=ButtonText.HOLLAND_CODES,
                callback_data=GetPersonalityCallback(
                    characteristic_name="HollandCodesSchema"
                ).pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


def get_mbti_keyboard(
        mbti_type: str
) -> InlineKeyboardMarkup:
    """клавиатуры для Соционики"""
    buttons: list = list()

    buttons.append(
        [InlineKeyboardButton(
            text=ButtonText.SOCIONICS_REININ,
            callback_data=SocionicsReininCallback().pack()
        )]
    )

    buttons.append(
        [InlineKeyboardButton(
            text=ButtonText.SOCIONICS_RELATIONSHIPS,
            callback_data=SocionicsRelationshipsWaitingCallback(
                mbti_type=mbti_type
            ).pack()
        )]
    )

    buttons.append(
        [InlineKeyboardButton(
            text=ButtonText.ARROW_LEFT,
            callback_data=BackToListingPersonalityCallback().pack()
        )]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


def get_about_mbti(
    passed_typing: bool
) -> InlineKeyboardMarkup:
    """Возвращает клавиатуру с кнопкой 'Пройти типирование' или 'MBTI тип'"""
    button: InlineKeyboardButton

    if not passed_typing:
        button = InlineKeyboardButton(
            text=ButtonText.MBTI_GET_TEST,
            callback_data=...  # TODO
        )
    else:
        button = InlineKeyboardButton(
            text=ButtonText.MBTI_ABOUT,
            callback_data=GetPersonalityCallback(
                characteristic_name="MBTISchema"
            ).pack()
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[[button]]
    )
