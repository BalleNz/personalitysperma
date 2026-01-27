from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field, ConfigDict, BaseModel, computed_field

from src.core.enums.dark_triads import DarkTriadsTypes


class DarkTriadsSchema(BaseModel):
    """Схема темной триады (цинизм, нарциссизм, макиавеллизм, психотизм)"""
    model_config = ConfigDict(from_attributes=True)

    id: Optional[UUID] = Field(default_factory=uuid4)
    user_id: str = Field(description="Идентификатор пользователя")

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

    records: int | None = Field(
        default=None,
        description="Количество записей"
    )

    @computed_field
    @property
    def accuracy_percent(self) -> float:
        """Процент точности"""
        records_count: int | None = self.records
        if records_count is None or records_count <= 0:
            return 0.0
        elif records_count == 1:
            return 0.04
        elif records_count == 2:
            return 0.09
        else:
            # при 7 записях: 42%
            # при 17 записях: 63%
            # при 27 записях: 71%
            # при 50 записях: 78%
            margin = 1.5081 / (records_count ** 0.5)
            return 1 - margin

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
