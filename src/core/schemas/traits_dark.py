from typing import Optional
from uuid import UUID

from pydantic import Field, ConfigDict, BaseModel, computed_field

from core.lexicon.enums import DarkTriadsTypes


class DarkTriadsSchema(BaseModel):
    """Схема темной триады (цинизм, нарциссизм, макиавеллизм, психотизм)"""
    model_config = ConfigDict(from_attributes=True)

    id: Optional[UUID] = None
    user_id: Optional[UUID] = None

    cynicism: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Цинизм: доверие → недоверие к мотивам других людей (0=доверчивый, 1=циничный)"
    )
    narcissism: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Нарциссизм: скромность → самолюбование (0=скромный, 1=нарциссичный)"
    )
    machiavellianism: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Макиавеллизм: прямота → манипулятивность (0=прямой, 1=манипулятивный)"
    )
    psychoticism: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Психотизм: нормальность → необычный опыт (0=нормальный, 1=психотичный)"
    )

    @computed_field
    @property
    def total_score(self) -> float | None:
        """Вычисляемое поле: общий балл"""
        values = [self.cynicism, self.narcissism,
                  self.machiavellianism, self.psychoticism]
        valid_values = [v for v in values if v is not None]

        if not valid_values:
            return None
        return sum(valid_values)

    @computed_field
    @property
    def dominant_trait(self) -> str | None:
        """Вычисляемое поле: доминирующая черта"""
        traits = {
            DarkTriadsTypes.CYNICISM: self.cynicism,
            DarkTriadsTypes.NARCISSISM: self.narcissism,
            DarkTriadsTypes.MACHIAVELLIANISM: self.machiavellianism,
            DarkTriadsTypes.PSYCHOTICISM: self.psychoticism
        }

        # Фильтруем None значения
        valid_traits = {k: v for k, v in traits.items() if v is not None}

        if not valid_traits:
            return None

        # Находим максимальное значение
        max_trait = max(valid_traits.items(), key=lambda x: x[1])
        return max_trait[0]