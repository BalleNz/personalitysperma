import datetime
import logging
import math
from typing import Optional

from pydantic import BaseModel, Field

from src.bot.lexicon.button_text import ButtonText
from src.bot.lexicon.message_text import MessageText
from src.core.enums.dark_triads import DarkTriadsTypes
from src.core.schemas.clinical_disorders.anxiety_disorders import AnxietyDisordersSchema
from src.core.schemas.clinical_disorders.mood_disorders import MoodDisordersSchema
from src.core.schemas.clinical_disorders.neuro_disorders import NeuroDisordersSchema
from src.core.schemas.clinical_disorders.personality_disorders import PersonalityDisordersSchema
from src.core.schemas.personality_types.hexaco import UserHexacoSchema
from src.core.schemas.personality_types.holland_codes import UserHollandCodesSchema
from src.core.schemas.personality_types.socionics_type import UserSocionicsSchema
from src.core.schemas.traits.traits_basic import (
    SocialProfileSchema,
    CognitiveProfileSchema,
    EmotionalProfileSchema,
    BehavioralProfileSchema,
)
from src.core.schemas.traits.traits_dark import DarkTriadsSchema
from src.core.schemas.traits.traits_humor import HumorProfileSchema, HUMOR_FIELDS
from src.infrastructure.database.models.base import S

logger = logging.getLogger(__name__)


def get_last_update(date: Optional[datetime.datetime]) -> str:
    """Последнее обновление в строчном виде (вчера, неделю назад, ...)"""
    if date is None:
        return "N/A"

    now = datetime.datetime.now(datetime.timezone.utc)
    delta = now - date

    if delta.days == 0:
        return "сегодня"
    if delta.days == 1:
        return "вчера"
    if 2 <= delta.days <= 6:
        return f"{delta.days} дня назад"
    if 7 <= delta.days <= 13:
        return "неделю назад"
    if 14 <= delta.days <= 29:
        return "больше недели назад"
    if delta.days >= 30:
        return "больше месяца назад"
    return "N/A"


def get_characteristic_name(schema_name: type[S]):
    """
    Возвращает человеко-ориентированное название характеристики/профиля
    """
    names = {
        SocialProfileSchema: "Социальность",
        CognitiveProfileSchema: "Мышление",
        EmotionalProfileSchema: "Эмоциональность",
        BehavioralProfileSchema: "Поведение",
        DarkTriadsSchema: "Тёмная триада",
        HumorProfileSchema: "Чувство юмора",
        MoodDisordersSchema: "Настроение",
        AnxietyDisordersSchema: "Тревожность",
        NeuroDisordersSchema: "Нейрокогнитивные нарушения",
        PersonalityDisordersSchema: "Личностные расстройства",
        UserHexacoSchema: "HEXACO",
        UserHollandCodesSchema: "Коды Холланда",
        UserSocionicsSchema: "Соционика",
    }
    return names[schema_name]

    # RelationshipPreferenceSchema
    # LoveLanguageSchema
    # SexualPreferenceSchema


def get_date_word_from_iso(date: datetime.datetime | datetime.date | str | None) -> str:
    """
    Возвращает дату на русском языке
    Примеры:
        datetime(..) → "4 марта"
    """
    if isinstance(date, datetime.datetime):
        date = date.date()

    day = date.day
    month_names = [
        "января", "февраля", "марта", "апреля", "мая", "июня",
        "июля", "августа", "сентября", "октября", "ноября", "декабря"
    ]

    month = month_names[date.month - 1]

    return f"{day} {month}"


class CharacteristicInfo(BaseModel):
    characteristic_text: str = Field(...)
    accuracy_percent: float = Field(...)
    last_update: datetime.datetime = Field(...)


