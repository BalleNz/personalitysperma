from aiogram.filters.callback_data import CallbackData

from src.core.enums.user import GENDER
from src.core.lexicon.typifications import TypificationPack


# [ START ]
class SelectGenderCallback(CallbackData, prefix="gender_select"):
    gender: GENDER


# [ SURVEY ]
class SurveyAnswerCallback(CallbackData, prefix="surv_ans"):
    answer_hash: str
    characteristic_names: str


# [ CHARACTERISTICS ]
class GetCharacteristicCallback(CallbackData, prefix="get_char"):
    characteristic_name: str | None = None
    characteristic_group: str | None = None


class GetClinicalListingCallback(CallbackData, prefix="get_clinical"):
    pass


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


class SocionicsRelationshipsWaitingCallback(CallbackData, prefix="socionics_relationships"):
    mbti_type: str  # тип для сравнения с другими


# [ DIARY ]
class DiaryPaginationCallback(CallbackData, prefix="pagination"):
    page: int
    arrow: str | None = None  # left / right


class DiaryGetCallback(CallbackData, prefix="diary_get"):
    page: int | None
    diaries_count: int  # количество записей
    current_diary: int | None = None  # текущая запись в нумерации


# [ ТИПИРОВАНИЕ ]

class TypificationListingCallback(CallbackData, prefix="typification_listing"):
    """Листинг типирований"""
    pass


class ReturnToCharacteristicListingAfterTypificationPassedCallback(CallbackData, prefix="listing_after_typif"):
    """Возврат к листингу полученных характеристик после типирования"""
    typification_name: TypificationPack


class TypificationCallback(CallbackData, prefix="typification_start"):
    """После кнопки с выбором типирования"""
    question_index: str | None = None  # индекс вопроса
    question_pack: TypificationPack
    is_passed: bool


class TypificationAlreadyPassedCallback(CallbackData, prefix="typification_passed"):
    """типификация уже пройдена"""
    pass


class TypificationEndOnMidCallback(CallbackData, prefix="typification_end_on_mid"):
    """закончить на середине тест"""
    pass


class DeleteTypificationCallback(CallbackData, prefix="typification_delete_progress"):
    """удалить прогресс типификации"""
    pass
