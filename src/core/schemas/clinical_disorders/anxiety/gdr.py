import uuid
from datetime import datetime
from typing import Optional

from pydantic import BaseModel, Field, computed_field


class GDRSchema(BaseModel):
    """ТРЕВОГА"""
    id: Optional[uuid.UUID] = Field(default_factory=uuid.uuid4)
    user_id: uuid.UUID = Field(description="Идентификатор пользователя")

    gad_worry: Optional[float] = Field(default=None, ge=0.0, le=1.0,
                                       description="Чрезмерное беспокойство / тревожные ожидания (0-1)")
    gad_uncontrollable: Optional[float] = Field(default=None, ge=0.0, le=1.0,
                                                description="Трудности с контролем беспокойства (0-1)")

    gad_relaxation: Optional[float] = Field(default=None, ge=0.0, le=1.0,
                                            description="Трудности с расслаблением (0-1)")
    gad_muscle_tension: Optional[float] = Field(default=None, ge=0.0, le=1.0,
                                                description="Мышечное напряжение, скованность (0-1)")

    gad_catastrophic: Optional[float] = Field(default=None, ge=0.0, le=1.0,
                                              description="Предчувствие беды / ощущение надвигающейся катастрофы (0-1)")
    gad_restlessness: Optional[float] = Field(default=None, ge=0.0, le=1.0,
                                              description="Моторное беспокойство, неусидчивость, ощущение на взводе (0-1)")
    gad_fatigue: Optional[float] = Field(default=None, ge=0.0, le=1.0,
                                         description="Лёгкая утомляемость, быстрое истощение (0-1)")
    gad_concentration: Optional[float] = Field(default=None, ge=0.0, le=1.0,
                                               description="Трудности с концентрацией внимания, «пустота в голове» (0-1)")
    gad_irritability: Optional[float] = Field(default=None, ge=0.0, le=1.0,
                                              description="Раздражительность, вспыльчивость (0-1)")

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
