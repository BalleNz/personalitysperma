from pydantic import BaseModel, Field


class PsychoRequest(BaseModel):
    message: str = Field(..., description="сообщение юзера")
