from pydantic import BaseModel, Field


class CheckInRequest(BaseModel):
    message: str = Field(..., description="сообщение юзера")
