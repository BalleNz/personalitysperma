from pydantic import BaseModel

from src.core.enums.user import GENDER


class ChangeGenderRequest(BaseModel):
    gender: GENDER
