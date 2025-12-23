from enum import Enum


class HumorStyleEnum(str, Enum):
    """Перечисление доминирующих стилей юмора (основные категории для категоризации)"""
    AFFILIATIVE = "affiliative"  # Юмор для укрепления связей, дружеский, игривый
    SELF_ENHANCING = "self_enhancing"  # Юмор для поднятия настроения себе, оптимистичный
    AGGRESSIVE = "aggressive"  # Юмор за счет других, сарказм, насмешка
    SELF_DEFEATING = "self_defeating"  # Самоирония, юмор за свой счет
    NONE = "none"  # Нет выраженного стиля


# [ Dark Triads ]
class DarkTriadsTypes(str, Enum):
    CYNICISM = "cynicism"
    NARCISSISM = "narcissism"
    MACHIAVELLIANISM = "machiavellianism"
    PSYCHOTICISM = "psychoticism"
