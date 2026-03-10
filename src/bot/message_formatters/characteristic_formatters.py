import datetime
import logging
import math
from typing import Optional

from pydantic import BaseModel, Field

from src.bot.lexicon.button_text import ButtonText
from src.bot.lexicon.message_text import MessageText
from src.core.enums.dark_triads import DarkTriadsTypes
from src.core.schemas.traits.traits_basic import (
    SocialProfileSchema,
    CognitiveProfileSchema,
    EmotionalProfileSchema,
    BehavioralProfileSchema,
)
from src.core.schemas.traits.traits_dark import DarkTriadsSchema
from src.core.schemas.traits.traits_humor import HumorProfileSchema, HUMOR_FIELDS
from src.core.utils.text_formatters import get_characteristic_name, get_date_word_from_iso
from src.infrastructure.database.models.base import S

logger = logging.getLogger(__name__)


class CharacteristicInfo(BaseModel):
    characteristic_text: str = Field(...)
    accuracy_percent: float = Field(...)
    last_update: datetime.datetime = Field(...)


def format_value(
        value: Optional[float],
        field_name: str,
        previous: Optional[Any]
) -> str:
    """
    Форматирует значение в процентах и добавляет стрелки в зависимости от изменения.

    Правила стрелок (по абсолютной разнице в исходных значениях 0..1):
    • |Δ| ≤ 0.05     → без стрелок
    • 0.05 < |Δ| ≤ 0.15 → одна стрелка
    • 0.15 < |Δ| ≤ 0.30 → две стрелки
    • |Δ| > 0.30       → три стрелки

    ↑ — значение выросло (стало лучше)
    ↓ — значение уменьшилось (стало хуже)
    """
    if value is None:
        return ""

    percent = math.ceil(100 * value)
    arrows = ""

    if previous is not None:
        prev_value = getattr(previous, field_name, None)
        if prev_value is not None:
            delta = value - prev_value
            abs_delta = abs(delta)

            if abs_delta <= 0.05:
                arrows = "—"
            else:
                count = 1
                if abs_delta > 0.15:
                    count = 2
                if abs_delta > 0.30:
                    count = 3

                if delta > 0:
                    arrows = "↑" * count
                else:
                    arrows = "↓" * count

    return f"{percent}% {arrows}"


