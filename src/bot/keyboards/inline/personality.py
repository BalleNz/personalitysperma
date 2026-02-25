from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.callbacks.callbacks import BackToListingPersonalityCallback, GetPersonalityCallback, SocionicsReininCallback
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


def get_personality_types_keyboard(
) -> InlineKeyboardMarkup:
    buttons = [
        [
            InlineKeyboardButton(
                text=ButtonText.SOCIONICS,
                callback_data=GetPersonalityCallback(
                    characteristic_name="UserSocionicsSchema"
                ).pack()
            )],
        [
            InlineKeyboardButton(
                text=ButtonText.HEXACO,
                callback_data=GetPersonalityCallback(
                    characteristic_name="UserHexacoSchema"
                ).pack()
            )
        ],
        [
            InlineKeyboardButton(
                text=ButtonText.HOLLAND_CODES,
                callback_data=GetPersonalityCallback(
                    characteristic_name="UserHollandCodesSchema"
                ).pack()
            )
        ]
    ]
    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


def get_socionics_keyboard(

) -> InlineKeyboardMarkup:
    """клавиатуры для Соционики"""
    buttons: list = list()

    buttons.append(
        [InlineKeyboardButton(
            text=ButtonText.SOCIONICS_REININ,
            callback_data=SocionicsReininCallback().pack()
        )]
    )

    # buttons.append(
    #     [InlineKeyboardButton(
    #         text=ButtonText.SOCIONICS_RELATIONSHIPS,
    #         callback_data=SocionicsRelationshipsCallback().pack()
    #     )]
    # )

    buttons.append(
        [InlineKeyboardButton(
            text=ButtonText.ARROW_LEFT,
            callback_data=BackToListingPersonalityCallback().pack()
        )]
    )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )
