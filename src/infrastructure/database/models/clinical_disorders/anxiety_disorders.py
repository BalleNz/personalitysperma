from typing import Type

from sqlalchemy import UUID, ForeignKey, Float, String, Integer
from sqlalchemy.orm import mapped_column, relationship, Mapped

from src.core.schemas.clinical_disorders.anxiety_disorders import AnxietyDisordersSchema
from src.infrastructure.database.models.base import S, IDMixin, TimestampsMixin


class AnxietyDisorders(IDMixin, TimestampsMixin):
    """ТРЕВОЖНЫЕ, ОКР И ТРАВМАТИЧЕСКИЕ РАССТРОЙСТВА"""
    __tablename__ = "anxiety_ocd_trauma_disorders"

    user_id = mapped_column(
        UUID,
        ForeignKey('users.id', ondelete="CASCADE"),
        nullable=False,
        comment="ID пользователя",
        index=True
    )
    user = relationship("User", back_populates="anxiety_disorders")

    # [ Тревожные расстройства ]
    # [ ГТР ]
    gad = mapped_column(Float, default=None, comment="Генерализованное тревожное расстройство (0-1)")
    gad_worry = mapped_column(Float, default=None, comment="Беспокойство (0-1)")
    gad_restlessness = mapped_column(Float, default=None, comment="Беспокойство/нервозность (0-1)")
    gad_fatigue = mapped_column(Float, default=None, comment="Утомляемость (0-1)")
    gad_concentration = mapped_column(Float, default=None, comment="Нарушения концентрации (0-1)")
    gad_irritability = mapped_column(Float, default=None, comment="Раздражительность (0-1)")
    gad_muscle = mapped_column(Float, default=None, comment="Мышечное напряжение (0-1)")
    gad_sleep = mapped_column(Float, default=None, comment="Нарушения сна (0-1)")

    # [ Паническое ]
    panic = mapped_column(Float, default=None, comment="Паническое расстройство (0-1)")
    panic_frequency = mapped_column(String(20), default=None, comment="Частота панических атак")
    panic_anticipatory = mapped_column(Float, default=None, comment="Тревога ожидания (0-1)")

    # [ Социальное ]
    social_anxiety = mapped_column(Float, default=None, comment="Социальная тревога (0-1)")
    social_avoidance = mapped_column(Float, default=None, comment="Избегание социальных ситуаций (0-1)")

    # [ ОКР и родственные ]
    ocd = mapped_column(Float, default=None, comment="Обсессивно-компульсивное расстройство (0-1)")
    ocd_obsessions = mapped_column(Float, default=None, comment="Навязчивые мысли (0-1)")
    ocd_compulsions = mapped_column(Float, default=None, comment="Компульсивные действия (0-1)")
    ocd_insight = mapped_column(Float, default=None, comment="Критичность к симптомам (0-1)")
    body_dysmorphia = mapped_column(Float, default=None, comment="Дисморфофобия (0-1)")
    bfrb = mapped_column(Float, default=None, comment="Повторяющееся поведение (0-1)")

    # ————————————————————————————————————
    # [ Травма и стрессовые расстройства ]
    ptsd = mapped_column(Float, default=None, comment="Посттравматическое стрессовое расстройство (0-1)")
    ptsd_intrusions = mapped_column(Float, default=None, comment="Интрузивные воспоминания (0-1)")
    ptsd_avoidance = mapped_column(Float, default=None, comment="Избегание триггеров (0-1)")
    ptsd_cognition = mapped_column(Float, default=None, comment="Негативные мысли (0-1)")
    ptsd_arousal = mapped_column(Float, default=None, comment="Гипервозбуждение (0-1)")
    acute_stress = mapped_column(Float, default=None, comment="Острое стрессовое расстройство (0-1)")

    # [ Комплексное ПТСР ]
    cptsd = mapped_column(Float, default=None, comment="Комплексное ПТСР (0-1)")
    cptsd_emotion = mapped_column(Float, default=None, comment="Нарушения эмоциональной регуляции (0-1)")
    cptsd_self = mapped_column(Float, default=None, comment="Нарушения самооценки (0-1)")
    cptsd_relations = mapped_column(Float, default=None, comment="Нарушения в отношениях (0-1)")

    # [ Диссоциативные расстройства ]
    dissociative = mapped_column(Float, default=None, comment="Диссоциативные симптомы (0-1)")
    amnesia = mapped_column(Float, default=None, comment="Амнезия (0-1)")
    did = mapped_column(Float, default=None, comment="Диссоциативное расстройство идентичности (0-1)")
    depersonalization = mapped_column(Float, default=None, comment="Деперсонализация/дереализация (0-1)")

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
        return AnxietyDisordersSchema
