import datetime
import logging
import math
from enum import Enum
from typing import Optional, Any, Callable

from pydantic import BaseModel, Field

from src.bot.lexicon.button_text import ButtonText
from src.bot.lexicon.message_text import MessageText
from src.core.enums.dark_triads import DarkTriadsTypes
from src.core.schemas.clinical_disorders.anxiety.gdr import GDRSchema
from src.core.schemas.clinical_disorders.anxiety.panic import PanicSchema
from src.core.schemas.clinical_disorders.anxiety.ptsd import PTSDSchema
from src.core.schemas.clinical_disorders.mood_disorders.bipolar import BipolarDisorderSchema
from src.core.schemas.clinical_disorders.mood_disorders.depression import DepressionDisorderSchema
from src.core.schemas.clinical_disorders.neuro_disorders.adhd import ADHDSchema
from src.core.schemas.clinical_disorders.neuro_disorders.autism import AutismSchema
from src.core.schemas.clinical_disorders.neuro_disorders.dissociative import DissociativeSchema
from src.core.schemas.clinical_disorders.neuro_disorders.eating import EatingSchema
from src.core.schemas.clinical_disorders.neuro_disorders.looks_disorder import LooksSchema
from src.core.schemas.clinical_disorders.personality_disorders.bpd import BPDSchema
from src.core.schemas.traits.traits_basic import (
    SocialProfileSchema,
    CognitiveProfileSchema,
    EmotionalProfileSchema,
    BehavioralProfileSchema,
)
from src.core.schemas.traits.traits_humor import HumorProfileSchema
from src.core.schemas.triads.dark_triad import DarkTriadsSchema
from src.core.schemas.triads.light_triad import LightTriadsSchema
from src.core.utils.text_formatters import get_characteristic_name, get_date_word_from_iso
from src.infrastructure.database.models.base import S

logger = logging.getLogger(__name__)


class CharacteristicGroups(str, Enum):
    """ГРУППЫ ХАРАКТЕРИСТИК"""

    MBTI = "mbti"
    HOLLAND_CODES = "holland_codes"
    HEXACO = "hexaco"

    BASIC = "basic"
    TRIADS = "triads"
    HUMOR = "humor"

    NEURO = "neuro"
    MOOD_DISORDERS = "mood_disorders"
    BPD = "bpd"
    DISSOCIATIVE_DISORDER = "dissociative"
    ANXIETY = "anxiety"
    LOOKS = "looks"


