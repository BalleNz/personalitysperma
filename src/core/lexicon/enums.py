from enum import Enum


# [ SQLAlchemy ]
class TablesClassificationType(str, Enum):
    """Названия таблиц"""
    DARK_TRIAD = "DarkTriad"
    HUMOR_SENSE = "HumorSense"
    SEXUAL_PREFERENCE = "SexualPreference"
    COGNITIVE_PROFILE = "CognitiveProfile"
    EMOTIONAL_PROFILE = "EmotionalProfile"
    ATTACHMENT_STYLE = "AttachmentStyle"
    LOVE_LANGUAGE = "LoveLanguage"
    PERSONALITY_TRAITS = "PersonalityTraits"


class HumorStyleEnum(str, Enum):
    """Перечисление доминирующих стилей юмора (основные категории для категоризации)"""
    AFFILIATIVE = "affiliative"  # Юмор для укрепления связей, дружеский, игривый
    SELF_ENHANCING = "self_enhancing"  # Юмор для поднятия настроения себе, оптимистичный
    AGGRESSIVE = "aggressive"  # Юмор за счет других, сарказм, насмешка
    SELF_DEFEATING = "self_defeating"  # Самоирония, юмор за свой счет
    NONE = "none"  # Нет выраженного стиля
