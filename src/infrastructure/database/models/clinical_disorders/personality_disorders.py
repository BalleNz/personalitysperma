from typing import Type

from sqlalchemy import UUID, ForeignKey, Float, CheckConstraint
from sqlalchemy.orm import mapped_column, relationship

from infrastructure.database.models.base import TimestampsMixin, S, IDMixin
from core.schemas.clinical_disorders.personality_disorders import PersonalityDisordersSchema


class PersonalityDisorders(IDMixin, TimestampsMixin):
    """РАССТРОЙСТВА ЛИЧНОСТИ"""
    __tablename__ = "personality_disorders"

    user_id = mapped_column(UUID, ForeignKey('users.id'), nullable=False, unique=True, comment="ID пользователя")
    user = relationship("User", back_populates="personality_disorder")

    # [ ПРЛ ]
    bpd_severity = mapped_column(Float, default=None, comment="Тяжесть ПРЛ (0-1)")
    bpd_abandonment = mapped_column(Float, default=None, comment="Страх брошенности (0-1)")
    bpd_unstable_relations = mapped_column(Float, default=None, comment="Нестабильные отношения (0-1)")
    bpd_identity = mapped_column(Float, default=None, comment="Нарушение идентичности (0-1)")
    bpd_impulsivity = mapped_column(Float, default=None, comment="Импульсивность (0-1)")
    bpd_suicidal = mapped_column(Float, default=None, comment="Суицидальное поведение (0-1)")
    bpd_mood_swings = mapped_column(Float, default=None, comment="Перепады настроения (0-1)")
    bpd_emptiness = mapped_column(Float, default=None, comment="Чувство пустоты (0-1)")
    bpd_anger = mapped_column(Float, default=None, comment="Неадекватный гнев (0-1)")
    bpd_paranoia = mapped_column(Float, default=None, comment="Параноидные идеи (0-1)")

    # [ Другие РЛ ]
    npd = mapped_column(Float, default=None, comment="Нарциссическое РЛ (0-1)")
    aspd = mapped_column(Float, default=None, comment="Антисоциальное РЛ (0-1)")
    avpd = mapped_column(Float, default=None, comment="Избегающее РЛ (0-1)")
    dpd = mapped_column(Float, default=None, comment="Зависимое РЛ (0-1)")
    ocpd = mapped_column(Float, default=None, comment="Обсессивно-компульсивное РЛ (0-1)")
    ppd = mapped_column(Float, default=None, comment="Параноидное РЛ (0-1)")
    szpd = mapped_column(Float, default=None, comment="Шизоидное РЛ (0-1)")
    stpd = mapped_column(Float, default=None, comment="Шизотипическое РЛ (0-1)")

    @property
    def schema_class(cls) -> Type[S]:
        return PersonalityDisordersSchema

    __table_args__ = (
        CheckConstraint('bpd_severity >= 0 AND bpd_severity <= 1.00', name='ck_bpd_severity_range'),
        CheckConstraint('bpd_abandonment >= 0 AND bpd_abandonment <= 1.00', name='ck_bpd_abandonment_range'),
        CheckConstraint('bpd_unstable_relations >= 0 AND bpd_unstable_relations <= 1.00', name='ck_bpd_unstable_relations_range'),
        CheckConstraint('bpd_identity >= 0 AND bpd_identity <= 1.00', name='ck_bpd_identity_range'),
        CheckConstraint('bpd_impulsivity >= 0 AND bpd_impulsivity <= 1.00', name='ck_bpd_impulsivity_range'),
        CheckConstraint('bpd_suicidal >= 0 AND bpd_suicidal <= 1.00', name='ck_bpd_suicidal_range'),
        CheckConstraint('bpd_mood_swings >= 0 AND bpd_mood_swings <= 1.00', name='ck_bpd_mood_swings_range'),
        CheckConstraint('bpd_emptiness >= 0 AND bpd_emptiness <= 1.00', name='ck_bpd_emptiness_range'),
        CheckConstraint('bpd_anger >= 0 AND bpd_anger <= 1.00', name='ck_bpd_anger_range'),
        CheckConstraint('bpd_paranoia >= 0 AND bpd_paranoia <= 1.00', name='ck_bpd_paranoia_range'),
        CheckConstraint('npd >= 0 AND npd <= 1.00', name='ck_npd_range'),
        CheckConstraint('aspd >= 0 AND aspd <= 1.00', name='ck_aspd_range'),
        CheckConstraint('avpd >= 0 AND avpd <= 1.00', name='ck_avpd_range'),
        CheckConstraint('dpd >= 0 AND dpd <= 1.00', name='ck_dpd_range'),
        CheckConstraint('ocpd >= 0 AND ocpd <= 1.00', name='ck_ocpd_range'),
        CheckConstraint('ppd >= 0 AND ppd <= 1.00', name='ck_ppd_range'),
        CheckConstraint('szpd >= 0 AND szpd <= 1.00', name='ck_szpd_range'),
        CheckConstraint('stpd >= 0 AND stpd <= 1.00', name='ck_stpd_range'),
    )
