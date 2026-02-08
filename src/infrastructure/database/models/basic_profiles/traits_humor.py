from typing import Type

from sqlalchemy import Float, ForeignKey, UUID, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.schemas.traits.traits_humor import HumorProfileSchema
from src.infrastructure.database.models.base import IDMixin, S, TimestampsMixin


class HumorProfile(IDMixin, TimestampsMixin):
    """Чувство юмора профиль"""

    __tablename__ = "user_humor_sense"

    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="humor_profile")

    # [ affiliative ]
    affiliative_humor: Mapped[float | None] = mapped_column(Float, default=None,
                                                            comment="Аффилиативный юмор: для укрепления социальных связей, дружеский, групповой (0=редко, 1=часто использует)")
    puns_wordplay: Mapped[float | None] = mapped_column(Float, default=None,
                                                        comment="Игры слов, каламбуры, панчи (0=не ценит, 1=обожает)")
    slapstick_physical: Mapped[float | None] = mapped_column(Float, default=None,
                                                             comment="Физический юмор: падения, клоунада, визуальные гэги (0=не смешно, 1=веселит)")
    observational_humor: Mapped[float | None] = mapped_column(Float, default=None,
                                                              comment="Наблюдательный юмор: о повседневной жизни, стереотипах (0=редко, 1=часто замечает)")

    # [ social humor ]
    self_enhancing_humor: Mapped[float | None] = mapped_column(Float, default=None,
                                                               comment="Самоподдерживающий юмор: для coping со стрессом, позитивный взгляд на жизнь (0=редко, 1=часто)")
    humor_frequency: Mapped[float | None] = mapped_column(Float, default=None,
                                                          comment="Частота использования юмора в общении (0=редко шутит, 1=постоянно)")
    humor_in_stress: Mapped[float | None] = mapped_column(Float, default=None,
                                                          comment="Юмор в стрессовых ситуациях: как coping-механизм (0=становится серьезным, 1=шутит чтобы разрядить)")
    humor_in_social: Mapped[float | None] = mapped_column(Float, default=None,
                                                          comment="Юмор в социальных взаимодействиях: для ice-breaking (0=стесняется, 1=активно использует)")

    # [ aggressive ]
    aggressive_humor: Mapped[float | None] = mapped_column(Float, default=None,
                                                           comment="Агрессивный юмор: сарказм, насмешка над другими, критика (0=избегает, 1=любит)")
    sarcasm_level: Mapped[float | None] = mapped_column(Float, default=None,
                                                        comment="Сарказм: ирония, подколы (0=не любит, 1=мастер сарказма)")
    satirical_parody: Mapped[float | None] = mapped_column(Float, default=None,
                                                           comment="Сатира, пародия: критика общества, имитация (0=не интересует, 1=ценит)")
    dark_humor: Mapped[float | None] = mapped_column(Float, default=None,
                                                     comment="Черный юмор: о смерти, трагедиях, taboo-темах (0=отталкивает, 1=привлекает)")

    # [ self_defeating ]
    self_defeating_humor: Mapped[float | None] = mapped_column(Float, default=None,
                                                               comment="Самоуничижительный юмор: самоирония, юмор за свой счет для принятия (0=избегает, 1=часто)")
    self_deprecating: Mapped[float | None] = mapped_column(Float, default=None,
                                                           comment="Самоирония: шутки над собой (0=избегает, 1=часто использует)")

    # [ cognitive humor ]
    witty_quick: Mapped[float | None] = mapped_column(Float, default=None,
                                                      comment="Остроумный юмор: быстрые реплики, интеллект (0=медленный, 1=острый ум)")
    absurd_surreal: Mapped[float | None] = mapped_column(Float, default=None,
                                                         comment="Абсурдный юмор: нелогичный, сюрреалистичный (0=не понимает, 1=любит)")
    dry_deadpan: Mapped[float | None] = mapped_column(Float, default=None,
                                                      comment="Сухой юмор: deadpan, без эмоций (0=не замечает, 1=мастер)")

    records: Mapped[int | None] = mapped_column(
        Integer,
        default=None,
        comment="количество записей"
    )

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return HumorProfileSchema
