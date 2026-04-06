from typing import Any

from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.callbacks.callbacks import GetClinicalListingCallback, BackToListingCharacteristicCallback, \
    GetCharacteristicCallback
from src.bot.lexicon.button_text import ButtonText

back_to_characteristic_listing_keyboard = InlineKeyboardMarkup(
    inline_keyboard=[
        [
            InlineKeyboardButton(
                text=ButtonText.ARROW_LEFT,
                callback_data=BackToListingCharacteristicCallback().pack()
            )
        ]
    ]
)


def get_characteristic_listing_keyboard(
        user_characteristics: dict[str, dict[str, Any]]  # schema_name: list[schema_json, schema_json]
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
                text=ButtonText.BASIC,
                callback_data=GetCharacteristicCallback(
                    characteristic_group="basic"
                ).pack()
            ),
        )

    clinical_traits: tuple[str, ...] = (
        "AutismSchema",
        "ADHDSchema",
        "DepressionDisorderSchema",
        "BipolarDisorderSchema",
        "BPDSchema",
        "DissociativeSchema",
        "PanicSchema",
        "GDRSchema",
        "PTSDSchema",
        "LooksSchema",
        "EatingSchema",
    )

    if any(key in user_characteristics for key in clinical_traits):
        buttons.append(
            InlineKeyboardButton(
                text="👨🏻‍⚕️ Клинический профиль",
                callback_data=GetClinicalListingCallback().pack()
            )
        )

    if "HumorProfileSchema" in user_characteristics:
        buttons.append(
            InlineKeyboardButton(
                text="Чувство юмора",
                callback_data=GetCharacteristicCallback(
                    characteristic_group="humor"
                ).pack()
            )
        )

    triads_traits: list[str] = ["DarkTriadsSchema", "LightTriadsSchema"]
    if any(key in user_characteristics for key in triads_traits):
        buttons.append(
            InlineKeyboardButton(
                text="Тёмная и Светлая триады",
                callback_data=GetCharacteristicCallback(
                    characteristic_group="triads"
                ).pack()
            )
        )

    CHARACTERISTIC_LISTING_KEYBOARD: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[btn] for btn in buttons]
    )

    return CHARACTERISTIC_LISTING_KEYBOARD


def get_clinical_listing_keyboard(
        user_characteristics: dict
) -> InlineKeyboardMarkup:
    """КЛИНИЧЕСКИЙ ПРОФИЛЬ"""
    buttons: list[InlineKeyboardButton] = []

    neuro_traits: list[str] = ["AutismSchema", "ADHDSchema"]
    if any(key in user_characteristics for key in neuro_traits):
        buttons.append(
            InlineKeyboardButton(
                text="Нейроотличия (Аутизм, СДВГ)",
                callback_data=GetCharacteristicCallback(
                    characteristic_group="neuro"
                ).pack()
            )
        )

    mood_traits: list[str] = ["DepressionDisorderSchema", "BipolarDisorderSchema"]
    if any(key in user_characteristics for key in mood_traits):
        buttons.append(
            InlineKeyboardButton(
                text="Депрессия и биполярка",
                callback_data=GetCharacteristicCallback(
                    characteristic_group="mood_disorder"
                ).pack()
            )
        )

    if "BPDSchema" in user_characteristics:
        buttons.append(
            InlineKeyboardButton(
                text="Пограничное расстройство личности",
                callback_data=GetCharacteristicCallback(
                    characteristic_group="bpd"
                ).pack()
            )
        )

    if "DissociativeSchema" in user_characteristics:
        buttons.append(
            InlineKeyboardButton(
                text="Нарушения личности",
                callback_data=GetCharacteristicCallback(
                    characteristic_group="dissociative"
                ).pack()
            )
        )

    anxiety_traits: list[str] = ["PanicSchema", "GDRSchema", "PTSDSchema"]
    if any(key in user_characteristics for key in anxiety_traits):
        buttons.append(
            InlineKeyboardButton(
                text="Тревога и стресс",
                callback_data=GetCharacteristicCallback(
                    characteristic_group="anxiety"
                ).pack()
            )
        )

    body_traits: list[str] = ["LooksSchema", "EatingSchema"]
    if any(key in user_characteristics for key in body_traits):
        buttons.append(
            InlineKeyboardButton(
                text="Дисморфофобия и РПП",
                callback_data=GetCharacteristicCallback(
                    characteristic_group="looks"
                ).pack()
            )
        )

    buttons.append(
        InlineKeyboardButton(
            text=ButtonText.ARROW_LEFT,
            callback_data=BackToListingCharacteristicCallback().pack()
        )
    )

    CHARACTERISTIC_LISTING_KEYBOARD: InlineKeyboardMarkup = InlineKeyboardMarkup(
        inline_keyboard=[[btn] for btn in buttons]
    )

    return CHARACTERISTIC_LISTING_KEYBOARD
