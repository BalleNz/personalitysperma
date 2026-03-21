from pydantic import BaseModel, Field


class PsychoResponse(BaseModel):
    """ответ от check in:
    — таблицы, которые следует обновить
    """

    classifications: list[str] | None
    user_answer: str = Field(..., description="ответ пользователю (для продолжения диалога)")
