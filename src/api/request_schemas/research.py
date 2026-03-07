from pydantic import BaseModel, Field

from src.api.response_schemas.research import Characteristic

# [ DEFAULT ]


class ResearchDefaultRequest(BaseModel):
    user_message: str = Field(..., description="Сообщение юзера")


# [ SURVEY ]


class ResearchSurveyRequest(BaseModel):
    user_message: str = Field(..., description="Сообщение юзера")


class ResearchSurveyFinishRequest(BaseModel):
    """Запрос на обработку ответа на вопрос юзером"""
    question: str = Field(..., description="Вопрос юзеру")
    answer: str = Field(..., description="Ответ, который выбрал юзер")
    characteristics: list[Characteristic] = Field(..., description="Текущие характеристики юзера")
