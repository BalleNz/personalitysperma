import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, computed_field


class LooksSchema(BaseModel):
    """Дисморфофобия"""

    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID = Field(description="Идентификатор пользователя")

    bdd_general: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Общий уровень дисморфофобии (0-1)")
    muscle_dysmorphia: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Мышечная дисморфия / bigorexia (0-1)")
    skin_hair_focus: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Кожа, акне (0-1)")

    hair_focus: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Облысение / растительность на лице (0-1)")
    facial_features: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Черты лица (нос, губы, глаза, симметрия, луксмаксинг) (0-1)")
    body_fat: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Жир, целлюлит, вес (0-1)")

    genitals_size: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Размер / форма гениталий (0-1)")
    height_stature: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Рост, пропорции тела, осанка (0-1)")
    aging: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Старение (0-1)")

    reassurance: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Частота поиска подтверждения / вопросов о внешности (0-1)")
    impairment: Optional[float] = Field(default=None, ge=0.0, le=1.0, description="Нарушение жизни / избегание из-за озабоченности внешностью (0-1)")

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

    created_at: datetime | None = Field(None)
    updated_at: datetime | None = Field(None)