class CharacteristicMessageFormatter:
    """форматирование для характеристик"""

    @staticmethod
    def format_traits_core(
            schemas: list[list[S]],
            full_access: bool
    ) -> str:
        characteristic_texts: list[str] = []
        accuracy_percents: list[float] = []
        last_update_list: list[datetime] = []

        for schema_row in schemas:
            match schema_row[0].__class__.__name__:
                case SocialProfileSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter.format_social_profile(schema_row, full_access)
                case BehavioralProfileSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter.format_behavioral_profile(schema_row, full_access)
                case EmotionalProfileSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter.format_emotional_profile(schema_row, full_access)
                case CognitiveProfileSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter.format_cognitive_profile(schema_row, full_access)
                case _:
                    raise

            characteristic_texts.append(characteristic_info.characteristic_text)
            accuracy_percents.append(characteristic_info.accuracy_percent)
            last_update_list.append(characteristic_info.last_update)

        # [ общий текст ]
        all_text: str = ''.join(characteristic_texts)

        # [ точность ]
        accuracy_percent: float = math.fsum(accuracy_percents) / 4
        accuracy_percent = math.ceil(accuracy_percent * 100)

        # [ дата ]
        last_update = min(last_update_list)
        last_update_text = get_date_word_from_iso(last_update)

        verdict = ""
        if accuracy_percent < 0.24:
            verdict = "Эта характеристика не окончательная! Продолжайте рассказывать о себе!\n\n"

        return MessageText.CHARACTERISTIC_LISTING.format(
            characteristic_name=ButtonText.TRAITS_BASIC,
            characteristic=all_text,
            accuracy_percent=accuracy_percent,
            last_update=last_update_text,
            verdict=verdict
        )

    @staticmethod
    def format_social_profile(schemas: list[SocialProfileSchema], full_access: bool) -> CharacteristicInfo:
        fields: tuple

        schema: SocialProfileSchema = schemas[0]
        previous: SocialProfileSchema = schemas[1]

        if full_access:
            fields = (
                f"<b>— Ответственность за свои действия:</b> {format_value(schema.locus_control, 'locus_control', previous)}" if schema.locus_control is not None else "",
                f"<b>— Независимость от чужого мнения:</b> {format_value(schema.independence, 'independence', previous)}" if schema.independence is not None else "",
                f"<b>— Эмпатия:</b> {format_value(schema.empathy, 'empathy', previous)}" if schema.empathy is not None else "",
                f"<b>— Физическая чувствительность:</b> {format_value(schema.physical_sensitivity, 'physical_sensitivity', previous)}" if schema.physical_sensitivity is not None else "",
                f"<b>— Экстраверсия:</b> {format_value(schema.extraversion, 'extraversion', previous)}" if schema.extraversion is not None else "",
                f"<b>— Бескорыстность:</b> {format_value(schema.altruism, 'altruism', previous)}" if schema.altruism is not None else "",
                f"<b>— Конформизм:</b> {format_value(schema.conformity, 'conformity', previous)}" if schema.conformity is not None else "",
                f"<b>— Социальная уверенность:</b> {format_value(schema.social_confidence, 'social_confidence', previous)}" if schema.social_confidence is not None else "",
                f"<b>— Соревновательность:</b> {format_value(schema.competitiveness, 'competitiveness', previous)}" if schema.competitiveness is not None else ""
            )
        else:
            fields = (
                f"<b>— Ответственность за свои действия:</b> {format_value(schema.locus_control, 'locus_control', previous)}" if schema.locus_control is not None else "",
                f"<b>— Независимость от чужого мнения:</b> {format_value(schema.independence, 'independence', previous)}" if schema.independence is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 7 полей необходим полный доступ</i>",
            )

        characteristic: str = "👥 <b>Твоя социальность</b>\n" + "<blockquote>" + '\n'.join(
            [field for field in fields if field]) + "</blockquote>\n\n"

        return CharacteristicInfo(
            accuracy_percent=schema.accuracy_percent,
            characteristic_text=characteristic,
            last_update=schema.updated_at
        )

    @staticmethod
    def format_cognitive_profile(
            schemas: list[CognitiveProfileSchema],
            full_access: bool
    ) -> CharacteristicInfo:
        fields: tuple
        schema = schemas[0]
        previous = schemas[1]

        if full_access:
            fields = (
                f"<b>— Склонность к фантазиям:</b> {format_value(schema.fantasy_prone, 'fantasy_prone', previous)}" if schema.fantasy_prone is not None else "",
                f"<b>— Рефлексивность:</b> {format_value(schema.reflectiveness, 'reflectiveness', previous)}" if schema.reflectiveness is not None else "",
                f"<b>— Интуитивность:</b> {format_value(schema.intuitiveness, 'intuitiveness', previous)}" if schema.intuitiveness is not None else "",
                f"<b>— Креативность:</b> {format_value(schema.creativity, 'creativity', previous)}" if schema.creativity is not None else "",
                f"<b>— Аналитичность мышления:</b> {format_value(schema.thinking_style, 'thinking_style', previous)}" if schema.thinking_style is not None else "",
                f"<b>— Толерантность к неопределённости:</b> {format_value(schema.tolerance_for_ambiguity, 'tolerance_for_ambiguity', previous)}" if schema.tolerance_for_ambiguity is not None else "",
                f"<b>— Ментальная гибкость:</b> {format_value(schema.mental_flexibility, 'mental_flexibility', previous)}" if schema.mental_flexibility is not None else "",
            )
        else:
            fields = (
                f"<b>— Склонность к фантазиям:</b> {format_value(schema.fantasy_prone, 'fantasy_prone', previous)}" if schema.fantasy_prone is not None else "",
                f"<b>— Рефлексивность:</b> {format_value(schema.reflectiveness, 'reflectiveness', previous)}" if schema.reflectiveness is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 5 полей необходим полный доступ</i>",
            )

        characteristic: str = "🧠 <b>Мышление</b>\n" + "<blockquote>" + '\n'.join(
            [field for field in fields if field]
        ) + "</blockquote>\n\n"

        return CharacteristicInfo(
            accuracy_percent=schema.accuracy_percent,
            characteristic_text=characteristic,
            last_update=schema.updated_at
        )

    @staticmethod
    def format_emotional_profile(
            schemas: list[EmotionalProfileSchema],
            full_access: bool
    ) -> CharacteristicInfo:
        fields = tuple()

        schema: EmotionalProfileSchema = schemas[0]
        previous: EmotionalProfileSchema = schemas[1]

        if full_access:
            fields = (
                f"<b>— Тревожность:</b> {format_value(schema.anxiety_level, 'anxiety_level', previous)}" if schema.anxiety_level is not None else "",
                f"<b>— Оптимистичность:</b> {format_value(schema.optimism, 'optimism', previous)}" if schema.optimism is not None else "",
                f"<b>— Самооценка:</b> {format_value(schema.self_esteem, 'self_esteem', previous)}" if schema.self_esteem is not None else "",
                f"<b>— Способность к близости:</b> {format_value(schema.intimacy_capacity, 'intimacy_capacity', previous)}" if schema.intimacy_capacity is not None else "",
                f"<b>— Эмоциональная чувствительность:</b> {format_value(schema.emotional_sensitivity, 'emotional_sensitivity', previous)}" if schema.emotional_sensitivity is not None else "",
                f"<b>— Открытость эмоций:</b> {format_value(schema.emotional_expressiveness, 'emotional_expressiveness', previous)}" if schema.emotional_expressiveness is not None else "",
                f"<b>— Самоирония:</b> {format_value(schema.self_irony, 'self_irony', previous)}" if schema.self_irony is not None else "",
            )
        else:
            fields = (
                f"<b>— Тревожность:</b> {format_value(schema.anxiety_level, 'anxiety_level', previous)}" if schema.anxiety_level is not None else "",
                f"<b>— Оптимистичность:</b> {format_value(schema.optimism, 'optimism', previous)}" if schema.optimism is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 5 полей необходим полный доступ</i>",
            )

        characteristic: str = "🎭 <b>Твоя эмоциональность</b>\n" + "<blockquote>" + '\n'.join(
            [field for field in fields if field]) + "</blockquote>\n\n"

        return CharacteristicInfo(
            accuracy_percent=schema.accuracy_percent,
            characteristic_text=characteristic,
            last_update=schema.updated_at
        )

    @staticmethod
    def format_behavioral_profile(schemas: list[BehavioralProfileSchema], full_access: bool) -> CharacteristicInfo:
        fields: tuple

        schema: BehavioralProfileSchema = schemas[0]
        previous: BehavioralProfileSchema = schemas[1]

        if full_access:
            fields = (
                f"<b>— Решительность:</b> {format_value(schema.decisiveness, 'decisiveness', previous)}" if schema.decisiveness is not None else "",
                f"<b>— Стрессоустойчивость:</b> {format_value(schema.stress_tolerance, 'stress_tolerance', previous)}" if schema.stress_tolerance is not None else "",
                f"<b>— Терпение:</b> {format_value(schema.patience, 'patience', previous)}" if schema.patience is not None else "",
                f"<b>— Амбициозность:</b> {format_value(schema.ambition, 'ambition', previous)}" if schema.ambition is not None else "",
                f"<b>— Склонность к риску:</b> {format_value(schema.risk_taking, 'risk_taking', previous)}" if schema.risk_taking is not None else "",
                f"<b>— Перфекционизм:</b> {format_value(schema.perfectionism, 'perfectionism', previous)}" if schema.perfectionism is not None else "",
                f"<b>— Сдержанность:</b> {format_value(schema.impulse_control, 'impulse_control', previous)}" if schema.impulse_control is not None else "",
            )
        else:
            fields = (
                f"<b>— Решительность:</b> {format_value(schema.decisiveness, 'decisiveness', previous)}" if schema.decisiveness is not None else "",
                f"<b>— Стрессоустойчивость:</b> {format_value(schema.stress_tolerance, 'stress_tolerance', previous)}" if schema.stress_tolerance is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 5 полей необходим полный доступ</i>",
            )

        characteristic: str = "🗣 <b>Оценка твоего поведения</b>\n" + "<blockquote>" + '\n'.join(
            [field for field in fields if field]) + "</blockquote>\n\n"

        return CharacteristicInfo(
            accuracy_percent=schema.accuracy_percent,
            characteristic_text=characteristic,
            last_update=schema.updated_at
        )

    @staticmethod
    def format_dark_triads(schemas: list[DarkTriadsSchema]) -> str:
        schema: DarkTriadsSchema = schemas[0]
        previous: DarkTriadsSchema = schemas[1]

        fields = (
            f"Цинизм: {format_value(schema.cynicism, 'cynicism', previous)}% (доверчивость ←→ цинизм)" if schema.cynicism is not None else "",
            f"Нарциссизм: {format_value(schema.narcissism, 'narcissism', previous)}% (скромность ←→ нарциссизм)" if schema.narcissism is not None else "",
            f"Макиавеллизм: {format_value(schema.machiavellianism, 'machiavellianism', previous)}% (прямота ←→ манипулятивность)" if schema.machiavellianism is not None else "",
            f"Психотизм: {format_value(schema.psychoticism, 'psychoticism', previous)}% (норма ←→ психотизм)" if schema.psychoticism is not None else "",
        )

        extra: str = (
            f"Доминирующая черта: {DarkTriadsTypes(schema.dominant_trait).value if schema.dominant_trait else '—'}"
            if schema.dominant_trait else ""
        )

        characteristic_name = get_characteristic_name(type(schema))
        characteristic: str = ("Dark triads" + "<blockquote>" + '\n'.join([field for field in fields if field]) +
                               extra + "</blockquote>\n\n")

        last_update: str = get_date_word_from_iso(schema.updated_at)

        return MessageText.CHARACTERISTIC_LISTING.format(
            characteristic_name=characteristic_name,
            characteristic=characteristic,
            accuracy_percent=math.ceil(schema.accuracy_percent * 100),
            last_update=last_update,
        )

    @staticmethod
    def format_humor_profile(schemas: list[HumorProfileSchema]) -> str:
        schema = schemas[0]
        fields = tuple(
            f"{field.replace('_', ' ').capitalize()}: {math.ceil(100 * getattr(schema, field))}%"
            for field in HUMOR_FIELDS
            if getattr(schema, field) is not None
        )

        # TODO
        extra = (
            f"Доминирующий юмор: {', '.join(schema.dominant_humor) if schema.dominant_humor else '—'}"
        )

        characteristic_name = get_characteristic_name(type(schema))
        characteristic_text = '\n'.join([field for field in fields if field])

        last_update: str = get_date_word_from_iso(schema.updated_at)

        return MessageText.CHARACTERISTIC_LISTING.format(
            characteristic_name=characteristic_name,
            characteristic=characteristic_text,
            accuracy_percent=math.ceil(schema.accuracy_percent * 100),
            last_update=last_update
        )

    class characteristic_formatter:
        """Шаблоны с форматированием"""

        @staticmethod
        def get_characteristic_text_by_schema(
                formatter_name: str,
                # ... accesses for profiles
        ):
            # [ base ]
            TRAITS_CORE = CharacteristicMessageFormatter.format_traits_core

            DARK_TRIADS = CharacteristicMessageFormatter.format_dark_triads
            HUMOR_PROFILE = CharacteristicMessageFormatter.format_humor_profile

            # [ clinical ]
            # MOOD_DISORDERS = PersonalityMessageFormatter.format_mood_disorders
            # ...

            match formatter_name:
                case "basic":
                    return TRAITS_CORE

                case DarkTriadsSchema.__name__:
                    return DARK_TRIADS

                case HumorProfileSchema.__name__:
                    return HUMOR_PROFILE
