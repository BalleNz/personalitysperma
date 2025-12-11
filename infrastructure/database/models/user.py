from typing import TypeVar, Generic, Type

from pydantic import BaseModel
from sqlalchemy import String, Column, Enum, Float, ForeignKey, UUID, TypeDecorator, JSON
from sqlalchemy.orm import Mapped, mapped_column, relationship

from infrastructure.database.models.base import IDMixin, TimestampsMixin

M = TypeVar("M", bound=IDMixin)
S = TypeVar("S", bound=BaseModel)


class PydanticTypeList(TypeDecorator, Generic[S]):
    impl = JSON
    cache_ok = True

    def __init__(self, pydantic_type: Type[S], *args, **kwargs):
        super().__init__(*args, **kwargs)
        self.pydantic_type = pydantic_type

    def process_bind_param(self, value: list[S] | None, dialect):
        if value is None:
            return None
        return [item.model_dump() for item in value]

    def process_result_value(self, value: list | None, dialect):
        if value is None:
            return None
        return [self.pydantic_type(**item) for item in value]


class User(IDMixin, TimestampsMixin):
    __tablename__ = "users"

    telegram_id: Mapped[str] = mapped_column(String, comment="tg id")
    username: Mapped[str] = mapped_column(String, comment="username")
    first_name: Mapped[str | None] = mapped_column(String, comment="first name")
    last_name: Mapped[str | None] = mapped_column(String, comment="last name")

    # [ GENDER ]
    gender: Mapped[str] = mapped_column(Enum(...), nullable=False)
    orientation: Mapped[str] = mapped_column(Enum(...), nullable=False)

    characteristics = relationship("UserCharacteristic", back_populates="user", uselist=False)


class UserCharacteristic(IDMixin):
    __tablename__ = "user_characteristics"

    # [ DEPS ]
    user_id = mapped_column(UUID, ForeignKey('users.id'), nullable=False, unique=True)
    user = relationship("User", back_populates="characteristics")

    humor_sense: Mapped[float | None] = Column(Float, default=None, comment="Чувство юмора")
    patience: Mapped[float | None] = Column(Float, default=None, comment="0=нетерпеливый, 1=терпеливый")
    self_irony: Mapped[float | None] = Column(Float, default=None, comment="Способность к самоиронии")
    extraversion: Mapped[float | None] = mapped_column(Float, default=None, comment="0=интроверт, 1=экстраверт")
    altruism: Mapped[float | None] = Column(Float, default=None, comment="эгоизм → бескорыстная помощь")

    # [ КОГНИТИВНЫЙ СТИЛЬ ]
    reflectiveness: Mapped[float | None] = Column(Float, default=None, comment="0=простое мышление, 1=высокая саморефлексия")
    fantasy_prone: Mapped[float | None] = Column(Float, default=None, comment="0=приземленный/реалистичный, 1=склонный к фантазиям/мечтательный")

    thinking_style: Mapped[float | None] = Column(Float, default=None, comment="0=интуитивный/простые схемы, 1=аналитический/сложные схемы")

    thinking_approach: Mapped[float | None] = Column(Float, default=None, comment="0=интуитивный/целостный, 1=аналитический/детальный")

    cognitive_complexity: Mapped[float | None] = Column(Float, default=None, comment="0=простое/черно-белое мышление, 1=сложное/многомерное мышление")

    creativity: Mapped[float | None] = Column(Float, default=None, comment="0=практичный, 1=креативный")
    tolerance_for_ambiguity: Mapped[float | None] = Column(Float, default=None, comment="0=любит ясность и правила, 1=комфортно с неопределенностью")

    # [ ЭМОЦИИ ]
    emotional_expressiveness: Mapped[float | None] = Column(Float, default=None, comment="0=сдержанный в эмоциях, 1=эмоционально открытый")  # normal → difficulty describing emotions
    anxiety_level: Mapped[float | None] = Column(Float, default=None, comment="Спокойствие")  # calm → constant worry
    optimism: Mapped[float | None] = Column(Float, default=None, comment="0=пессимист, 1=оптимист")

    empathy: Mapped[float | None] = Column(Float, default=None, comment="Способность понимать чувства других")
    intimacy_capacity: Mapped[float | None] = Column(Float, default=None, comment="Способность к глубокой эмоциональной близости")
    emotional_sensitivity: Mapped[float | None] = Column(Float, default=None, comment="Эмоциональная чувствительность")

    # [ ЦЕННОСТИ И МОТИВАЦИЯ ]
    ambition: Mapped[float | None] = Column(Float, default=None, comment="0=нет целей, 1=амбициозный")
    locus_control: Mapped[float | None] = Column(Float, default=None,comment="0=внешний локус контроля (обстоятельства, другие люди), 1=внутренний, сам отвечаю за свою жизнь")
    independence: Mapped[float | None] = Column(Float, default=None, comment="0=конформист, 1=независимый")
    self_esteem: Mapped[float | None] = Column(Float, default=None, comment="0=низкая самооценка, 1=высокая")

    mental_flexibility: Mapped[float | None] = Column(Float, default=None, comment="Адаптивность. 0=ригидный, 1=гибкий")  # flexibility → inflexibility

    # [ ПОВЕДЕНЧЕСКИЕ ПАТТЕРНЫ ]
    risk_taking: Mapped[float | None] = Column(Float, default=None, comment="0=осторожный, 1=рискующий")
    perfectionism: Mapped[float | None] = Column(Float, default=None, comment="0=непритязательный, 1=перфекционист")
    decisiveness: Mapped[float | None] = Column(Float, default=None, comment="0=нерешительный, 1=решительный")

    impulse_control: Mapped[float | None] = Column(Float, default=None, comment="0=импульсивный, 1=сдержанный")
    stress_tolerance: Mapped[float | None] = Column(Float, default=None, comment="Устойчивость к стрессу")

    intuitiveness: Mapped[float | None] = Column(Float, default=None, comment="Опора на интуицию")

    need_for_order: Mapped[float | None] = Column(Float, default=None, comment="0=хаос, 1=порядок")

    # [ СЕНСОРНЫЕ ПРЕДПОЧТЕНИЯ ]
    physical_sensitivity: Mapped[float | None] = Column(Float, default=None, comment="Тактильность")

    # [ СОЦИАЛЬНЫЕ КАЧЕСТВА ]
    conformity: Mapped[float | None] = Column(Float, default=None, comment="Конформизм")  # independence → group influence
    social_confidence: Mapped[float | None] = Column(Float, default=None, comment="0=застенчивый, 1=уверенный в общении")
    competitiveness: Mapped[float | None] = Column(Float, default=None, comment="0=кооперативный, 1=соревновательный")


