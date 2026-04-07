from pydantic import BaseModel, Field

from src.core.lexicon.typifications import TypificationPack


class TypificationRequest(BaseModel):
    answers: list[str] = Field(...)
    characteristics: list[str] = Field(...)
    typification_name: TypificationPack


class TypificationGetStatisticsRequest(BaseModel):
    answers: list[str] = Field(...)
    typification_name: TypificationPack


class TypificationAssistantRequest(BaseModel):
    user_name: str = Field(..., description="имя пользователя")
    answers: list[str] = Field(...)


class TypificationGetQuestion(BaseModel):
    last_answer: str = Field(..., description="последний ответ юзера")
    this_question: str = Field(..., description="следующий вопрос")
    gender: str = Field(..., description="пол пользователя")  # "female" | "male" | "non_binary"


class DeleteTypificationRequest(BaseModel):
    typification_name: TypificationPack
