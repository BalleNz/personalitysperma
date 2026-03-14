from typing import Type

from sqlalchemy import Float
from sqlalchemy.orm import mapped_column, Mapped

from src.infrastructure.database.models.base import S, IDMixin, TimestampsMixin


class GDR(IDMixin, TimestampsMixin):
    """Генерализированное тревожное расстройство"""

    # TODO: разделить таблицы везде по таким абзацам для лучшего качества ответов
    # TODO: проверить соответствие полей и comment в grok

    # TODO: присвоить каждому полю с "расстройство" группу "болезни" и собирать в check_in если юзер просит (инструкция в промпт: загружай все таблицы с расстройствами и болезнями если юзер просит или их важно учитывать)
    #   - или сделать отдельный tuple с названиями таблиц, которые содержат эти поля

    gad = mapped_column(Float, default=None, comment="Генерализованное тревожное расстройство (0-1)")
    gad_worry = mapped_column(Float, default=None, comment="Беспокойство / тревога ожидания (0-1)")
    gad_irritability = mapped_column(Float, default=None, comment="Раздражительность (0-1)")
    gad_muscle = mapped_column(Float, default=None, comment="Мышечное напряжение (0-1)")

    accuracy_percent: Mapped[int | None] = mapped_column(
        Float,
        default=None,
        comment="процент точности"
    )

    @property
    def schema_class(cls) -> Type[S]:
        return ...
