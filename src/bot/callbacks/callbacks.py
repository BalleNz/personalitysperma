from aiogram.filters.callback_data import CallbackData


class GetCharacteristicCallback(CallbackData, prefix="get_char"):
    characteristic_name: str
