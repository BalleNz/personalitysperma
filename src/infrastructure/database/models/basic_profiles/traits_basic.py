from typing import Type

from sqlalchemy import Float, ForeignKey, UUID, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.schemas.traits.traits_basic import BehavioralProfileSchema, EmotionalProfileSchema, CognitiveProfileSchema, \
    SocialProfileSchema
from src.infrastructure.database.models.base import IDMixin, S, TimestampsMixin


class SocialProfile(IDMixin, TimestampsMixin):
    """Социальный профиль"""

    __tablename__ = "social_profiles"

    user_id = mapped_column(UUID, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="social_profile")

    # [ society influence ]
    locus_control: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="0=другие люди виноваты в моих проблемах, 1=сам отвечаю за свою жизнь"
    )
    independence: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="0=зависим от мнения людей, 1=независим от мнения людей"
    )

    # [ social profile ]
    empathy: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Способность понимать чувства других."
    )
    physical_sensitivity: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Тактильность"
    )
    extraversion: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="0=интроверт, 1=экстраверт"
    )
    altruism: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="эгоизм → бескорыстная помощь"
    )
    conformity: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Конформизм"
    )  # independence → group influence
    social_confidence: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="0=застенчивый, 1=уверенный в общении"
    )
    competitiveness: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="0=кооперативный, 1=соревновательный"
    )

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
    def schema_class(self) -> Type[S]:
        return SocialProfileSchema


class CognitiveProfile(IDMixin, TimestampsMixin):
    """Когнитивный профиль"""

    __tablename__ = "cognitive_profiles"

    user_id = mapped_column(UUID, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="cognitive_profile")

    # [ ДСМ ]
    reflectiveness: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Саморефлексия."
    )
    intuitiveness: Mapped[float | None] = mapped_column(Float, default=None, comment="Опора на интуицию")

    # [ фантазии ]
    fantasy_prone: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="0=приземленный/реалистичный, 1=склонный к фантазиям/мечтательный"
    )
    creativity: Mapped[float | None] = mapped_column(
        Float,
        default=None, comment="0=практичный, 1=креативный")

    # [ мышление ]
    thinking_style: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Деревья важнее леса? 0=простой тип мышления, 1=аналитический/многомерный/сложный тип мышления"
    )
    tolerance_for_ambiguity: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="0=любит ясность и правила, 1=комфортно с неопределенностью"
    )
    mental_flexibility: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Адаптивность. 0=ригидный, 1=гибкий"
    )

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
    def schema_class(self) -> Type[S]:
        return CognitiveProfileSchema


class EmotionalProfile(IDMixin, TimestampsMixin):
    """Эмоциональный профиль"""

    __tablename__ = "emotional_profiles"

    user_id = mapped_column(UUID, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="emotional_profile")

    # [ отношение к миру ]
    optimism: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="0=пессимист, 1=оптимист"
    )
    self_esteem: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Самооценка. 0=низкая самооценка, 1=высокая самооценка"
    )
    self_irony: Mapped[float | None] = mapped_column(Float, default=None, comment="Способность к самоиронии")

    # [ эмоциональность ]
    intimacy_capacity: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Способность к глубокой эмоциональной близости.")
    emotional_sensitivity: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Внутренняя эмоциональная чувствительность."
    )
    emotional_expressiveness: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Внешняя эмоциональность. 0=сдержанный в эмоциях, 1=эмоционально открытый."
    )
    anxiety_level: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Тревожность."
    )

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
    def schema_class(self) -> Type[S]:
        return EmotionalProfileSchema


class BehavioralProfile(IDMixin, TimestampsMixin):
    """ПОВЕДЕНИЕ"""

    __tablename__ = "user_behavioral_profiles"

    user_id = mapped_column(UUID, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="behavioral_profile")

    # [ стресс ]
    patience: Mapped[float | None] = mapped_column(
        Float, default=None,
        comment="Терпение во время стресса. 0=нетерпеливый, 1=терпеливый"
    )
    stress_tolerance: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Насколько комфортно в стрессе"
    )

    # [ решения ]
    ambition: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Амбициозность. 0=нет целей, 1=амбициозный"
    )
    decisiveness: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Решимость. 0=нерешительный, 1=решительный"
    )
    risk_taking: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Рискованность. 0=осторожный, 1=рискующий"
    )

    # [ перфекционизм ]
    perfectionism: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Требования к порядку. 0=непритязательный, 1=перфекционист"
    )

    impulse_control: Mapped[float | None] = mapped_column(
        Float,
        default=None,
        comment="Самоконтроль. 0=импульсивный, 1=сдержанный"  # развитость префронтальной коры
    )

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
    def schema_class(self) -> Type[S]:
        return BehavioralProfileSchema