class PersonalityMessageFormatter:
    """Форматирование сообщений о психологических профилях"""

    @staticmethod
    def format_traits_core(
            schemas: list[S],
            full_access: bool
    ) -> str:
        characteristic_texts: list[str] = []
        accuracy_percents: list[float] = []
        last_update_list: list[datetime] = []

        for schema in schemas:
            match schema.__class__.__name__:
                case SocialProfileSchema.__name__:
                    characteristic_info = PersonalityMessageFormatter.format_social_profile(schema, full_access)
                case BehavioralProfileSchema.__name__:
                    characteristic_info = PersonalityMessageFormatter.format_behavioral_profile(schema, full_access)
                case EmotionalProfileSchema.__name__:
                    characteristic_info = PersonalityMessageFormatter.format_emotional_profile(schema, full_access)
                case CognitiveProfileSchema.__name__:
                    characteristic_info = PersonalityMessageFormatter.format_cognitive_profile(schema, full_access)
                case _:
                    raise

            characteristic_texts.append(characteristic_info.characteristic_text)
            accuracy_percents.append(characteristic_info.accuracy_percent)
            last_update_list.append(characteristic_info.last_update)

        # [ общий текст ]
        all_text: str = ''.join(characteristic_texts)

        # [ точность ]
        accuracy_percent: float = math.fsum(accuracy_percents) / 4

        # [ дата ]
        last_update = min(last_update_list)
        last_update_text = get_date_word_from_iso(last_update)

        return MessageText.CHARACTERISTIC_LISTING.format(
            characteristic_name=ButtonText.TRAITS_BASIC,
            characteristic=all_text,
            accuracy_percent=math.ceil(accuracy_percent * 100),
            last_update=last_update_text
        )

    @staticmethod
    def format_social_profile(schema: SocialProfileSchema, full_access: bool) -> CharacteristicInfo:
        fields: tuple
        if full_access:
            fields = (
                f"<b>— Ответственность за свои действия:</b> {math.ceil(100 * schema.locus_control)}%" if schema.locus_control else "",
                f"<b>— Независимость от чужого мнения:</b> {math.ceil(100 * schema.independence)}%" if schema.independence else "",
                f"<b>— Эмпатия:</b> {math.ceil(100 * schema.empathy)}%" if schema.empathy is not None else "",
                f"<b>— Физическая чувствительность:</b> {math.ceil(100 * schema.physical_sensitivity)}%" if schema.physical_sensitivity is not None else "",
                f"<b>— Экстраверсия:</b> {math.ceil(100 * schema.extraversion)}%" if schema.extraversion is not None else "",
                f"<b>— Бескорыстность:</b> {math.ceil(100 * schema.altruism)}%" if schema.altruism is not None else "",
                f"<b>— Конформизм:</b> {math.ceil(100 * schema.conformity)}%" if schema.conformity is not None else "",
                f"<b>— Социальная уверенность:</b> {math.ceil(100 * schema.social_confidence)}%" if schema.social_confidence is not None else "",
                f"<b>— Соревновательность:</b> {math.ceil(100 * schema.competitiveness)}%" if schema.competitiveness is not None else "",
            )
        else:
            fields = (
                f"<b>— Ответственность за свои действия:</b> {math.ceil(100 * schema.locus_control)}%" if schema.locus_control else "",
                f"<b>— Независимость от чужого мнения:</b> {math.ceil(100 * schema.independence)}%" if schema.independence else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 7 полей необходим полный доступ</i>"
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
            schema: CognitiveProfileSchema,
            full_access: bool
    ) -> CharacteristicInfo:
        fields: tuple
        if full_access:
            fields = (
                f"<b>— Склонность к фантазиям:</b> {math.ceil(100 * schema.fantasy_prone)}%" if schema.fantasy_prone is not None else "",
                f"<b>— Рефлексивность:</b> {math.ceil(100 * schema.reflectiveness)}%" if schema.reflectiveness is not None else "",
                f"<b>— Интуитивность:</b> {math.ceil(100 * schema.intuitiveness)}%" if schema.intuitiveness is not None else "",
                f"<b>— Креативность:</b> {math.ceil(100 * schema.creativity)}%" if schema.creativity is not None else "",
                f"<b>— Аналитичность мышления:</b> {math.ceil(100 * schema.thinking_style)}%" if schema.thinking_style is not None else "",
                f"<b>— Толерантность к неопределённости:</b> {math.ceil(100 * schema.tolerance_for_ambiguity)}%" if schema.tolerance_for_ambiguity is not None else "",
                f"<b>— Ментальная гибкость:</b> {math.ceil(100 * schema.mental_flexibility)}%" if schema.mental_flexibility is not None else "",
            )
        else:
            fields = (
                f"<b>— Склонность к фантазиям:</b> {math.ceil(100 * schema.fantasy_prone)}%" if schema.fantasy_prone is not None else "",
                f"<b>— Рефлексивность:</b> {math.ceil(100 * schema.reflectiveness)}%" if schema.reflectiveness is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 5 полей необходим полный доступ</i>"
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
            schema: EmotionalProfileSchema,
            full_access: bool
    ) -> CharacteristicInfo:
        fields = tuple()
        if full_access:
            fields = (
                f"<b>— Тревожность:</b> {math.ceil(100 * schema.anxiety_level)}%" if schema.anxiety_level is not None else "",
                f"<b>— Оптимистичность:</b> {math.ceil(100 * schema.optimism)}%" if schema.optimism is not None else "",
                f"<b>— Самооценка:</b> {math.ceil(100 * schema.self_esteem)}%" if schema.self_esteem is not None else "",
                f"<b>— Способность к близости:</b> {math.ceil(100 * schema.intimacy_capacity)}%" if schema.intimacy_capacity is not None else "",
                f"<b>— Эмоциональная чувствительность:</b> {math.ceil(100 * schema.emotional_sensitivity)}%" if schema.emotional_sensitivity is not None else "",
                f"<b>— Открытость эмоций:</b> {math.ceil(100 * schema.emotional_expressiveness)}%" if schema.emotional_expressiveness is not None else "",
                f"<b>— Самоирония:</b> {math.ceil(100 * schema.self_irony)}%" if schema.self_irony is not None else "",
            )
        else:
            fields = (
                f"<b>— Тревожность:</b> {math.ceil(100 * schema.anxiety_level)}%" if schema.anxiety_level is not None else "",
                f"<b>— Оптимистичность:</b> {math.ceil(100 * schema.optimism)}%" if schema.optimism is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 5 полей необходим полный доступ</i>"
            )

        characteristic: str = "🎭 <b>Твоя эмоциональность</b>\n" + "<blockquote>" + '\n'.join(
            [field for field in fields if field]) + "</blockquote>\n\n"

        return CharacteristicInfo(
            accuracy_percent=schema.accuracy_percent,
            characteristic_text=characteristic,
            last_update=schema.updated_at
        )

    @staticmethod
    def format_behavioral_profile(schema: BehavioralProfileSchema, full_access: bool) -> CharacteristicInfo:
        fields: tuple
        if full_access:
            fields = (
                f"<b>— Решительность:</b> {math.ceil(100 * schema.decisiveness)}%" if schema.decisiveness is not None else "",
                f"<b>— Стрессоустойчивость:</b> {math.ceil(100 * schema.stress_tolerance)}%" if schema.stress_tolerance is not None else "",
                f"<b>— Терпение:</b> {math.ceil(100 * schema.patience)}%" if schema.patience is not None else "",
                f"<b>— Амбициозность:</b> {math.ceil(100 * schema.ambition)}%" if schema.ambition is not None else "",
                f"<b>— Склонность к риску:</b> {math.ceil(100 * schema.risk_taking)}%" if schema.risk_taking is not None else "",
                f"<b>— Перфекционизм:</b> {math.ceil(100 * schema.perfectionism)}%" if schema.perfectionism is not None else "",
                f"<b>— Сдержанность:</b> {math.ceil(100 * schema.impulse_control)}%" if schema.impulse_control is not None else "",
            )
        else:
            fields = (
                f"<b>— Решительность:</b> {math.ceil(100 * schema.decisiveness)}%" if schema.decisiveness is not None else "",
                f"<b>— Стрессоустойчивость:</b> {math.ceil(100 * schema.stress_tolerance)}%" if schema.stress_tolerance is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 5 полей необходим полный доступ</i>"
            )

        characteristic: str = "🗣 <b>Оценка твоего поведения</b>\n" + "<blockquote>" + '\n'.join(
            [field for field in fields if field]) + "</blockquote>\n\n"

        return CharacteristicInfo(
            accuracy_percent=schema.accuracy_percent,
            characteristic_text=characteristic,
            last_update=schema.updated_at
        )

    @staticmethod
    def format_dark_triads(schema: DarkTriadsSchema) -> str:
        fields = (
            f"Цинизм: {math.ceil(100 * schema.cynicism)}% (доверчивость ←→ цинизм)" if schema.cynicism is not None else "",
            f"Нарциссизм: {math.ceil(100 * schema.narcissism)}% (скромность ←→ нарциссизм)" if schema.narcissism is not None else "",
            f"Макиавеллизм: {math.ceil(100 * schema.machiavellianism)}% (прямота ←→ манипулятивность)" if schema.machiavellianism is not None else "",
            f"Психотизм: {math.ceil(100 * schema.psychoticism)}% (норма ←→ психотизм)" if schema.psychoticism is not None else "",
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
            last_update=last_update
        )

    @staticmethod
    def format_humor_profile(schema: HumorProfileSchema) -> str:
        fields = tuple(
            f"{field.replace('_', ' ').capitalize()}: {math.ceil(100 * getattr(schema, field))}%"
            for field in HUMOR_FIELDS
            if getattr(schema, field) is not None
        )

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

    @staticmethod
    def format_hexaco(schema: UserHexacoSchema) -> str:
        fields = (
            f"Честность-Скромность (H): {math.ceil(100 * schema.honesty_humility)}%" if schema.honesty_humility is not None else "",
            f"Эмоциональность (E): {math.ceil(100 * schema.emotionality)}%" if schema.emotionality is not None else "",
            f"Экстраверсия (X): {math.ceil(100 * schema.extraversion)}%" if schema.extraversion is not None else "",
            f"Сговорчивость (A): {math.ceil(100 * schema.agreeableness)}%" if schema.agreeableness is not None else "",
            f"Добросовестность (C): {math.ceil(100 * schema.conscientiousness)}%" if schema.conscientiousness is not None else "",
            f"Открытость опыту (O): {math.ceil(100 * schema.openness)}%" if schema.openness is not None else "",
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
            TRAITS_CORE = PersonalityMessageFormatter.format_traits_core

            DARK_TRIADS = PersonalityMessageFormatter.format_dark_triads
            HUMOR_PROFILE = PersonalityMessageFormatter.format_humor_profile

            # [ personality ]
            # SOCIONICS = PersonalityMessageFormatter.format_socionics
            # HOLLAND_CODES = PersonalityMessageFormatter.format_holland_codes
            HEXACO = PersonalityMessageFormatter.format_hexaco

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
