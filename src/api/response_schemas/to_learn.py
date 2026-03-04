from pydantic import BaseModel, Field


class Characteristic(BaseModel):
    characteristic_name: str = Field(..., description="название характеристики")
    new_characteristic: str = Field(..., description="новая характеристика")


# [ Finish ]

class ToLearnFinishResponse(BaseModel):
    """последняя обработка -> изменение таблиц"""
    new_characteristics: list[Characteristic]
