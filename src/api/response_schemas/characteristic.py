from pydantic import BaseModel, Field

from src.infrastructure.database.models.base import S


class CharacteristicResponseRaw(BaseModel):
    type: str = Field(..., description="тип характеристики")
    characteristics: list[S] = Field(..., description="последние две записи")


class GetAllCharacteristicResponse(BaseModel):
    response: list[CharacteristicResponseRaw]
