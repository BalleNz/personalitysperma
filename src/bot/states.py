from aiogram.fsm.state import StatesGroup, State


class States(StatesGroup):

    # [ PERSONALITY ]
    # [ socionics relationships waiting mbti_type]
    MBTI_RELATIONSHIPS_STATE = State()

    # [ TYPIFICATION ]
    Typification = State()
    TypificationEnd = State()
