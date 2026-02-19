from aiogram.filters.callback_data import CallbackData


class GetCharacteristicCallback(CallbackData, prefix="get_char"):
    characteristic_name: str | None = None
    characteristic_group: str | None = None


class BackToListingCallback(CallbackData, prefix="back"):
    pass


class GetFullAccessCallback(CallbackData, prefix="full_access"):
    pass


# [ diary ]
class DiaryPaginationCallback(CallbackData, prefix="pagination"):
    page: int
    arrow: str | None = None  # left / right


class DiaryGetCallback(CallbackData, prefix="diary_get"):
    page: int | None
    diaries_count: int  # количество записей
    current_diary: int | None = None  # текущая запись в нумерации
