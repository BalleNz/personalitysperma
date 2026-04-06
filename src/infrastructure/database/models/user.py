from typing import Type

from sqlalchemy import String, Integer, Boolean, text, Enum
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.enums.user import TALKING_MODES, GENDER
from src.core.schemas.user_schemas import UserSchema
from src.infrastructure.database.models.base import IDMixin, TimestampsMixin, S
from src.infrastructure.database.models.basic_profiles.traits_basic import SocialProfile, BehavioralProfile, \
    EmotionalProfile, \
    CognitiveProfile
from database.models.triads.dark_triad import DarkTriads
from src.infrastructure.database.models.basic_profiles.traits_humor import HumorProfile
from src.infrastructure.database.models.clinical_disorders.anxiety.gdr import GDRDisorder
from src.infrastructure.database.models.clinical_disorders.anxiety.panic import PanicDisorder
from src.infrastructure.database.models.clinical_disorders.anxiety.ptsd import PTSDDisorder
from src.infrastructure.database.models.clinical_disorders.mood_disorders.bipolar import BipolarDisorder
from src.infrastructure.database.models.clinical_disorders.mood_disorders.depression import DepressionDisorder
from src.infrastructure.database.models.clinical_disorders.neuro_disorders.adhd import ADHDDisorder
from src.infrastructure.database.models.clinical_disorders.neuro_disorders.autism import AutismDisorder
from database.models.clinical_disorders.personality_disorders.dissociative import DissociativeDisorder
from src.infrastructure.database.models.clinical_disorders.neuro_disorders.eating_disorders import EatingDisorder
from src.infrastructure.database.models.clinical_disorders.neuro_disorders.looks_disorder import LooksDisorder
from database.models.clinical_disorders.mood_disorders.bpd import BPDDisorder
from src.infrastructure.database.models.diary import UserDiary
from src.infrastructure.database.models.personality_types.hexaco import UserHexaco
from src.infrastructure.database.models.personality_types.holland_codes import UserHollandCodes
from src.infrastructure.database.models.personality_types.socionics import UserSocionics

TALKING_MODES_SQL = Enum(
    TALKING_MODES,
    name="talking_modes",
    values_callable=lambda obj: [e.value for e in obj]
)

GENDER_SQL = Enum(
    GENDER,
    name="gender",
    values_callable=lambda obj: [e.value for e in obj]
)


class User(IDMixin, TimestampsMixin):
    __tablename__ = "users"

    telegram_id: Mapped[str] = mapped_column(String, unique=True, comment="tg id")
    username: Mapped[str] = mapped_column(String, comment="username")
    first_name: Mapped[str | None] = mapped_column(String, comment="first name")
    last_name: Mapped[str | None] = mapped_column(String, comment="last name")

    # [ SETTINGS ]

    real_name: Mapped[str | None] = mapped_column(String, comment="реальное имя")
    talk_mode: Mapped[str] = mapped_column(
        TALKING_MODES_SQL,
        comment="режим общения",
        server_default=TALKING_MODES.RESEARCH.value
    )

    # [ ACCESSES ]
    used_voice_messages: Mapped[int] = mapped_column(
        Integer,
        comment="использовано голосовых сообщений",
        default=0,
        server_default="0"
    )
    full_access: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default=text("false"),
        comment="полный доступ: безлимит гс, базовая характеристика"
    )

    # [ Quizzes, tests ]

    passed_typing: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default=text("false"),
        comment="типирование пройдено"
    )

    dark_triads_full: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default=text("false"),
        comment="тёмная триада"
    )  # TODO: сделать туда еще светлую триаду
    humor_access: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default=text("false"),
        comment="базовая характеристика доступ"
    )
    clinical_access: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default=text("false"),
        comment="клиническая характеристика доступ"
    )
    love_access: Mapped[bool] = mapped_column(
        Boolean,
        default=False,
        nullable=False,
        server_default=text("false"),
        comment="романтические предпочтения доступ"
    )

    # [ INFO ]
    gender: Mapped[str] = mapped_column(
        GENDER_SQL,
        comment="gender",
        server_default=GENDER.MALE.value
    )
    age: Mapped[int | None] = mapped_column(Integer, comment="возраст (предугадывает нейронка)")

    # [ DIARY ]
    diary: Mapped["UserDiary | None"] = relationship(
        UserDiary, back_populates="user", uselist=True,
        cascade="all, delete-orphan",
        passive_deletes=True
    )

    # [ profiles ]
    social_profile: Mapped["SocialProfile | None"] = relationship(
        SocialProfile, back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    cognitive_profile: Mapped["CognitiveProfile | None"] = relationship(
        CognitiveProfile, back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    emotional_profile: Mapped["EmotionalProfile | None"] = relationship(
        EmotionalProfile, back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    behavioral_profile: Mapped["BehavioralProfile | None"] = relationship(
        BehavioralProfile, back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    humor_profile: Mapped["HumorProfile | None"] = relationship(
        HumorProfile, back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    dark_triads: Mapped["DarkTriads | None"] = relationship(
        DarkTriads, back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    hexaco: Mapped["UserHexaco | None"] = relationship(
        UserHexaco, back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    socionics: Mapped["UserSocionics | None"] = relationship(
        UserSocionics, back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    holland_codes: Mapped["UserHollandCodes | None"] = relationship(
        UserHollandCodes, back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # [ mood ]
    bipolar_disorder: Mapped["BipolarDisorder | None"] = relationship(
        BipolarDisorder, back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    depression_disorder: Mapped["DepressionDisorder | None"] = relationship(
        DepressionDisorder, back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # [ neuro ]
    adhd_disorder: Mapped["ADHDDisorder | None"] = relationship(
        ADHDDisorder, back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    autism_disorder: Mapped["AutismDisorder | None"] = relationship(
        AutismDisorder, back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    dissociative_disorder: Mapped["DissociativeDisorder | None"] = relationship(
        DissociativeDisorder, back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    eating_disorder: Mapped["EatingDisorder | None"] = relationship(
        EatingDisorder, back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    looks_disorder: Mapped["LooksDisorder | None"] = relationship(
        LooksDisorder, back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # [ anxiety ]
    gdr_disorder: Mapped["GDRDisorder | None"] = relationship(
        GDRDisorder, back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    panic_disorder: Mapped["PanicDisorder | None"] = relationship(
        PanicDisorder, back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    ptsd_disorder: Mapped["PTSDDisorder | None"] = relationship(
        PTSDDisorder, back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # [ listing ]
    bpd_disorder: Mapped["BPDDisorder | None"] = relationship(
        BPDDisorder, back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # FUTURE
    """love_language: Mapped["LoveLanguage | None"] = relationship(
        "LoveLanguage", back_populates="user", uselist=False
    )
    sexual_preference: Mapped["SexualPreference | None"] = relationship(
        "SexualPreference", back_populates="user", uselist=False
    )
    relationship_preference: Mapped["RelationshipPreference | None"] = relationship(
        "RelationshipPreference", back_populates="user", uselist=False
    )"""

    @property
    def schema_class(self) -> Type[S]:
        return UserSchema
