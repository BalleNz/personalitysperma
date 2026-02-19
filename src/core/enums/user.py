from enum import Enum


class TALKING_MODES(str, Enum):
    RESEARCH = "research"  # изучение себя
    INDIVIDUAL_PSYCHO = "psycho"  # индивидуальный психолог


class GENDER(str, Enum):
    MALE = "male"
    GIRL = "girl"
    NEUTRAL = "neutral"
