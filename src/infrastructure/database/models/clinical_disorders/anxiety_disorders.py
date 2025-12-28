from typing import Type

from sqlalchemy import UUID, ForeignKey, Float, String, CheckConstraint
from sqlalchemy.orm import mapped_column, relationship

from infrastructure.database.models.base import S, IDMixin, TimestampsMixin
from core.schemas.clinical_disorders.anxiety_disorders import AnxietyDisordersSchema


class AnxietyOCDTraumaDisorders(IDMixin, TimestampsMixin):
    """ТРЕВОЖНЫЕ, ОКР И ТРАВМАТИЧЕСКИЕ РАССТРОЙСТВА"""
    __tablename__ = "anxiety_ocd_trauma_disorders"

    user_id = mapped_column(
        UUID,
        ForeignKey('users.id'),
        nullable=False,
        unique=True,
        comment="ID пользователя",
        index=True
    )
    user = relationship("User", back_populates="anxiety_ocd_trauma_disorder")

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

    # [ Фобии ]
    agoraphobia = mapped_column(Float, default=None, comment="Агорафобия (0-1)")
    specific_phobia = mapped_column(Float, default=None, comment="Специфическая фобия (0-1)")
    phobia_type = mapped_column(String(50), default=None, comment="Тип фобии")

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

    @property
    def schema_class(cls) -> Type[S]:
        return AnxietyDisordersSchema

    __table_args__ = (
        CheckConstraint('gad >= 0 AND gad <= 1.00', name='ck_gad_range'),
        CheckConstraint('gad_worry >= 0 AND gad_worry <= 1.00', name='ck_gad_worry_range'),
        CheckConstraint('gad_restlessness >= 0 AND gad_restlessness <= 1.00', name='ck_gad_restlessness_range'),
        CheckConstraint('gad_fatigue >= 0 AND gad_fatigue <= 1.00', name='ck_gad_fatigue_range'),
        CheckConstraint('gad_concentration >= 0 AND gad_concentration <= 1.00', name='ck_gad_concentration_range'),
        CheckConstraint('gad_irritability >= 0 AND gad_irritability <= 1.00', name='ck_gad_irritability_range'),
        CheckConstraint('gad_muscle >= 0 AND gad_muscle <= 1.00', name='ck_gad_muscle_range'),
        CheckConstraint('gad_sleep >= 0 AND gad_sleep <= 1.00', name='ck_gad_sleep_range'),
        CheckConstraint('panic >= 0 AND panic <= 1.00', name='ck_panic_range'),
        CheckConstraint('panic_anticipatory >= 0 AND panic_anticipatory <= 1.00', name='ck_panic_anticipatory_range'),
        CheckConstraint('social_anxiety >= 0 AND social_anxiety <= 1.00', name='ck_social_anxiety_range'),
        CheckConstraint('social_avoidance >= 0 AND social_avoidance <= 1.00', name='ck_social_avoidance_range'),
        CheckConstraint('agoraphobia >= 0 AND agoraphobia <= 1.00', name='ck_agoraphobia_range'),
        CheckConstraint('specific_phobia >= 0 AND specific_phobia <= 1.00', name='ck_specific_phobia_range'),
        CheckConstraint('ocd >= 0 AND ocd <= 1.00', name='ck_ocd_range'),
        CheckConstraint('ocd_obsessions >= 0 AND ocd_obsessions <= 1.00', name='ck_ocd_obsessions_range'),
        CheckConstraint('ocd_compulsions >= 0 AND ocd_compulsions <= 1.00', name='ck_ocd_compulsions_range'),
        CheckConstraint('ocd_insight >= 0 AND ocd_insight <= 1.00', name='ck_ocd_insight_range'),
        CheckConstraint('body_dysmorphia >= 0 AND body_dysmorphia <= 1.00', name='ck_body_dysmorphia_range'),
        CheckConstraint('bfrb >= 0 AND bfrb <= 1.00', name='ck_bfrb_range'),
        CheckConstraint('ptsd >= 0 AND ptsd <= 1.00', name='ck_ptsd_range'),
        CheckConstraint('ptsd_intrusions >= 0 AND ptsd_intrusions <= 1.00', name='ck_ptsd_intrusions_range'),
        CheckConstraint('ptsd_avoidance >= 0 AND ptsd_avoidance <= 1.00', name='ck_ptsd_avoidance_range'),
        CheckConstraint('ptsd_cognition >= 0 AND ptsd_cognition <= 1.00', name='ck_ptsd_cognition_range'),
        CheckConstraint('ptsd_arousal >= 0 AND ptsd_arousal <= 1.00', name='ck_ptsd_arousal_range'),
        CheckConstraint('acute_stress >= 0 AND acute_stress <= 1.00', name='ck_acute_stress_range'),
        CheckConstraint('cptsd >= 0 AND cptsd <= 1.00', name='ck_cptsd_range'),
        CheckConstraint('cptsd_emotion >= 0 AND cptsd_emotion <= 1.00', name='ck_cptsd_emotion_range'),
        CheckConstraint('cptsd_self >= 0 AND cptsd_self <= 1.00', name='ck_cptsd_self_range'),
        CheckConstraint('cptsd_relations >= 0 AND cptsd_relations <= 1.00', name='ck_cptsd_relations_range'),
        CheckConstraint('dissociative >= 0 AND dissociative <= 1.00', name='ck_dissociative_range'),
        CheckConstraint('amnesia >= 0 AND amnesia <= 1.00', name='ck_amnesia_range'),
        CheckConstraint('did >= 0 AND did <= 1.00', name='ck_did_range'),
        CheckConstraint('depersonalization >= 0 AND depersonalization <= 1.00', name='ck_depersonalization_range'),
    )
