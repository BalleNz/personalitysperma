from aiogram.filters.callback_data import CallbackData


class GetCharacteristicCallback(CallbackData, prefix="get_char"):
    characteristic_name: str | None = None
    characteristic_group: str | None = None


class BackToListingCallback(CallbackData, prefix="back"):
    pass


class GetFullAccessCallback(CallbackData, prefix="full_access"):
    pass