# TODO: у каждого юзера только по 1 таблице в каждой таблице, которые могут меняться

class UserClinicalAssessment(IDMixin):
    __tablename__ = ""


class DarkTriads(IDMixin):
    __tablename__ = ""
    cynicism: Mapped[float | None] = Column(Float, default=0.5)  # trust → distrust of others' motives
    narcissism: Mapped[float | None] = Column(Float, default=0.5)  # modesty → self-admiration
    machiavellianism: Mapped[float | None] = Column(Float, default=0.5)  # directness → manipulative tendency
    psychoticism: Mapped[float | None] = Column(Float, default=None)  # normality → unusual experiences


class UserHumorSense(IDMixin):
    ...


class UserRelationshipPreference(IDMixin):
    ...
    # attachment_style (secure, anxious, avoidant) - КРИТИЧНО для отношений


class UserCommunicationStyle(IDMixin):
    ...


class UserLoveLanguage(IDMixin):
    """Язык любви"""
    ...
    sensuality: Mapped[float | None] = Column(Float, default=None, comment="Внимание к физическим ощущениям и близости")


class UserSexualPreference(IDMixin):
    """18+ Описание сексуальных предпочтений"""
    ...
    # TODO: подумать об объединении с UserLoveLanguage

    # TODO: Sexual предпочтения таблица, libido value
    # sex_drive_type: Mapped[... | None] = Column(Enum(SexDriveTypeEnum))

# TODO: 3 personal tables. personality_type: Mapped[str | None] = Column(Enum(PersonalityTypeEnum))


class CharacteristicHistory(IDMixin, TimestampsMixin):
    __tablename__ = "characteristic_history"
    user_id = mapped_column(UUID, ForeignKey('users.id'))
    profile_type: Mapped[str] = Column(String)  # 'cognitive', 'emotional', etc.
    characteristic_name: Mapped[str] = Column(String)
    old_value: Mapped[float] = Column(Float)
    new_value: Mapped[float] = Column(Float)
    source: Mapped[str] = Column(String)  # 'voice_message', 'test', 'manual'
