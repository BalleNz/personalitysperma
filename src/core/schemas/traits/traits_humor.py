from typing import Optional
from uuid import UUID, uuid4

from pydantic import Field, ConfigDict, BaseModel, computed_field

HUMOR_FIELDS = [
    "affiliative_humor",
    "puns_wordplay",
    "slapstick_physical",
    "observational_humor",
    "self_enhancing_humor",
    "humor_frequency",
    "humor_in_stress",
    "humor_in_social",
    "aggressive_humor",
    "sarcasm_level",
    "satirical_parody",
    "dark_humor",
    "self_defeating_humor",
    "self_deprecating",
    "witty_quick",
    "absurd_surreal",
    "dry_deadpan",
]


class HumorProfileSchema(BaseModel):
    """Схема профиля чувства юмора"""
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: Optional[UUID] = Field(default_factory=uuid4)
    user_id: Optional[UUID] = None

    # [ affiliative ]
    affiliative_humor: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Аффилиативный юмор: для укрепления социальных связей, дружеский, групповой (0=редко, 1=часто использует)"
    )
    puns_wordplay: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Игры слов, каламбуры, панчи (0=не ценит, 1=обожает)"
    )
    slapstick_physical: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Физический юмор: падения, клоунада, визуальные гэги (0=не смешно, 1=веселит)"
    )
    observational_humor: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Наблюдательный юмор: о повседневной жизни, стереотипах (0=редко, 1=часто замечает)"
    )

    # [ social humor ]
    self_enhancing_humor: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Самоподдерживающий юмор: для coping со стрессом, позитивный взгляд на жизнь (0=редко, 1=часто)"
    )
    humor_frequency: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Частота использования юмора в общении (0=редко шутит, 1=постоянно)"
    )
    humor_in_stress: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Юмор в стрессовых ситуациях: как coping-механизм (0=становится серьезным, 1=шутит чтобы разрядить)"
    )
    humor_in_social: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Юмор в социальных взаимодействиях: для ice-breaking (0=стесняется, 1=активно использует)"
    )

    # [ aggressive ]
    aggressive_humor: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Агрессивный юмор: сарказм, насмешка над других, критика (0=избегает, 1=любит)"
    )
    sarcasm_level: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Сарказм: ирония, подколы (0=не любит, 1=мастер сарказма)"
    )
    satirical_parody: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Сатира, пародия: критика общества, имитация (0=не интересует, 1=ценит)"
    )
    dark_humor: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Черный юмор: о смерти, трагедиях, taboo-темах (0=отталкивает, 1=привлекает)"
    )

    # [ self_defeating ]
    self_defeating_humor: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Самоуничижительный юмор: самоирония, юмор за свой счет для принятия (0=избегает, 1=часто)"
    )
    self_deprecating: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Самоирония: шутки над собой (0=избегает, 1=часто использует)"
    )

    # [ cognitive humor ]
    witty_quick: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Остроумный юмор: быстрые реплики, интеллект (0=медленный, 1=острый ум)"
    )
    absurd_surreal: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Абсурдный юмор: нелогичный, сюрреалистичный (0=не понимает, 1=любит)"
    )
    dry_deadpan: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Сухой юмор: deadpan, без эмоций (0=не замечает, 1=мастер)"
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
    def dominant_humor(self) -> list[str]:
        """Возвращает доминантный/-ные тип юмора"""

        values = [(f, getattr(self, f, 0)) for f in HUMOR_FIELDS]
        if not values:
            return []
        max_v = max(v for _, v in values)
        return sorted(f for f, v in values if abs(v - max_v) < 1e-9)