CharacteristicGroup_To_ButtonText: dict = {
    CharacteristicGroups.MBTI: ButtonText.MBTI,
    CharacteristicGroups.HOLLAND_CODES: ButtonText.HOLLAND_CODES,
    CharacteristicGroups.HEXACO: ButtonText.HEXACO,

    CharacteristicGroups.BASIC: ButtonText.BASIC,
    CharacteristicGroups.TRIADS: ButtonText.TRIADS,
    CharacteristicGroups.HUMOR: ButtonText.HUMOR,

    CharacteristicGroups.NEURO: ButtonText.NEURO,
    CharacteristicGroups.MOOD_DISORDERS: ButtonText.MOOD_DISORDERS,
    CharacteristicGroups.BPD: ButtonText.BPD,
    CharacteristicGroups.DISSOCIATIVE_DISORDER: ButtonText.DISSOCIATIVE_DISORDER,
    CharacteristicGroups.ANXIETY: ButtonText.ANXIETY,
    CharacteristicGroups.LOOKS: ButtonText.LOOKS
}


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
    • |Δ| ≤ 0.05 → без стрелок
    • 0.05 < |Δ| ≤ 0.15 → одна стрелка
    • 0.15 < |Δ| ≤ 0.30 → две стрелки
    • |Δ| > 0.30 → три стрелки

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

            if abs_delta <= 0.03:
                arrows = ""
            else:
                count = 1
                if abs_delta > 0.07:
                    count = 2
                if abs_delta > 0.10:
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
                    characteristic_info = CharacteristicMessageFormatter().format_social_profile(
                        schema_row,
                        full_access
                    )
                case BehavioralProfileSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter().format_behavioral_profile(
                        schema_row,
                        full_access
                    )
                case EmotionalProfileSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter().format_emotional_profile(
                        schema_row,
                        full_access
                    )
                case CognitiveProfileSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter().format_cognitive_profile(
                        schema_row,
                        full_access
                    )
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

        return MessageText.CHARACTERISTIC_LISTING_GROUP.format(
            characteristic_name=ButtonText.BASIC,
            characteristic=all_text,
            accuracy_percent=accuracy_percent,
            last_update=last_update_text,
            verdict=verdict
        )

    @staticmethod
    def format_humor(
            schemas: list[list[S]],
            full_access: bool
    ) -> str:
        characteristic_texts: list[str] = []
        accuracy_percents: list[float] = []
        last_update_list: list[datetime] = []

        for schema_row in schemas:
            match schema_row[0].__class__.__name__:
                case HumorProfileSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter().format_humor_profile(
                        schema_row,
                        full_access
                    )
                case _:
                    raise

            characteristic_texts.append(characteristic_info.characteristic_text)
            accuracy_percents.append(characteristic_info.accuracy_percent)
            last_update_list.append(characteristic_info.last_update)

        # [ общий текст ]
        all_text: str = ''.join(characteristic_texts)

        # [ точность ]
        accuracy_percent: float = math.fsum(accuracy_percents) / len(accuracy_percents) if accuracy_percents else 0.0
        accuracy_percent = math.ceil(accuracy_percent * 100)

        # [ дата ]
        last_update = min(last_update_list)
        last_update_text = get_date_word_from_iso(last_update)

        verdict = ""
        if accuracy_percent < 0.24:
            verdict = "Эта характеристика не окончательная! Продолжайте рассказывать о себе!\n\n"

        return MessageText.CHARACTERISTIC_LISTING_SINGLE.format(
            characteristic=all_text,
            accuracy_percent=accuracy_percent,
            last_update=last_update_text,
            verdict=verdict
        )

    @staticmethod
    def format_neurodivergence(
            schemas: list[list[S]],
            full_access: bool
    ) -> str:
        characteristic_texts: list[str] = []
        accuracy_percents: list[float] = []
        last_update_list: list[datetime] = []

        for schema_row in schemas:
            match schema_row[0].__class__.__name__:
                case AutismSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter().format_autism_profile(
                        schema_row,
                        full_access
                    )
                case ADHDSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter().format_adhd_profile(
                        schema_row,
                        full_access
                    )
                case _:
                    raise

            characteristic_texts.append(characteristic_info.characteristic_text)
            accuracy_percents.append(characteristic_info.accuracy_percent)
            last_update_list.append(characteristic_info.last_update)

        # [ общий текст ]
        all_text: str = ''.join(characteristic_texts)

        # [ точность ]
        accuracy_percent: float = math.fsum(accuracy_percents) / len(accuracy_percents) if accuracy_percents else 0.0
        accuracy_percent = math.ceil(accuracy_percent * 100)

        # [ дата ]
        last_update = min(last_update_list)
        last_update_text = get_date_word_from_iso(last_update)

        verdict = ""
        if accuracy_percent < 0.24:
            verdict = "Эта характеристика не окончательная! Продолжайте рассказывать о себе!\n\n"

        return MessageText.CHARACTERISTIC_LISTING_GROUP.format(
            characteristic_name="Нейроотличия (Аутизм, СДВГ)",
            characteristic=all_text,
            accuracy_percent=accuracy_percent,
            last_update=last_update_text,
            verdict=verdict
        )

    @staticmethod
    def format_mood_disorders(
            schemas: list[list[S]],
            full_access: bool
    ) -> str:
        characteristic_texts: list[str] = []
        accuracy_percents: list[float] = []
        last_update_list: list[datetime] = []

        for schema_row in schemas:
            match schema_row[0].__class__.__name__:
                case DepressionDisorderSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter().format_depression_profile(
                        schema_row,
                        full_access
                    )
                case BipolarDisorderSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter().format_bipolar_profile(
                        schema_row,
                        full_access
                    )
                case _:
                    raise

            characteristic_texts.append(characteristic_info.characteristic_text)
            accuracy_percents.append(characteristic_info.accuracy_percent)
            last_update_list.append(characteristic_info.last_update)

        # [ общий текст ]
        all_text: str = ''.join(characteristic_texts)

        # [ точность ]
        accuracy_percent: float = math.fsum(accuracy_percents) / len(accuracy_percents) if accuracy_percents else 0.0
        accuracy_percent = math.ceil(accuracy_percent * 100)

        # [ дата ]
        last_update = min(last_update_list)
        last_update_text = get_date_word_from_iso(last_update)

        verdict = ""
        if accuracy_percent < 0.24:
            verdict = "Эта характеристика не окончательная! Продолжайте рассказывать о себе!\n\n"

        return MessageText.CHARACTERISTIC_LISTING_GROUP.format(
            characteristic_name="Депрессия и биполярное расстройство",
            characteristic=all_text,
            accuracy_percent=accuracy_percent,
            last_update=last_update_text,
            verdict=verdict
        )

    @staticmethod
    def format_bpd(
            schemas: list[list[S]],
            full_access: bool
    ) -> str:
        characteristic_texts: list[str] = []
        accuracy_percents: list[float] = []
        last_update_list: list[datetime] = []

        for schema_row in schemas:
            match schema_row[0].__class__.__name__:
                case BPDSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter().format_bpd_profile(
                        schema_row,
                        full_access
                    )
                case _:
                    raise

            characteristic_texts.append(characteristic_info.characteristic_text)
            accuracy_percents.append(characteristic_info.accuracy_percent)
            last_update_list.append(characteristic_info.last_update)

        # [ общий текст ]
        all_text: str = ''.join(characteristic_texts)

        # [ точность ]
        accuracy_percent: float = math.fsum(accuracy_percents) / len(accuracy_percents) if accuracy_percents else 0.0
        accuracy_percent = math.ceil(accuracy_percent * 100)

        # [ дата ]
        last_update = min(last_update_list)
        last_update_text = get_date_word_from_iso(last_update)

        verdict = ""
        if accuracy_percent < 0.24:
            verdict = "Эта характеристика не окончательная! Продолжайте рассказывать о себе!\n\n"

        return MessageText.CHARACTERISTIC_LISTING_SINGLE.format(
            characteristic=all_text,
            accuracy_percent=accuracy_percent,
            last_update=last_update_text,
            verdict=verdict
        )

    @staticmethod
    def format_dissociative(
            schemas: list[list[S]],
            full_access: bool
    ) -> str:
        characteristic_texts: list[str] = []
        accuracy_percents: list[float] = []
        last_update_list: list[datetime] = []

        for schema_row in schemas:
            match schema_row[0].__class__.__name__:
                case DissociativeSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter().format_dissociative_profile(
                        schema_row,
                        full_access
                    )
                case _:
                    raise

            characteristic_texts.append(characteristic_info.characteristic_text)
            accuracy_percents.append(characteristic_info.accuracy_percent)
            last_update_list.append(characteristic_info.last_update)

        # [ общий текст ]
        all_text: str = ''.join(characteristic_texts)

        # [ точность ]
        accuracy_percent: float = math.fsum(accuracy_percents) / len(accuracy_percents) if accuracy_percents else 0.0
        accuracy_percent = math.ceil(accuracy_percent * 100)

        # [ дата ]
        last_update = min(last_update_list)
        last_update_text = get_date_word_from_iso(last_update)

        verdict = ""
        if accuracy_percent < 0.24:
            verdict = "Эта характеристика не окончательная! Продолжайте рассказывать о себе!\n\n"

        return MessageText.CHARACTERISTIC_LISTING_SINGLE.format(
            characteristic=all_text,
            accuracy_percent=accuracy_percent,
            last_update=last_update_text,
            verdict=verdict
        )

    @staticmethod
    def format_anxiety_stress(
            schemas: list[list[S]],
            full_access: bool
    ) -> str:
        characteristic_texts: list[str] = []
        accuracy_percents: list[float] = []
        last_update_list: list[datetime] = []

        for schema_row in schemas:
            match schema_row[0].__class__.__name__:
                case PanicSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter().format_panic_profile(
                        schema_row,
                        full_access
                    )
                case GDRSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter().format_gdr_profile(
                        schema_row,
                        full_access
                    )
                case PTSDSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter().format_ptsd_profile(
                        schema_row,
                        full_access
                    )
                case _:
                    raise

            characteristic_texts.append(characteristic_info.characteristic_text)
            accuracy_percents.append(characteristic_info.accuracy_percent)
            last_update_list.append(characteristic_info.last_update)

        # [ общий текст ]
        all_text: str = ''.join(characteristic_texts)

        # [ точность ]
        accuracy_percent: float = math.fsum(accuracy_percents) / len(accuracy_percents) if accuracy_percents else 0.0
        accuracy_percent = math.ceil(accuracy_percent * 100)

        # [ дата ]
        last_update = min(last_update_list)
        last_update_text = get_date_word_from_iso(last_update)

        verdict = ""
        if accuracy_percent < 0.24:
            verdict = "Эта характеристика не окончательная! Продолжайте рассказывать о себе!\n\n"

        return MessageText.CHARACTERISTIC_LISTING_GROUP.format(
            characteristic_name="Тревога и стресс",
            characteristic=all_text,
            accuracy_percent=accuracy_percent,
            last_update=last_update_text,
            verdict=verdict
        )

    @staticmethod
    def format_body_image_eating(
            schemas: list[list[S]],
            full_access: bool
    ) -> str:
        characteristic_texts: list[str] = []
        accuracy_percents: list[float] = []
        last_update_list: list[datetime] = []

        for schema_row in schemas:
            match schema_row[0].__class__.__name__:
                case LooksSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter().format_looks_profile(
                        schema_row,
                        full_access
                    )
                case EatingSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter().format_eating_profile(
                        schema_row,
                        full_access
                    )
                case _:
                    raise

            characteristic_texts.append(characteristic_info.characteristic_text)
            accuracy_percents.append(characteristic_info.accuracy_percent)
            last_update_list.append(characteristic_info.last_update)

        # [ общий текст ]
        all_text: str = ''.join(characteristic_texts)

        # [ точность ]
        accuracy_percent: float = math.fsum(accuracy_percents) / len(accuracy_percents) if accuracy_percents else 0.0
        accuracy_percent = math.ceil(accuracy_percent * 100)

        # [ дата ]
        last_update = min(last_update_list)
        last_update_text = get_date_word_from_iso(last_update)

        verdict = ""
        if accuracy_percent < 0.24:
            verdict = "Эта характеристика не окончательная! Продолжайте рассказывать о себе!\n\n"

        return MessageText.CHARACTERISTIC_LISTING_GROUP.format(
            characteristic_name="Дисморфофобия и РПП",
            characteristic=all_text,
            accuracy_percent=accuracy_percent,
            last_update=last_update_text,
            verdict=verdict
        )

    @staticmethod
    def format_triads(
            schemas: list[list[S]],
            full_access: bool
    ) -> str:
        characteristic_texts: list[str] = []
        accuracy_percents: list[float] = []
        last_update_list: list[datetime] = []

        for schema_row in schemas:
            match schema_row[0].__class__.__name__:
                case DarkTriadsSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter().format_dark_triad_profile(
                        schema_row,
                        full_access
                    )
                case LightTriadsSchema.__name__:
                    characteristic_info = CharacteristicMessageFormatter().format_light_triad_profile(
                        schema_row,
                        full_access
                    )
                case _:
                    raise

            characteristic_texts.append(characteristic_info.characteristic_text)
            accuracy_percents.append(characteristic_info.accuracy_percent)
            last_update_list.append(characteristic_info.last_update)

        # [ общий текст ]
        all_text: str = ''.join(characteristic_texts)

        # [ точность ]
        accuracy_percent: float = math.fsum(accuracy_percents) / len(accuracy_percents) if accuracy_percents else 0.0
        accuracy_percent = math.ceil(accuracy_percent * 100)

        # [ дата ]
        last_update = min(last_update_list)
        last_update_text = get_date_word_from_iso(last_update)

        verdict = ""
        if accuracy_percent < 0.24:
            verdict = "Эта характеристика не окончательная! Продолжайте рассказывать о себе!\n\n"

        return MessageText.CHARACTERISTIC_LISTING_GROUP.format(
            characteristic_name="Тёмная и Светлая триады",
            characteristic=all_text,
            accuracy_percent=accuracy_percent,
            last_update=last_update_text,
            verdict=verdict
        )

    @staticmethod
    def format_social_profile(schemas: list[SocialProfileSchema], full_access: bool) -> CharacteristicInfo:
        fields: tuple

        schema: SocialProfileSchema = schemas[0]
        previous: SocialProfileSchema
        if len(schemas) > 1:
            previous = schemas[1]
        else:
            previous = schema

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
        previous: CognitiveProfileSchema
        if len(schemas) > 1:
            previous = schemas[1]
        else:
            previous = schema

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
        fields: tuple

        schema: EmotionalProfileSchema = schemas[0]
        previous: EmotionalProfileSchema
        if len(schemas) > 1:
            previous = schemas[1]
        else:
            previous = schema

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
        previous: BehavioralProfileSchema
        if len(schemas) > 1:
            previous = schemas[1]
        else:
            previous = schema

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
        previous: DarkTriadsSchema
        if len(schemas) > 1:
            previous = schemas[1]
        else:
            previous = schema

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

        return MessageText.CHARACTERISTIC_LISTING_GROUP.format(
            characteristic_name=characteristic_name,
            characteristic=characteristic,
            accuracy_percent=math.ceil(schema.accuracy_percent * 100),
            last_update=last_update,
        )

    @staticmethod
    def format_autism_profile(schemas: list[AutismSchema], full_access: bool) -> CharacteristicInfo:
        fields: tuple

        schema: AutismSchema = schemas[0]
        previous: AutismSchema
        if len(schemas) > 1:
            previous = schemas[1]
        else:
            previous = schema

        if full_access:
            fields = (
                f"<b>— Аутистические черты:</b> {format_value(schema.autism, 'autism', previous)}" if schema.autism is not None else "",
                f"<b>— Нарушения социальной коммуникации:</b> {format_value(schema.autism_social, 'autism_social', previous)}" if schema.autism_social is not None else "",
                f"<b>— Ограниченные интересы / ритуалы:</b> {format_value(schema.autism_interests, 'autism_interests', previous)}" if schema.autism_interests is not None else "",
                f"<b>— Маскировка:</b> {format_value(schema.masking, 'masking', previous)}" if schema.masking is not None else "",
                f"<b>— Сенсорная перегрузка:</b> {format_value(schema.sensory_overload, 'sensory_overload', previous)}" if schema.sensory_overload is not None else "",
            )
        else:
            fields = (
                f"<b>— Аутистические черты:</b> {format_value(schema.autism, 'autism', previous)}" if schema.autism is not None else "",
                f"<b>— Нарушения социальной коммуникации:</b> {format_value(schema.autism_social, 'autism_social', previous)}" if schema.autism_social is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 3 полей необходим полный доступ</i>",
            )

        characteristic: str = "🧠 <b>Аутистические черты</b>\n" + "<blockquote>" + '\n'.join(
            [field for field in fields if field]) + "</blockquote>\n\n"

        return CharacteristicInfo(
            accuracy_percent=schema.accuracy_percent,
            characteristic_text=characteristic,
            last_update=schema.updated_at
        )

    @staticmethod
    def format_adhd_profile(schemas: list[ADHDSchema], full_access: bool) -> CharacteristicInfo:
        fields: tuple

        schema: ADHDSchema = schemas[0]
        previous: ADHDSchema
        if len(schemas) > 1:
            previous = schemas[1]
        else:
            previous = schema

        if full_access:
            fields = (
                f"<b>— Уровень СДВГ:</b> {format_value(schema.adhd, 'adhd', previous)}" if schema.adhd is not None else "",
                f"<b>— Невнимательность:</b> {format_value(schema.adhd_inattention, 'adhd_inattention', previous)}" if schema.adhd_inattention is not None else "",
                f"<b>— Гиперактивность:</b> {format_value(schema.adhd_hyperactivity, 'adhd_hyperactivity', previous)}" if schema.adhd_hyperactivity is not None else "",
                f"<b>— Гиперфокус:</b> {format_value(schema.hyperfocus, 'hyperfocus', previous)}" if schema.hyperfocus is not None else "",
                f"<b>— Внутренняя гиперактивность:</b> {format_value(schema.internal_hyperactivity, 'internal_hyperactivity', previous)}" if schema.internal_hyperactivity is not None else "",
                f"<b>— Тайм-слепота:</b> {format_value(schema.time_blindness, 'time_blindness', previous)}" if schema.time_blindness is not None else "",
                f"<b>— Проблемы с мотивацией:</b> {format_value(schema.motivation_problems, 'motivation_problems', previous)}" if schema.motivation_problems is not None else "",
            )
        else:
            fields = (
                f"<b>— Уровень СДВГ:</b> {format_value(schema.adhd, 'adhd', previous)}" if schema.adhd is not None else "",
                f"<b>— Невнимательность:</b> {format_value(schema.adhd_inattention, 'adhd_inattention', previous)}" if schema.adhd_inattention is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 5 полей необходим полный доступ</i>",
            )

        characteristic: str = "🧬 <b>СДВГ</b>\n" + "<blockquote>" + '\n'.join(
            [field for field in fields if field]) + "</blockquote>\n\n"

        return CharacteristicInfo(
            accuracy_percent=schema.accuracy_percent,
            characteristic_text=characteristic,
            last_update=schema.updated_at
        )

    @staticmethod
    def format_humor_profile(schemas: list[HumorProfileSchema], full_access: bool) -> CharacteristicInfo:
        fields: tuple

        schema: HumorProfileSchema = schemas[0]
        previous: HumorProfileSchema
        if len(schemas) > 1:
            previous = schemas[1]
        else:
            previous = schema

        if full_access:
            fields = (
                f"<b>— Частота использования юмора:</b> {format_value(schema.humor_frequency, 'humor_frequency', previous)}" if schema.humor_frequency is not None else "",
                f"<b>— Аффилиативный юмор:</b> {format_value(schema.affiliative_humor, 'affiliative_humor', previous)}" if schema.affiliative_humor is not None else "",
                f"<b>— Игры слов / каламбуры:</b> {format_value(schema.puns_wordplay, 'puns_wordplay', previous)}" if schema.puns_wordplay is not None else "",
                f"<b>— Физический юмор:</b> {format_value(schema.slapstick_physical, 'slapstick_physical', previous)}" if schema.slapstick_physical is not None else "",
                f"<b>— Наблюдательный юмор:</b> {format_value(schema.observational_humor, 'observational_humor', previous)}" if schema.observational_humor is not None else "",
                f"<b>— Самоподдерживающий юмор:</b> {format_value(schema.self_enhancing_humor, 'self_enhancing_humor', previous)}" if schema.self_enhancing_humor is not None else "",
                f"<b>— Самоуничижительный юмор:</b> {format_value(schema.self_defeating_humor, 'self_defeating_humor', previous)}" if schema.self_defeating_humor is not None else "",
                f"<b>— Юмор в стрессе:</b> {format_value(schema.humor_in_stress, 'humor_in_stress', previous)}" if schema.humor_in_stress is not None else "",
                f"<b>— Агрессивный юмор:</b> {format_value(schema.aggressive_humor, 'aggressive_humor', previous)}" if schema.aggressive_humor is not None else "",
                f"<b>— Сарказм:</b> {format_value(schema.sarcasm_level, 'sarcasm_level', previous)}" if schema.sarcasm_level is not None else "",
                f"<b>— Чёрный юмор:</b> {format_value(schema.dark_humor, 'dark_humor', previous)}" if schema.dark_humor is not None else "",
                f"<b>— Остроумный:</b> {format_value(schema.witty_quick, 'witty_quick', previous)}" if schema.witty_quick is not None else "",
                f"<b>— Абсурдный юмор:</b> {format_value(schema.absurd_surreal, 'absurd_surreal', previous)}" if schema.absurd_surreal is not None else "",
                f"<b>— Сухой юмор:</b> {format_value(schema.dry_deadpan, 'dry_deadpan', previous)}" if schema.dry_deadpan is not None else "",
            )
        else:
            fields = (
                f"<b>— Чёрный юмор:</b> {format_value(schema.dark_humor, 'dark_humor', previous)}" if schema.dark_humor is not None else "",
                f"<b>— Частота использования юмора:</b> {format_value(schema.humor_frequency, 'humor_frequency', previous)}" if schema.humor_frequency is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 12 полей необходим полный доступ</i>",
            )

        characteristic: str = "😵‍💫 <b>Чувство юмора</b>\n" + "<blockquote>" + '\n'.join(
            [field for field in fields if field]) + "</blockquote>\n\n"

        return CharacteristicInfo(
            accuracy_percent=schema.accuracy_percent,
            characteristic_text=characteristic,
            last_update=schema.updated_at
        )

    @staticmethod
    def format_bipolar_profile(schemas: list[BipolarDisorderSchema], full_access: bool) -> CharacteristicInfo:
        fields: tuple

        schema: BipolarDisorderSchema = schemas[0]
        previous: BipolarDisorderSchema
        if len(schemas) > 1:
            previous = schemas[1]
        else:
            previous = schema

        if full_access:
            fields = (
                f"<b>— Уровень биполярного расстройства:</b> {format_value(schema.bipolar_score, 'bipolar_score', previous)}" if schema.bipolar_score is not None else "",
                f"<b>— Маниакальные эпизоды:</b> {format_value(schema.bipolar_mania, 'bipolar_mania', previous)}" if schema.bipolar_mania is not None else "",
                f"<b>— Гипоманиакальные эпизоды:</b> {format_value(schema.bipolar_hypomania, 'bipolar_hypomania', previous)}" if schema.bipolar_hypomania is not None else "",
                f"<b>— Депрессивные эпизоды:</b> {format_value(schema.bipolar_depression, 'bipolar_depression', previous)}" if schema.bipolar_depression is not None else "",
                f"<b>— Быстрая смена фаз:</b> {format_value(schema.bipolar_rapid, 'bipolar_rapid', previous)}" if schema.bipolar_rapid is not None else "",
                f"<b>— Психотические черты:</b> {format_value(schema.bipolar_psychotic, 'bipolar_psychotic', previous)}" if schema.bipolar_psychotic is not None else "",
            )
        else:
            fields = (
                f"<b>— Уровень биполярного расстройства:</b> {format_value(schema.bipolar_score, 'bipolar_score', previous)}" if schema.bipolar_score is not None else "",
                f"<b>— Маниакальные эпизоды:</b> {format_value(schema.bipolar_mania, 'bipolar_mania', previous)}" if schema.bipolar_mania is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 4 полей необходим полный доступ</i>",
            )

        characteristic: str = "🌊 <b>Биполярное расстройство</b>\n" + "<blockquote>" + '\n'.join(
            [field for field in fields if field]) + "</blockquote>\n\n"

        return CharacteristicInfo(
            accuracy_percent=schema.accuracy_percent,
            characteristic_text=characteristic,
            last_update=schema.updated_at
        )

    @staticmethod
    def format_depression_profile(schemas: list[DepressionDisorderSchema], full_access: bool) -> CharacteristicInfo:
        fields: tuple

        schema: DepressionDisorderSchema = schemas[0]
        previous: DepressionDisorderSchema
        if len(schemas) > 1:
            previous = schemas[1]
        else:
            previous = schema

        if full_access:
            fields = (
                f"<b>— Уровень депрессии:</b> {format_value(schema.depression_score, 'depression_score', previous)}" if schema.depression_score is not None else "",
                f"<b>— Ангедония (потеря удовольствия):</b> {format_value(schema.anhedonia, 'anhedonia', previous)}" if schema.anhedonia is not None else "",
                f"<b>— Усталость / истощение:</b> {format_value(schema.fatigue, 'fatigue', previous)}" if schema.fatigue is not None else "",
                f"<b>— Нарушения сна:</b> {format_value(schema.sleep_disturbance, 'sleep_disturbance', previous)}" if schema.sleep_disturbance is not None else "",
                f"<b>— Чувство никчёмности / вины:</b> {format_value(schema.worthlessness, 'worthlessness', previous)}" if schema.worthlessness is not None else "",
                f"<b>— Суицидальные мысли:</b> {format_value(schema.suicidal, 'suicidal', previous)}" if schema.suicidal is not None else "",
            )
        else:
            fields = (
                f"<b>— Уровень депрессии:</b> {format_value(schema.depression_score, 'depression_score', previous)}" if schema.depression_score is not None else "",
                f"<b>— Ангедония (потеря удовольствия):</b> {format_value(schema.anhedonia, 'anhedonia', previous)}" if schema.anhedonia is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 4 полей необходим полный доступ</i>",
            )

        characteristic: str = "😔 <b>Депрессия</b>\n" + "<blockquote>" + '\n'.join(
            [field for field in fields if field]) + "</blockquote>\n\n"

        return CharacteristicInfo(
            accuracy_percent=schema.accuracy_percent,
            characteristic_text=characteristic,
            last_update=schema.updated_at
        )

    @staticmethod
    def format_panic_profile(schemas: list[PanicSchema], full_access: bool) -> CharacteristicInfo:
        fields: tuple

        schema: PanicSchema = schemas[0]
        previous: PanicSchema
        if len(schemas) > 1:
            previous = schemas[1]
        else:
            previous = schema

        if full_access:
            fields = (
                f"<b>— Частота панических атак:</b> {format_value(schema.attack_frequency, 'attack_frequency', previous)}" if schema.attack_frequency is not None else "",
                f"<b>— Избегание ситуаций:</b> {format_value(schema.situational_avoid, 'situational_avoid', previous)}" if schema.situational_avoid is not None else "",
                f"<b>— Тревога ожидания атаки:</b> {format_value(schema.anticipatory, 'anticipatory', previous)}" if schema.anticipatory is not None else "",
                f"<b>— Страх катастрофы:</b> {format_value(schema.fear_catastrophe, 'fear_catastrophe', previous)}" if schema.fear_catastrophe is not None else "",
                f"<b>— Нарушение жизни:</b> {format_value(schema.life_impairment, 'life_impairment', previous)}" if schema.life_impairment is not None else "",
            )
        else:
            fields = (
                f"<b>— Частота панических атак:</b> {format_value(schema.attack_frequency, 'attack_frequency', previous)}" if schema.attack_frequency is not None else "",
                f"<b>— Избегание ситуаций:</b> {format_value(schema.situational_avoid, 'situational_avoid', previous)}" if schema.situational_avoid is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 3 полей необходим полный доступ</i>",
            )

        characteristic: str = "😱 <b>Паническое расстройство</b>\n" + "<blockquote>" + '\n'.join(
            [field for field in fields if field]) + "</blockquote>\n\n"

        return CharacteristicInfo(
            accuracy_percent=schema.accuracy_percent,
            characteristic_text=characteristic,
            last_update=schema.updated_at
        )

    @staticmethod
    def format_gdr_profile(schemas: list[GDRSchema], full_access: bool) -> CharacteristicInfo:
        fields: tuple

        schema: GDRSchema = schemas[0]
        previous: GDRSchema
        if len(schemas) > 1:
            previous = schemas[1]
        else:
            previous = schema

        if full_access:
            fields = (
                f"<b>— Чрезмерное беспокойство:</b> {format_value(schema.gad_worry, 'gad_worry', previous)}" if schema.gad_worry is not None else "",
                f"<b>— Трудности с контролем тревоги:</b> {format_value(schema.gad_uncontrollable, 'gad_uncontrollable', previous)}" if schema.gad_uncontrollable is not None else "",
                f"<b>— Трудности с расслаблением:</b> {format_value(schema.gad_relaxation, 'gad_relaxation', previous)}" if schema.gad_relaxation is not None else "",
                f"<b>— Мышечное напряжение:</b> {format_value(schema.gad_muscle_tension, 'gad_muscle_tension', previous)}" if schema.gad_muscle_tension is not None else "",
                f"<b>— Предчувствие катастрофы:</b> {format_value(schema.gad_catastrophic, 'gad_catastrophic', previous)}" if schema.gad_catastrophic is not None else "",
                f"<b>— Моторное беспокойство:</b> {format_value(schema.gad_restlessness, 'gad_restlessness', previous)}" if schema.gad_restlessness is not None else "",
                f"<b>— Быстрая утомляемость:</b> {format_value(schema.gad_fatigue, 'gad_fatigue', previous)}" if schema.gad_fatigue is not None else "",
                f"<b>— Проблемы с концентрацией:</b> {format_value(schema.gad_concentration, 'gad_concentration', previous)}" if schema.gad_concentration is not None else "",
                f"<b>— Раздражительность:</b> {format_value(schema.gad_irritability, 'gad_irritability', previous)}" if schema.gad_irritability is not None else "",
            )
        else:
            fields = (
                f"<b>— Чрезмерное беспокойство:</b> {format_value(schema.gad_worry, 'gad_worry', previous)}" if schema.gad_worry is not None else "",
                f"<b>— Трудности с контролем тревоги:</b> {format_value(schema.gad_uncontrollable, 'gad_uncontrollable', previous)}" if schema.gad_uncontrollable is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 7 полей необходим полный доступ</i>",
            )

        characteristic: str = "😟 <b>Генерализованная тревога</b>\n" + "<blockquote>" + '\n'.join(
            [field for field in fields if field]) + "</blockquote>\n\n"

        return CharacteristicInfo(
            accuracy_percent=schema.accuracy_percent,
            characteristic_text=characteristic,
            last_update=schema.updated_at
        )

    @staticmethod
    def format_ptsd_profile(schemas: list[PTSDSchema], full_access: bool) -> CharacteristicInfo:
        fields: tuple

        schema: PTSDSchema = schemas[0]
        previous: PTSDSchema
        if len(schemas) > 1:
            previous = schemas[1]
        else:
            previous = schema

        if full_access:
            fields = (
                f"<b>— Уровень ПТСР:</b> {format_value(schema.ptsd, 'ptsd', previous)}" if schema.ptsd is not None else "",
                f"<b>— Флэшбэки / интрузии:</b> {format_value(schema.ptsd_intrusions, 'ptsd_intrusions', previous)}" if schema.ptsd_intrusions is not None else "",
                f"<b>— Негативные изменения в мышлении:</b> {format_value(schema.ptsd_cognition, 'ptsd_cognition', previous)}" if schema.ptsd_cognition is not None else "",
                f"<b>— Гипервозбуждение:</b> {format_value(schema.ptsd_arousal, 'ptsd_arousal', previous)}" if schema.ptsd_arousal is not None else "",
                f"<b>— Нарушения самооценки:</b> {format_value(schema.ptsd_self, 'ptsd_self', previous)}" if schema.ptsd_self is not None else "",
                f"<b>— Избегание триггеров:</b> {format_value(schema.ptsd_avoidance, 'ptsd_avoidance', previous)}" if schema.ptsd_avoidance is not None else "",
                f"<b>— Нарушения в отношениях:</b> {format_value(schema.ptsd_relations, 'ptsd_relations', previous)}" if schema.ptsd_relations is not None else "",
            )
        else:
            fields = (
                f"<b>— Уровень ПТСР:</b> {format_value(schema.ptsd, 'ptsd', previous)}" if schema.ptsd is not None else "",
                f"<b>— Флэшбэки / интрузии:</b> {format_value(schema.ptsd_intrusions, 'ptsd_intrusions', previous)}" if schema.ptsd_intrusions is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 5 полей необходим полный доступ</i>",
            )

        characteristic: str = "🪖 <b>ПТСР</b>\n" + "<blockquote>" + '\n'.join(
            [field for field in fields if field]) + "</blockquote>\n\n"

        return CharacteristicInfo(
            accuracy_percent=schema.accuracy_percent,
            characteristic_text=characteristic,
            last_update=schema.updated_at
        )

    @staticmethod
    def format_dissociative_profile(schemas: list[DissociativeSchema], full_access: bool) -> CharacteristicInfo:
        fields: tuple

        schema: DissociativeSchema = schemas[0]
        previous: DissociativeSchema
        if len(schemas) > 1:
            previous = schemas[1]
        else:
            previous = schema

        if full_access:
            fields = (
                f"<b>— Диссоциативные симптомы:</b> {format_value(schema.dissociative, 'dissociative', previous)}" if schema.dissociative is not None else "",
                f"<b>— Деперсонализация / дереализация:</b> {format_value(schema.depersonalization, 'depersonalization', previous)}" if schema.depersonalization is not None else "",
                f"<b>— Амнезия:</b> {format_value(schema.amnesia, 'amnesia', previous)}" if schema.amnesia is not None else "",
                f"<b>— Диссоциативное расстройство идентичности:</b> {format_value(schema.did, 'did', previous)}" if schema.did is not None else "",
            )
        else:
            fields = (
                f"<b>— Диссоциативные симптомы:</b> {format_value(schema.dissociative, 'dissociative', previous)}" if schema.dissociative is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 3 полей необходим полный доступ</i>",
            )

        characteristic: str = "🌫️ <b>Диссоциативные расстройства</b>\n" + "<blockquote>" + '\n'.join(
            [field for field in fields if field]) + "</blockquote>\n\n"

        return CharacteristicInfo(
            accuracy_percent=schema.accuracy_percent,
            characteristic_text=characteristic,
            last_update=schema.updated_at
        )

    @staticmethod
    def format_bpd_profile(schemas: list[BPDSchema], full_access: bool) -> CharacteristicInfo:
        fields: tuple

        schema: BPDSchema = schemas[0]
        previous: BPDSchema
        if len(schemas) > 1:
            previous = schemas[1]
        else:
            previous = schema

        if full_access:
            fields = (
                f"<b>— Уровень ПРЛ:</b> {format_value(schema.bpd_severity, 'bpd_severity', previous)}" if schema.bpd_severity is not None else "",
                f"<b>— Страх брошенности:</b> {format_value(schema.bpd_abandonment, 'bpd_abandonment', previous)}" if schema.bpd_abandonment is not None else "",
                f"<b>— Нестабильные отношения:</b> {format_value(schema.bpd_unstable_relations, 'bpd_unstable_relations', previous)}" if schema.bpd_unstable_relations is not None else "",
                f"<b>— Нарушение идентичности:</b> {format_value(schema.bpd_identity, 'bpd_identity', previous)}" if schema.bpd_identity is not None else "",
                f"<b>— Импульсивность:</b> {format_value(schema.bpd_impulsivity, 'bpd_impulsivity', previous)}" if schema.bpd_impulsivity is not None else "",
                f"<b>— Перепады настроения:</b> {format_value(schema.bpd_mood_swings, 'bpd_mood_swings', previous)}" if schema.bpd_mood_swings is not None else "",
                f"<b>— Чувство пустоты:</b> {format_value(schema.bpd_emptiness, 'bpd_emptiness', previous)}" if schema.bpd_emptiness is not None else "",
                f"<b>— Неадекватный гнев:</b> {format_value(schema.bpd_anger, 'bpd_anger', previous)}" if schema.bpd_anger is not None else "",
                f"<b>— Параноидные идеи:</b> {format_value(schema.bpd_paranoia, 'bpd_paranoia', previous)}" if schema.bpd_paranoia is not None else "",
                f"<b>— Суицидальное поведение / самоповреждения:</b> {format_value(schema.bpd_suicidal, 'bpd_suicidal', previous)}" if schema.bpd_suicidal is not None else "",
            )
        else:
            fields = (
                f"<b>— Уровень ПРЛ:</b> {format_value(schema.bpd_severity, 'bpd_severity', previous)}" if schema.bpd_severity is not None else "",
                f"<b>— Страх брошенности:</b> {format_value(schema.bpd_abandonment, 'bpd_abandonment', previous)}" if schema.bpd_abandonment is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 8 полей необходим полный доступ</i>",
            )

        characteristic: str = "🎭 <b>Пограничное расстройство личности</b>\n" + "<blockquote>" + '\n'.join(
            [field for field in fields if field]) + "</blockquote>\n\n"

        return CharacteristicInfo(
            accuracy_percent=schema.accuracy_percent,
            characteristic_text=characteristic,
            last_update=schema.updated_at
        )

    @staticmethod
    def format_looks_profile(schemas: list[LooksSchema], full_access: bool) -> CharacteristicInfo:
        fields: tuple

        schema: LooksSchema = schemas[0]
        previous: LooksSchema
        if len(schemas) > 1:
            previous = schemas[1]
        else:
            previous = schema

        if full_access:
            fields = (
                f"<b>— Уровень дисморфофобии:</b> {format_value(schema.bdd_general, 'bdd_general', previous)}" if schema.bdd_general is not None else "",
                f"<b>— Мышечная дисморфия:</b> {format_value(schema.muscle_dysmorphia, 'muscle_dysmorphia', previous)}" if schema.muscle_dysmorphia is not None else "",
                f"<b>— Озабоченность кожей / акне:</b> {format_value(schema.skin_hair_focus, 'skin_hair_focus', previous)}" if schema.skin_hair_focus is not None else "",
                f"<b>— Облысение / волосы:</b> {format_value(schema.hair_focus, 'hair_focus', previous)}" if schema.hair_focus is not None else "",
                f"<b>— Черты лица:</b> {format_value(schema.facial_features, 'facial_features', previous)}" if schema.facial_features is not None else "",
                f"<b>— Жир / вес тела:</b> {format_value(schema.body_fat, 'body_fat', previous)}" if schema.body_fat is not None else "",
                f"<b>— Гениталии / размер:</b> {format_value(schema.genitals_size, 'genitals_size', previous)}" if schema.genitals_size is not None else "",
                f"<b>— Рост / пропорции:</b> {format_value(schema.height_stature, 'height_stature', previous)}" if schema.height_stature is not None else "",
                f"<b>— Старение:</b> {format_value(schema.aging, 'aging', previous)}" if schema.aging is not None else "",
                f"<b>— Поиск подтверждения:</b> {format_value(schema.reassurance, 'reassurance', previous)}" if schema.reassurance is not None else "",
                f"<b>— Нарушение жизни:</b> {format_value(schema.impairment, 'impairment', previous)}" if schema.impairment is not None else "",
            )
        else:
            fields = (
                f"<b>— Уровень дисморфофобии:</b> {format_value(schema.bdd_general, 'bdd_general', previous)}" if schema.bdd_general is not None else "",
                f"<b>— Мышечная дисморфия:</b> {format_value(schema.muscle_dysmorphia, 'muscle_dysmorphia', previous)}" if schema.muscle_dysmorphia is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 9 полей необходим полный доступ</i>",
            )

        characteristic: str = "🪞 <b>Дисморфофобия</b>\n" + "<blockquote>" + '\n'.join(
            [field for field in fields if field]) + "</blockquote>\n\n"

        return CharacteristicInfo(
            accuracy_percent=schema.accuracy_percent,
            characteristic_text=characteristic,
            last_update=schema.updated_at
        )

    @staticmethod
    def format_eating_profile(schemas: list[EatingSchema], full_access: bool) -> CharacteristicInfo:
        fields: tuple

        schema: EatingSchema = schemas[0]
        previous: EatingSchema
        if len(schemas) > 1:
            previous = schemas[1]
        else:
            previous = schema

        if full_access:
            fields = (
                f"<b>— Общий уровень РПП:</b> {format_value(schema.eating, 'eating', previous)}" if schema.eating is not None else "",
                f"<b>— Анорексия / потеря аппетита:</b> {format_value(schema.anorexia, 'anorexia', previous)}" if schema.anorexia is not None else "",
                f"<b>— Булимия:</b> {format_value(schema.bulimia, 'bulimia', previous)}" if schema.bulimia is not None else "",
                f"<b>— Компульсивное переедание:</b> {format_value(schema.binge, 'binge', previous)}" if schema.binge is not None else "",
                f"<b>— Дистресс от образа тела:</b> {format_value(schema.body_image_distress, 'body_image_distress', previous)}" if schema.body_image_distress is not None else "",
                f"<b>— Компенсаторное поведение:</b> {format_value(schema.compensatory_behaviors, 'compensatory_behaviors', previous)}" if schema.compensatory_behaviors is not None else "",
            )
        else:
            fields = (
                f"<b>— Общий уровень РПП:</b> {format_value(schema.eating, 'eating', previous)}" if schema.eating is not None else "",
                f"<b>— Анорексия / потеря аппетита:</b> {format_value(schema.anorexia, 'anorexia', previous)}" if schema.anorexia is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 4 полей необходим полный доступ</i>",
            )

        characteristic: str = "🍽️ <b>Пищевое поведение</b>\n" + "<blockquote>" + '\n'.join(
            [field for field in fields if field]) + "</blockquote>\n\n"

        return CharacteristicInfo(
            accuracy_percent=schema.accuracy_percent,
            characteristic_text=characteristic,
            last_update=schema.updated_at
        )

    @staticmethod
    def format_dark_triad_profile(schemas: list[DarkTriadsSchema], full_access: bool) -> CharacteristicInfo:
        fields: tuple

        schema: DarkTriadsSchema = schemas[0]
        previous: DarkTriadsSchema
        if len(schemas) > 1:
            previous = schemas[1]
        else:
            previous = schema

        if full_access:
            fields = (
                f"<b>— Цинизм:</b> {format_value(schema.cynicism, 'cynicism', previous)}" if schema.cynicism is not None else "",
                f"<b>— Нарциссизм:</b> {format_value(schema.narcissism, 'narcissism', previous)}" if schema.narcissism is not None else "",
                f"<b>— Макиавеллизм:</b> {format_value(schema.machiavellianism, 'machiavellianism', previous)}" if schema.machiavellianism is not None else "",
                f"<b>— Психотизм:</b> {format_value(schema.psychoticism, 'psychoticism', previous)}" if schema.psychoticism is not None else "",
            )
        else:
            fields = (
                f"<b>— Цинизм:</b> {format_value(schema.cynicism, 'cynicism', previous)}" if schema.cynicism is not None else "",
                f"<b>— Нарциссизм:</b> {format_value(schema.narcissism, 'narcissism', previous)}" if schema.narcissism is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 2 полей необходим полный доступ</i>",
            )

        characteristic: str = "🖤 <b>Тёмная триада</b>\n" + "<blockquote>" + '\n'.join(
            [field for field in fields if field]) + "</blockquote>\n\n"

        return CharacteristicInfo(
            accuracy_percent=schema.accuracy_percent,
            characteristic_text=characteristic,
            last_update=schema.updated_at
        )

    @staticmethod
    def format_light_triad_profile(schemas: list[LightTriadsSchema], full_access: bool) -> CharacteristicInfo:
        fields: tuple

        schema: LightTriadsSchema = schemas[0]
        previous: LightTriadsSchema
        if len(schemas) > 1:
            previous = schemas[1]
        else:
            previous = schema

        if full_access:
            fields = (
                f"<b>— Вера в человечность:</b> {format_value(schema.faith_in_humanity, 'faith_in_humanity', previous)}" if schema.faith_in_humanity is not None else "",
                f"<b>— Гуманизм:</b> {format_value(schema.humanism, 'humanism', previous)}" if schema.humanism is not None else "",
                f"<b>— Кантианство (уважение к другим):</b> {format_value(schema.kantianism, 'kantianism', previous)}" if schema.kantianism is not None else "",
                f"<b>— Скромность:</b> {format_value(schema.humility, 'humility', previous)}" if schema.humility is not None else "",
            )
        else:
            fields = (
                f"<b>— Вера в человечность:</b> {format_value(schema.faith_in_humanity, 'faith_in_humanity', previous)}" if schema.faith_in_humanity is not None else "",
                f"<b>— Гуманизм:</b> {format_value(schema.humanism, 'humanism', previous)}" if schema.humanism is not None else "",
                f"<b>— ...</b>",
                f"<i>для просмотра ещё 2 полей необходим полный доступ</i>",
            )

        characteristic: str = "🌟 <b>Светлая триада</b>\n" + "<blockquote>" + '\n'.join(
            [field for field in fields if field]) + "</blockquote>\n\n"

        return CharacteristicInfo(
            accuracy_percent=schema.accuracy_percent,
            characteristic_text=characteristic,
            last_update=schema.updated_at
        )

    class characteristic_formatter:
        """Шаблоны с форматированием"""

        @staticmethod
        def get_characteristic_text_by_schema(
                formatter_name: str
        ) -> Callable[[list[list[S]], bool], str]:
            # [ base ]
            TRAITS_CORE = CharacteristicMessageFormatter.format_traits_core

            TRIADS = CharacteristicMessageFormatter.format_triads

            HUMOR_PROFILE = CharacteristicMessageFormatter.format_humor

            # [ clinical ]
            NEURO_DIVERGENCE = CharacteristicMessageFormatter.format_neurodivergence
            MOOD_DISORDERS = CharacteristicMessageFormatter.format_mood_disorders
            BPD_DISORDER = CharacteristicMessageFormatter.format_bpd
            DISSOCIATIVE_DISORDER = CharacteristicMessageFormatter.format_dissociative
            ANXIETY_DISORDERS = CharacteristicMessageFormatter.format_anxiety_stress
            LOOKS_DISORDER = CharacteristicMessageFormatter.format_body_image_eating

            match formatter_name:
                case CharacteristicGroups.BASIC:
                    return TRAITS_CORE

                case CharacteristicGroups.TRIADS:
                    return TRIADS

                case CharacteristicGroups.HUMOR:
                    return HUMOR_PROFILE

                case CharacteristicGroups.NEURO:
                    return NEURO_DIVERGENCE
                case CharacteristicGroups.MOOD_DISORDERS:
                    return MOOD_DISORDERS
                case CharacteristicGroups.BPD:
                    return BPD_DISORDER
                case CharacteristicGroups.DISSOCIATIVE_DISORDER:
                    return DISSOCIATIVE_DISORDER
                case CharacteristicGroups.ANXIETY:
                    return ANXIETY_DISORDERS
                case CharacteristicGroups.LOOKS:
                    return LOOKS_DISORDER
                case _:
                    raise ValueError(f"Unknown characteristic group: {formatter_name}")
