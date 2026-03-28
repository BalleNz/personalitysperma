from pydantic import BaseModel, Field

from src.core.enums.user import TALKING_MODES
from src.api.response_schemas.survey import QuestionPack


class AssistantResponse(BaseModel):
    """
    ответ от check in:
        — таблицы, которые следует обновить
        — ответ юзеру
        — возможно: survey: question pack
    """

    classifications: list[str] | None = Field(None, description="Какие характеристики нужно обновить")
    user_answer: str | None = Field(None, description="Ответ пользователю (для продолжения диалога)")
    question_pack: QuestionPack | None = Field(None, description="Пак вопросов в режиме survey")
    about_mbti: bool | None = False


class CheckInResponse(BaseModel):
    """Список характеристик которые нужно учитывать"""

    characteristics_list: list[str]
    talk_mode: TALKING_MODES
    about_mbti: bool | None = False
