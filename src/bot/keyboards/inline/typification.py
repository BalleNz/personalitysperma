from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from lexicon.button_text import ButtonText
from src.bot.callbacks.callbacks import GetPersonalityCallback, GetCharacteristicCallback, DeleteTypificationCallback, \
    TypificationEndOnMidCallback, TypificationCallback
from src.bot.message_formatters.characteristic_formatters import CharacteristicGroups, CharacteristicGroup_To_ButtonText
from src.core.lexicon.typifications import TypificationPack
from src.core.schemas.user_schemas import UserSchema


def get_typification_start_keyboard(user: UserSchema) -> InlineKeyboardMarkup | None:
    """Пройти первое типирование"""
    if not user.passed_personality_core:
        return InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text="пройти базовое типирование",
                    callback_data=TypificationCallback(
                        question_pack=TypificationPack.PERSONALITY_CORE,
                        is_passed=False
                    ).pack()
                )
            ]]
        )
    return None


def get_typification_listing_keyboard(user: UserSchema) -> InlineKeyboardMarkup:
    """Генерирует кнопки с актуальным статусом и стилем"""

    passed = {
        TypificationPack.PERSONALITY_CORE: user.passed_personality_core,
        TypificationPack.CAREER_HOLLAND: user.passed_holland,
        TypificationPack.NEURO_DIVERSITY: user.passed_neurodiversity,
        TypificationPack.MOOD_ANXIETY: user.passed_mood_anxiety,
        TypificationPack.LOOKS_DISORDERS: user.passed_body_image_eating,
        TypificationPack.SEX: user.passed_sex_romance,
    }

    mapping = {
        TypificationPack.PERSONALITY_CORE: "Личность",
        TypificationPack.CAREER_HOLLAND: "Карьера",
        TypificationPack.NEURO_DIVERSITY: "Нейроразнообразие",
        TypificationPack.MOOD_ANXIETY: "Беспокойство",
        TypificationPack.LOOKS_DISORDERS: "Недовольство внешностью",
        TypificationPack.SEX: "Предпочтения в сексе",
    }

    buttons = []
    for pack, is_passed in passed.items():
        text = mapping[pack]
        style = "success" if is_passed else "danger"

        buttons.append(
            InlineKeyboardButton(
                text=text,
                callback_data=TypificationCallback(
                    question_pack=pack,
                    is_passed=is_passed
                ).pack(),
                style=style,
                icon_custom_emoji_id="5213134259098761044" if pack == TypificationPack.SEX else None
            )
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[buttons]
    )


def get_typification_delete_progress_keyboard() -> InlineKeyboardMarkup:
    """Удалить прогресс типирования"""
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="удалить прогресс :#",
                callback_data=DeleteTypificationCallback().pack()
            )
        ]]
    )


def get_typification_may_end_on_mid_keyboard() -> InlineKeyboardMarkup:
    """Закончить типирование на середине типирования"""
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="закончить прямо сейчас",
                callback_data=TypificationEndOnMidCallback().pack()
            )
        ]]
    )


def get_characteristics_list_after_typification_end_keyboard(
        characteristic_groups: list[str]
) -> InlineKeyboardMarkup:
    """получить все характеристики после прохождения типирования"""

    buttons: list[InlineKeyboardButton] = []
    for characteristic_group in characteristic_groups:

        text: str = CharacteristicGroup_To_ButtonText[characteristic_group]

        # [ тип личности ]
        if characteristic_group in ("MBTISchema", "HollandCodesSchema", "HexacoSchema"):
            buttons.append(
                InlineKeyboardButton(
                    text=text,
                    callback_data=GetPersonalityCallback(
                        characteristic_name=characteristic_group
                    ).pack()
                )
            )
            continue

        buttons.append(
            InlineKeyboardButton(
                text=text,
                callback_data=GetCharacteristicCallback(
                    characteristic_name=characteristic_group if characteristic_group not in CharacteristicGroups else None,
                    characteristic_group=characteristic_group if characteristic_group in CharacteristicGroups else None
                ).pack()
            )
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[buttons]
    )
