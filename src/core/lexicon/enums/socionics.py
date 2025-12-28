from enum import Enum


class Club(str, Enum):
    RESEARCHERS = "researchers"
    SOCIALS = "socials"
    PRACTICALS = "practicals"
    HUMANITARIANS = "humanitarians"


class SocionicsType(str, Enum):
    # Русские обозначения
    ILE = "ИЛЭ"  # Дон Кихот
    SEI = "СЭИ"  # Дюма
    ESE = "ЭСЭ"  # Гюго
    LII = "ЛИИ"  # Робеспьер
    SLE = "СЛЭ"  # Жуков
    IEI = "ИЭИ"  # Есенин
    EIE = "ЭИЭ"  # Гамлет
    LSI = "ЛСИ"  # Максим Горький
    SEE = "СЭЭ"  # Наполеон
    ILI = "ИЛИ"  # Бальзак
    LIE = "ЛИЭ"  # Джек Лондон
    ESI = "ЭСИ"  # Драйзер
    LSE = "ЛСЭ"  # Штирлиц
    EII = "ЭИИ"  # Достоевский
    IEE = "ИЭЭ"  # Гексли
    SLI = "СЛИ"  # Габен


# ============ МЕЖТИПНЫЕ ОТНОШЕНИЯ ============
class RelationshipType(str, Enum):
    """14 типов интертипных отношений в соционике"""
    DUAL = "Дуальные"
    CONFLICT = "Конфликтные"
    ACTIVATION = "Активационные"
    MIRROR = "Зеркальные"
    IDENTICAL = "Идентичные"
    KIND_RED = "Родственные"
    BUSINESS = "Деловые"
    SUPERVISEE = "Подопечный"
    SUPERVISOR = "Ревизор"
    ILLUSORY = "Миражные"
    SEMI_DUAL = "Полудуальные"
    QUASI_IDENTICAL = "Квазитождественные"
    SUPER_EGO = "Суперэго"
    OTHER = "Другие"
