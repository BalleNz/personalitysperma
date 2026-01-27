from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot.lexicon.button_text import ButtonText

MAIN_KEYBOARD: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=ButtonText.CHARACTETISTIC_LISTING)],
        [KeyboardButton(text=ButtonText.MY_PERSONALITY_TYPES)],
    ],
    resize_keyboard=True
)