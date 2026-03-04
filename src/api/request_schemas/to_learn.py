from pydantic import BaseModel, Field

from src.api.response_schemas.to_learn import Characteristic


class ToLearnSurveyRequest(BaseModel):
    user_message: str = Field(..., description="Сообщение юзера")

# [ Finish ]


class AnswerPacks(BaseModel):
    """паки с вопросами: ответы и характеристики"""
    answer: str = Field(..., description="один из ответов")
    characteristics: list[str] = Field(..., description="какие характеристики (таблицы) будут затронуты")


class QuestionPack(BaseModel):
    """паки с вопросами"""
    question: str = Field(..., description="вопрос")
    answer_packs: list[AnswerPacks]


class ToLearnSurveyResponse(BaseModel):
    user_answer: str = Field(..., description="ответ пользователю (для продолжения диалога)")
    question_pack: QuestionPack


class ToLearnFinishRequest(BaseModel):
    """Запрос на обработку ответа на вопрос юзером"""
    question: str = Field(...)
    answer: str = Field(...)
    characteristics: list[Characteristic]
