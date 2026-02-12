from datetime import datetime
from typing import Optional
from uuid import UUID, uuid4

from pydantic import BaseModel, ConfigDict, Field, computed_field


class SocialProfileSchema(BaseModel):
    """Схема социального профиля"""
    model_config = ConfigDict(from_attributes=True)
    GROUP: str = "basic"

    id: Optional[UUID] = Field(default_factory=uuid4)
    user_id: Optional[UUID] = None

    # [ society influence ]
    locus_control: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="0=другие люди виноваты в моих проблемах, 1=сам отвечаю за свою жизнь"
    )
    independence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="0=зависим от мнения людей, 1=независим от мнения людей"
    )

    # [ social profile ]
    empathy: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Способность понимать чувства других"
    )
    physical_sensitivity: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Тактильность в социуме"
    )
    extraversion: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="0=интроверт, 1=экстраверт"
    )
    altruism: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="эгоизм → бескорыстная помощь"
    )
    conformity: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Конформизм: independence → group influence"
    )
    social_confidence: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="0=застенчивый, 1=уверенный в общении"
    )
    competitiveness: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="0=кооперативный, 1=соревновательный"
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

    created_at: datetime | None = Field(None)
    updated_at: datetime | None = Field(None)


class CognitiveProfileSchema(BaseModel):
    """Схема когнитивного профиля"""
    model_config = ConfigDict(from_attributes=True)
    GROUP: str = "basic"

    id: Optional[UUID] = Field(default_factory=uuid4)
    user_id: Optional[UUID] = None

    # [ ДСМ ]
    reflectiveness: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Саморефлексия"
    )
    intuitiveness: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Опора на интуицию"
    )

    # [ фантазии ]
    fantasy_prone: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="0=приземленный/реалистичный, 1=склонный к фантазиям/мечтательный"
    )
    creativity: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="0=практичный, 1=креативный"
    )

    # [ мышление ]
    thinking_style: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Деревья важнее леса? 0=простой тип мышления, 1=аналитический/многомерный/сложный тип мышления"
    )
    tolerance_for_ambiguity: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="0=любит ясность и правила, 1=комфортно с неопределенностью"
    )
    mental_flexibility: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Адаптивность. 0=ригидный, 1=гибкий"
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

    created_at: datetime | None = Field(None)
    updated_at: datetime | None = Field(None)


class EmotionalProfileSchema(BaseModel):
    """Схема эмоционального профиля"""
    model_config = ConfigDict(from_attributes=True)
    GROUP: str = "basic"

    id: Optional[UUID] = Field(default_factory=uuid4)
    user_id: Optional[UUID] = None

    # [ отношение к миру ]
    optimism: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="0=пессимист, 1=оптимист"
    )
    self_esteem: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Самооценка. 0=низкая самооценка, 1=высокая самооценка"
    )
    self_irony: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Способность к самоиронии"
    )

    # [ эмоциональность ]
    intimacy_capacity: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Способность к глубокой эмоциональной близости"
    )
    emotional_sensitivity: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Внутренняя эмоциональная чувствительность"
    )
    emotional_expressiveness: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Внешняя эмоциональность. 0=сдержанный в эмоциях, 1=эмоционально открытый"
    )
    anxiety_level: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Тревожность"
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

    created_at: datetime | None = Field(None)
    updated_at: datetime | None = Field(None)


class BehavioralProfileSchema(BaseModel):
    """Схема поведенческого профиля"""
    model_config = ConfigDict(from_attributes=True)
    GROUP: str = "basic"

    id: Optional[UUID] = Field(default_factory=uuid4)
    user_id: Optional[UUID] = None

    # [ стресс ]
    patience: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Терпение во время стресса. 0=нетерпеливый, 1=терпеливый"
    )
    stress_tolerance: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Насколько комфортно в стрессе"
    )

    # [ решения ]
    ambition: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Амбициозность. 0=нет целей, 1=амбициозный"
    )
    decisiveness: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Решимость. 0=нерешительный, 1=решительный"
    )
    risk_taking: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Рискованность. 0=осторожный, 1=рискующий"
    )

    # [ перфекционизм ]
    perfectionism: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Требования к порядку. 0=непритязательный, 1=перфекционист"
    )

    impulse_control: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Самоконтроль. 0=импульсивный, 1=сдержанный"
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

    created_at: datetime | None = Field(None)
    updated_at: datetime | None = Field(None)
