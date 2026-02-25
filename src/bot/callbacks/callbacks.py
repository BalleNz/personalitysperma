from aiogram.filters.callback_data import CallbackData

from src.core.enums.user import GENDER


# [ START ]
class SelectGenderCallback(CallbackData, prefix="gender_select"):
    gender: GENDER


# [ CHARACTERISTICS ]
class GetCharacteristicCallback(CallbackData, prefix="get_char"):
    characteristic_name: str | None = None
    characteristic_group: str | None = None


class GetPersonalityCallback(CallbackData, prefix="get_persn"):
    characteristic_name: str | None = None


class BackToListingPersonalityCallback(CallbackData, prefix="pers_back"):
    pass


class BackToListingCharacteristicCallback(CallbackData, prefix="charact_back"):
    pass


class GetFullAccessCallback(CallbackData, prefix="full_access"):
    pass


# [ SOCIONICS ]
class SocionicsReininCallback(CallbackData, prefix="socionics_reinin"):
    pass


class SocionicsRelationshipsCallback(CallbackData, prefix="socionics_relationships"):
    mbti_2: str  # с кем ищем совместимость


# [ DIARY ]
class DiaryPaginationCallback(CallbackData, prefix="pagination"):
    page: int
    arrow: str | None = None  # left / right


class DiaryGetCallback(CallbackData, prefix="diary_get"):
    page: int | None
    diaries_count: int  # количество записей
    current_diary: int | None = None  # текущая запись в нумерации
