from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.callbacks.callbacks import GetCharacteristicCallback
from src.bot.lexicon.button_text import ButtonText
from src.core.schemas.traits.traits_core import CognitiveProfileSchema, SocialProfileSchema, BehavioralProfileSchema
from src.core.schemas.traits.traits_core import EmotionalProfileSchema


def get_characteristic_listing_keyboard() -> InlineKeyboardMarkup:
    CHARACTERISTIC_LISTING_KEYBOARD: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[
            [
                InlineKeyboardButton(
                    text=ButtonText.EMOTIONAL_CHARACTERISTIC,
                    callback_data=GetCharacteristicCallback(
                        characteristic_name=EmotionalProfileSchema.__name__
                    ).pack()
                ),
            ],
            [
                InlineKeyboardButton(
                    text=ButtonText.BEHAVIORAL_CHARACTERISTIC,
                    callback_data=GetCharacteristicCallback(
                        characteristic_name=BehavioralProfileSchema.__name__
                    ).pack()
                ),
            ],
            [
                InlineKeyboardButton(
                    text=ButtonText.SOCIAL_CHARACTERISTIC,
                    callback_data=GetCharacteristicCallback(
                        characteristic_name=SocialProfileSchema.__name__
                    ).pack()
                ),
            ],
            [
                InlineKeyboardButton(
                    text=ButtonText.COGNITIVE_CHARACTERISTIC,
                    callback_data=GetCharacteristicCallback(
                        characteristic_name=CognitiveProfileSchema.__name__
                    ).pack()
                ),
            ],
        ]
    )

    return CHARACTERISTIC_LISTING_KEYBOARD
