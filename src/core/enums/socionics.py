from enum import Enum


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
