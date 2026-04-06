from pydantic import BaseModel, Field


class CheckInRequest(BaseModel):
    message: str = Field(..., description="сообщение юзера")
    talk_mode_input: str = Field(..., description="режим юзера")
