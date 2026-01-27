from pydantic import BaseModel, Field

from src.infrastructure.database.models.base import S


class CharacteristicResponseRaw(BaseModel):
    type: str = Field(..., description="тип характеристики")
    characteristic: S = Field(...)


class GetAllCharacteristicResponse(BaseModel):
    response: list[CharacteristicResponseRaw]
