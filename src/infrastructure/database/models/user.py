from typing import Type

from sqlalchemy import String, Integer, Boolean, text
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.schemas.user_schemas import UserSchema
from src.infrastructure.database.models.base import IDMixin, TimestampsMixin, S


class User(IDMixin, TimestampsMixin):
    __tablename__ = "users"

    telegram_id: Mapped[str] = mapped_column(String, unique=True, comment="tg id")
    username: Mapped[str] = mapped_column(String, comment="username")
    first_name: Mapped[str | None] = mapped_column(String, comment="first name")
    last_name: Mapped[str | None] = mapped_column(String, comment="last name")

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

    # [ base info ]
    age: Mapped[int | None] = mapped_column(Integer, comment="возраст (предугадывает нейронка)")

    # [ core ]
    social_profile: Mapped["SocialProfile | None"] = relationship(
        "SocialProfile", back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    cognitive_profile: Mapped["CognitiveProfile | None"] = relationship(
        "CognitiveProfile", back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    emotional_profile: Mapped["EmotionalProfile | None"] = relationship(
        "EmotionalProfile", back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    behavioral_profile: Mapped["BehavioralProfile | None"] = relationship(
        "BehavioralProfile", back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # [ humor ]
    humor_profile: Mapped["HumorProfile | None"] = relationship(
        "HumorProfile", back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # [ dark ]
    dark_triads: Mapped["DarkTriads | None"] = relationship(
        "DarkTriads", back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # [ personality types ]
    hexaco: Mapped["UserHexaco | None"] = relationship(
        "UserHexaco", back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    socionics: Mapped["UserSocionics | None"] = relationship(
        "UserSocionics", back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    holland_codes: Mapped["UserHollandCodes | None"] = relationship(
        "UserHollandCodes", back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # [ clinical ]
    clinical_profile: Mapped["ClinicalProfile | None"] = relationship(
        "ClinicalProfile", back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    mood_disorders: Mapped["MoodDisorders | None"] = relationship(
        "MoodDisorders", back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    anxiety_disorders: Mapped["AnxietyDisorders | None"] = relationship(
        "AnxietyDisorders", back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    personality_disorders: Mapped["PersonalityDisorders | None"] = relationship(
        "PersonalityDisorders", back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )
    neuro_disorders: Mapped["NeuroDisorders | None"] = relationship(
        "NeuroDisorders", back_populates="user", uselist=False,
        cascade="all, delete-orphan",
        passive_deletes=True,
    )

    # [ romance_preferences ]
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
