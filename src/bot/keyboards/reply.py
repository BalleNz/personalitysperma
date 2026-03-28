from aiogram.types import ReplyKeyboardMarkup, KeyboardButton

from src.bot.lexicon.button_text import ButtonText

MAIN_KEYBOARD: ReplyKeyboardMarkup = ReplyKeyboardMarkup(
    keyboard=[
        [KeyboardButton(text=ButtonText.DIARY)],
        [KeyboardButton(text=ButtonText.MY_CHARACTERISTIC)],
        [KeyboardButton(text=ButtonText.MY_PERSONALITY)],
    ],
    resize_keyboard=True
)
