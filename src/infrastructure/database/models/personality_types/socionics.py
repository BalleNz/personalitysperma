from typing import Type

from sqlalchemy import UUID, ForeignKey, Float, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship

from src.core.schemas.personality_types.socionics_type import UserSocionicsSchema
from src.infrastructure.database.models.base import IDMixin, TimestampsMixin, S


class UserSocionics(IDMixin, TimestampsMixin):
    """
    Соционика — вероятностное распределение по 16 типам (в нотации, близкой к MBTI).
    Каждое поле — вероятность (0.0–1.0) принадлежности к данному типу.
    Сумма всех 16 полей ≈ 1.0 (нормализуется на уровне приложения/схемы).
    вычисление — в схеме.
    """

    __tablename__ = "user_socionics"

    user_id: Mapped[UUID] = mapped_column(UUID, ForeignKey('users.id', ondelete="CASCADE"), nullable=False)
    user = relationship("User", back_populates="socionics")

    # Alpha квадра
    ENTP: Mapped[float | None] = mapped_column(Float, default=None,
                                               comment="ENTP / ILE – Intuitive Logical Extravert (Don Quixote)")
    ISFJ: Mapped[float | None] = mapped_column(Float, default=None,
                                               comment="ISFJ / SEI – Sensing Ethical Introvert (Dumas)")
    ESFJ: Mapped[float | None] = mapped_column(Float, default=None,
                                               comment="ESFJ / ESE – Ethical Sensory Extravert (Hugo)")
    INTP: Mapped[float | None] = mapped_column(Float, default=None,
                                               comment="INTP / LII – Logical Intuitive Introvert (Robespierre)")

    # Beta квадра
    ENFJ: Mapped[float | None] = mapped_column(Float, default=None,
                                               comment="ENFJ / EIE – Ethical Intuitive Extravert (Hamlet)")
    ISTP: Mapped[float | None] = mapped_column(Float, default=None,
                                               comment="ISTP / LSI – Logical Sensory Introvert (Maxim Gorky)")
    ESTP: Mapped[float | None] = mapped_column(Float, default=None,
                                               comment="ESTP / SLE – Sensory Logical Extravert (Zhukov)")
    INFJ: Mapped[float | None] = mapped_column(Float, default=None,
                                               comment="INFJ / IEI – Intuitive Ethical Introvert (Yesenin)")

    # Gamma квадра
    ESFP: Mapped[float | None] = mapped_column(Float, default=None,
                                               comment="ESFP / SEE – Sensory Ethical Extravert (Napoleon)")
    INTJ: Mapped[float | None] = mapped_column(Float, default=None,
                                               comment="INTJ / ILI – Intuitive Logical Introvert (Balzac)")
    ENTJ: Mapped[float | None] = mapped_column(Float, default=None,
                                               comment="ENTJ / LIE – Logical Intuitive Extravert (Jack London)")
    ISFP: Mapped[float | None] = mapped_column(Float, default=None,
                                               comment="ISFP / ESI – Ethical Sensory Introvert (Dreiser)")

    # Delta квадра
    ENFP: Mapped[float | None] = mapped_column(Float, default=None,
                                               comment="ENFP / IEE – Intuitive Ethical Extravert (Huxley)")
    INFP: Mapped[float | None] = mapped_column(Float, default=None,
                                               comment="INFP / EII – Ethical Intuitive Introvert (Dostoevsky)")
    ESTJ: Mapped[float | None] = mapped_column(Float, default=None,
                                               comment="ESTJ / LSE – Logical Sensory Extravert (Stirlitz)")
    ISTJ: Mapped[float | None] = mapped_column(Float, default=None,
                                               comment="ISTJ / SLI – Sensory Logical Introvert (Gabin)")

    records: Mapped[int] = mapped_column(Integer, comment="количество записей")

    @property
    def schema_class(self) -> Type[S]:
        return UserSocionicsSchema
