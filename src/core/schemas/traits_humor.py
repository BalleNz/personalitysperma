from typing import Optional
from uuid import UUID

from pydantic import Field, ConfigDict, BaseModel

from core.lexicon.enums import HumorStyleEnum


class HumorProfileSchema(BaseModel):
    """Схема профиля чувства юмора"""
    model_config = ConfigDict(from_attributes=True, use_enum_values=True)

    id: Optional[UUID] = None
    user_id: Optional[UUID] = None

    # Доминирующий стиль юмора HSQ
    dominant_style: Optional[HumorStyleEnum] = Field(
        default=HumorStyleEnum.NONE,
        description="Доминирующий стиль: affiliative, self-enhancing, aggressive, self-defeating"
    )

    # Количественные шкалы по стилям HSQ
    affiliative_humor: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Аффилиативный юмор: для укрепления социальных связей, дружеский, групповой (0=редко, 1=часто использует)"
    )
    self_enhancing_humor: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Самоподдерживающий юмор: для coping со стрессом, позитивный взгляд на жизнь (0=редко, 1=часто)"
    )
    aggressive_humor: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Агрессивный юмор: сарказм, насмешка над других, критика (0=избегает, 1=любит)"
    )
    self_defeating_humor: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Самоуничижительный юмор: самоирония, юмор за свой счет для принятия (0=избегает, 1=часто)"
    )

    # [ подробное описание юмора ]
    sarcasm_level: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Сарказм: ирония, подколы (0=не любит, 1=мастер сарказма)"
    )
    puns_wordplay: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Игры слов, каламбуры, панчи (0=не ценит, 1=обожает)"
    )
    dark_humor: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Черный юмор: о смерти, трагедиях, taboo-темах (0=отталкивает, 1=привлекает)"
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
    satirical_parody: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Сатира, пародия: критика общества, имитация (0=не интересует, 1=ценит)"
    )
    dry_deadpan: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Сухой юмор: deadpan, без эмоций (0=не замечает, 1=мастер)"
    )
    self_deprecating: Optional[float] = Field(
        default=None,
        ge=0.0,
        le=1.0,
        description="Самоирония: шутки над собой (0=избегает, 1=часто использует)"
    )

    # [ юмор в социуме ]
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
