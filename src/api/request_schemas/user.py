from pydantic import BaseModel

from src.core.enums.user import GENDER, TALKING_MODES


class ChangeGenderRequest(BaseModel):
    gender: GENDER


class ChangeTalkModeRequest(BaseModel):
    talk_mode: TALKING_MODES
