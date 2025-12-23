from typing import Type

from sqlalchemy import Column, Float, ForeignKey, UUID
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models.base import IDMixin, S


class SocialProfile(IDMixin):
    """Социальный профиль"""

    __tablename__ = "social_profiles"

    user_id = mapped_column(UUID, ForeignKey('users.id'), nullable=False, unique=True)
    user = relationship("User", back_populates="social_profile")

    # [ society influence ]
    locus_control: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="0=другие люди виноваты в моих проблемах, 1=сам отвечаю за свою жизнь"
    )
    independence: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="0=зависим от мнения людей, 1=независим от мнения людей"
    )

    # [ social profile ]
    empathy: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="Способность понимать чувства других."
    )
    physical_sensitivity: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="Тактильность"
    )
    extraversion: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="0=интроверт, 1=экстраверт"
    )
    altruism: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="эгоизм → бескорыстная помощь"
    )
    conformity: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="Конформизм"
    )  # independence → group influence
    social_confidence: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="0=застенчивый, 1=уверенный в общении"
    )
    competitiveness: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="0=кооперативный, 1=соревновательный"
    )

    @property
    def schema_class(self) -> Type[S]:
        return ...


class CognitiveProfile(IDMixin):
    """Когнитивный профиль"""

    __tablename__ = "cognitive_profiles"

    user_id = mapped_column(UUID, ForeignKey('users.id'), nullable=False, unique=True)
    user = relationship("User", back_populates="cognitive_profile")

    # [ ДСМ ]
    reflectiveness: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="Саморефлексия."
    )
    intuitiveness: Mapped[float | None] = Column(Float, default=None, comment="Опора на интуицию")

    # [ фантазии ]
    fantasy_prone: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="0=приземленный/реалистичный, 1=склонный к фантазиям/мечтательный"
    )
    creativity: Mapped[float | None] = Column(
        Float,
        default=None, comment="0=практичный, 1=креативный")

    # [ мышление ]
    thinking_style: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="Деревья важнее леса? 0=простой тип мышления, 1=аналитический/многомерный/сложный тип мышления"
    )
    tolerance_for_ambiguity: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="0=любит ясность и правила, 1=комфортно с неопределенностью"
    )
    mental_flexibility: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="Адаптивность. 0=ригидный, 1=гибкий"
    )

    @property
    def schema_class(self) -> Type[S]:
        return ...


class EmotionalProfile(IDMixin):
    """Эмоциональный профиль"""

    __tablename__ = "emotional_profiles"

    user_id = mapped_column(UUID, ForeignKey('users.id'), nullable=False, unique=True)
    user = relationship("User", back_populates="emotional_profile")

    # [ отношение к миру ]
    optimism: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="0=пессимист, 1=оптимист"
    )
    self_esteem: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="Самооценка. 0=низкая самооценка, 1=высокая самооценка"
    )
    self_irony: Mapped[float | None] = Column(Float, default=None, comment="Способность к самоиронии")

    # [ эмоциональность ]
    intimacy_capacity: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="Способность к глубокой эмоциональной близости.")
    emotional_sensitivity: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="Внутренняя эмоциональная чувствительность."
    )
    emotional_expressiveness: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="Внешняя эмоциональность. 0=сдержанный в эмоциях, 1=эмоционально открытый."
    )
    anxiety_level: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="Тревожность."
    )

    @property
    def schema_class(self) -> Type[S]:
        return ...


class BehavioralProfile(IDMixin):
    """ПОВЕДЕНИЕ"""

    __tablename__ = "user_behavioral_profiles"

    user_id = mapped_column(UUID, ForeignKey('users.id'), nullable=False, unique=True)
    user = relationship("User", back_populates="behavioral_profile")

    # [ стресс ]
    patience: Mapped[float | None] = Column(
        Float, default=None,
        comment="Терпение во время стресса. 0=нетерпеливый, 1=терпеливый"
    )
    stress_tolerance: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="Насколько комфортно в стрессе"
    )

    # [ решения ]
    ambition: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="Амбициозность. 0=нет целей, 1=амбициозный"
    )
    decisiveness: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="Решимость. 0=нерешительный, 1=решительный"
    )
    risk_taking: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="Рискованность. 0=осторожный, 1=рискующий"
    )

    # [ перфекционизм ]
    need_for_order: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="Нуждаемость в порядке."
    )
    perfectionism: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="Требования к порядку. 0=непритязательный, 1=перфекционист"
    )

    impulse_control: Mapped[float | None] = Column(
        Float,
        default=None,
        comment="Самоконтроль. 0=импульсивный, 1=сдержанный"  # развитость префронтальной коры
    )

    @property
    def schema_class(self) -> Type[S]:
        return ...
