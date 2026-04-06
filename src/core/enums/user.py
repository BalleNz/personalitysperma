from enum import Enum


class TALKING_MODES(str, Enum):
    RESEARCH = "research"  # изучение себя
    INDIVIDUAL_PSYCHO = "psycho"  # индивидуальный психолог


class TALKING_MODES_CHECK_IN(str, Enum):
    RESEARCH = "research"
    INDIVIDUAL_PSYCHO = "psycho"
    LONG = "long"
    SURVEY = "survey"


class GENDER(str, Enum):
    MALE = "male"
    GIRL = "girl"
    NEUTRAL = "neutral"

    WOMAN = "woman"
    MAN = "man"

    NON_BINARY = "non_binary"
    TRANSGENDER = "transgender"
    GENDERQUEER = "genderqueer"
    GENDERFLUID = "genderfluid"
    AGENDER = "agender"
    OTHER = "other"
    PREFER_NOT_TO_SAY = "prefer_not_to_say"
