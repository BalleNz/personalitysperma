from pydantic import BaseModel, Field

# [ ITEMS ]


class Characteristic(BaseModel):
    characteristic_name: str = Field(..., description="название характеристики")
    characteristic: dict = Field(..., description="характеристика юзера JSON (прошлая или новая)")


class AnswerPacks(BaseModel):
    """паки с вопросами: ответы и характеристики"""
    answer: str = Field(..., description="один из ответов")
    characteristics: list[str] = Field(..., description="какие характеристики (таблицы) будут затронуты")


class QuestionPack(BaseModel):
    """паки с вопросами"""
    question: str = Field(..., description="вопрос")
    answer_packs: list[AnswerPacks]


# [ SURVEY ]


class ResearchSurveyFinishResponse(BaseModel):
    """последняя обработка -> изменение таблиц"""
    user_answer: str = Field(..., description="ответ пользователю (для продолжения диалога)")
    new_characteristics: list[Characteristic]
