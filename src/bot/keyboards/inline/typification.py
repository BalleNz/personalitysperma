from aiogram.types import InlineKeyboardMarkup, InlineKeyboardButton

from src.bot.callbacks.callbacks import TypificationPreRollCallback, \
    ReturnToCharacteristicListingAfterTypificationPassedCallback, GetPersonalityCallback, GetCharacteristicCallback, \
    DeleteTypificationCallback, TypificationEndOnMidCallback, TypificationCallback
from src.bot.lexicon.button_text import ButtonText
from src.bot.message_formatters.characteristic_formatters import CharacteristicGroup_To_ButtonText
from src.core.lexicon.typifications import TypificationPack
from src.core.schemas.user_schemas import UserSchema


def get_return_to_listing_after_typification_keyboard(typification_name: TypificationPack) -> InlineKeyboardMarkup:
    """возврат в листинг характеристик после типирования"""
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text=ButtonText.ARROW_LEFT,
                callback_data=ReturnToCharacteristicListingAfterTypificationPassedCallback(
                    typification_name=typification_name
                ).pack()
            )
        ]]
    )


def get_typification_PERSONALITY_CORE_preroll_keyboard(user: UserSchema) -> InlineKeyboardMarkup | None:
    """Пройти первое типирование"""
    if not user.passed_personality_core:
        return InlineKeyboardMarkup(
            inline_keyboard=[[
                InlineKeyboardButton(
                    text="пройти базовое типирование",
                    callback_data=TypificationPreRollCallback(
                        typification_name=TypificationPack.PERSONALITY_CORE,
                        is_passed=False
                    ).pack()
                )
            ]]
        )
    return None


def get_typification_start_keyboard(
        typification_name: TypificationPack
) -> InlineKeyboardMarkup:
    """ВО ВРЕМЯ ПРЕРОЛЛА"""
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="начать типирование",
                callback_data=TypificationCallback(
                    typification_name=typification_name,
                    is_passed=False
                ).pack()
            )
        ]]
    )


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
            [
                InlineKeyboardButton(
                    text=text,
                    callback_data=TypificationPreRollCallback(
                        typification_name=pack,
                        is_passed=is_passed
                    ).pack(),
                    style=style,
                    icon_custom_emoji_id="5213134259098761044" if pack == TypificationPack.SEX else None
                )
            ]
        )

    return InlineKeyboardMarkup(
        inline_keyboard=buttons
    )


def get_typification_delete_progress_keyboard(
        typification_pack_name: TypificationPack
) -> InlineKeyboardMarkup:
    """Удалить прогресс типирования"""
    return InlineKeyboardMarkup(
        inline_keyboard=[[
            InlineKeyboardButton(
                text="удалить прогресс :#",
                callback_data=DeleteTypificationCallback(
                    typification_name=typification_pack_name
                ).pack()
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
                    characteristic_group=characteristic_group
                ).pack()
            )
        )

    return InlineKeyboardMarkup(
        inline_keyboard=[buttons]
    )
