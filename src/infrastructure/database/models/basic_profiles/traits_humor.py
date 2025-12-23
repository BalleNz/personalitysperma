from typing import Type

from sqlalchemy import Enum, Float, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from core.lexicon.enums import HumorStyleEnum
from core.schemas.traits_humor import HumorProfileSchema
from infrastructure.database.models.base import IDMixin, S


class HumorProfile(IDMixin):
    """Чувство юмора профиль"""

    __tablename__ = "user_humor_sense"

    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('users.id'), nullable=False, unique=True)
    user = relationship("User", back_populates="humor_sense")

    # Доминирующий стиль юмора HSQ
    dominant_style: Mapped[str | None] = mapped_column(Enum(HumorStyleEnum), default=HumorStyleEnum.NONE, comment="Доминирующий стиль: affiliative, self-enhancing, aggressive, self-defeating")

    # Количественные шкалы по стилям HSQ
    affiliative_humor: Mapped[float | None] = mapped_column(Float, default=None, comment="Аффилиативный юмор: для укрепления социальных связей, дружеский, групповой (0=редко, 1=часто использует)")
    self_enhancing_humor: Mapped[float | None] = mapped_column(Float, default=None, comment="Самоподдерживающий юмор: для coping со стрессом, позитивный взгляд на жизнь (0=редко, 1=часто)")
    aggressive_humor: Mapped[float | None] = mapped_column(Float, default=None, comment="Агрессивный юмор: сарказм, насмешка над другими, критика (0=избегает, 1=любит)")
    self_defeating_humor: Mapped[float | None] = mapped_column(Float, default=None, comment="Самоуничижительный юмор: самоирония, юмор за свой счет для принятия (0=избегает, 1=часто)")

    # [ подробное описание юмора ]
    sarcasm_level: Mapped[float | None] = mapped_column(Float, default=None, comment="Сарказм: ирония, подколы (0=не любит, 1=мастер сарказма)")
    puns_wordplay: Mapped[float | None] = mapped_column(Float, default=None, comment="Игры слов, каламбуры, панчи (0=не ценит, 1=обожает)")
    dark_humor: Mapped[float | None] = mapped_column(Float, default=None, comment="Черный юмор: о смерти, трагедиях, taboo-темах (0=отталкивает, 1=привлекает)")
    slapstick_physical: Mapped[float | None] = mapped_column(Float, default=None, comment="Физический юмор: падения, клоунада, визуальные гэги (0=не смешно, 1=веселит)")
    observational_humor: Mapped[float | None] = mapped_column(Float, default=None, comment="Наблюдательный юмор: о повседневной жизни, стереотипах (0=редко, 1=часто замечает)")
    witty_quick: Mapped[float | None] = mapped_column(Float, default=None, comment="Остроумный юмор: быстрые реплики, интеллект (0=медленный, 1=острый ум)")
    absurd_surreal: Mapped[float | None] = mapped_column(Float, default=None, comment="Абсурдный юмор: нелогичный, сюрреалистичный (0=не понимает, 1=любит)")
    satirical_parody: Mapped[float | None] = mapped_column(Float, default=None, comment="Сатира, пародия: критика общества, имитация (0=не интересует, 1=ценит)")
    dry_deadpan: Mapped[float | None] = mapped_column(Float, default=None, comment="Сухой юмор: deadpan, без эмоций (0=не замечает, 1=мастер)")
    self_deprecating: Mapped[float | None] = mapped_column(Float, default=None, comment="Самоирония: шутки над собой (0=избегает, 1=часто использует)")

    # [ юмор в социуме ]
    humor_frequency: Mapped[float | None] = mapped_column(Float, default=None, comment="Частота использования юмора в общении (0=редко шутит, 1=постоянно)")
    humor_in_stress: Mapped[float | None] = mapped_column(Float, default=None, comment="Юмор в стрессовых ситуациях: как coping-механизм (0=становится серьезным, 1=шутит чтобы разрядить)")
    humor_in_social: Mapped[float | None] = mapped_column(Float, default=None, comment="Юмор в социальных взаимодействиях: для ice-breaking (0=стесняется, 1=активно использует)")

    @property
    def schema_class(cls) -> Type[S]:
        return HumorProfileSchema
