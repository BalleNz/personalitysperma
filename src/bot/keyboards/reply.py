from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot.lexicon.button_text import ButtonText

MAIN_KEYBOARD_PSYCHO: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=ButtonText.PSYCHO_MODE)],
        [KeyboardButton(text=ButtonText.DIARY)],
        [KeyboardButton(text=ButtonText.MY_PERSONALITY)],
        [KeyboardButton(text=ButtonText.MY_TYPES)],
    ],
    resize_keyboard=True
)

MAIN_KEYBOARD_RESEARCH: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=ButtonText.RESEARCH_MODE)],
        [KeyboardButton(text=ButtonText.DIARY)],
        [KeyboardButton(text=ButtonText.MY_PERSONALITY)],
        [KeyboardButton(text=ButtonText.MY_TYPES)],
    ],
    resize_keyboard=True
)
