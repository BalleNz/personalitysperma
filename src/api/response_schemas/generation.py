from pydantic import BaseModel


class CheckInResponse(BaseModel):
    """ответ от check in:
    — таблицы, которые следует обновить
    """

    # TODO special classifications

    classifications: list[str]
    precise_question: str
