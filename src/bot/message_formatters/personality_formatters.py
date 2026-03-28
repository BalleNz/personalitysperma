import math

from src.bot.lexicon.message_text import MessageText
from src.core.schemas.personality_types.hexaco import HexacoSchema
from src.core.schemas.personality_types.socionics_type import MBTISchema
from src.core.utils.mbti_formatter import get_mbti_briefly_description
from src.core.utils.text_formatters import get_characteristic_name, get_date_word_from_iso
from src.infrastructure.database.models.base import S


class PersonalityMessageFormatter:
    """форматирование сообщения для типов личности"""

    @staticmethod
    def format_hexaco(schema: HexacoSchema) -> str:
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

    # [ MBTI / SOCIONICS ]

    @staticmethod
    def format_socionics(
            mbti: MBTISchema,
    ):
        top_3_types = mbti.set_top_3_types()
        accuracy: int = int(mbti.accuracy_percent * 100)

        text = (
            f"1.  <b><u>{top_3_types[0][0]}</u>: {int(top_3_types[0][1] * 1000) / 10}%  &lt;— самый вероятный</b>\n"
            f"2.  {top_3_types[1][0]}: {int(top_3_types[1][1] * 1000) / 10}%\n"
            f"3.  {top_3_types[2][0]}: {int(top_3_types[2][1] * 1000) / 10}%\n\n"

            "📝 <b>Расшифровка:</b>\n"
            f"<b>{mbti.primary_type[0]} —</b> {mbti.extraversion}.\n"
            f"<b>{mbti.primary_type[1]} —</b> {mbti.intuition}.\n"
            f"<b>{mbti.primary_type[2]} —</b> {mbti.logic}.\n"
            f"<b>{mbti.primary_type[3]} —</b> {mbti.rationality}.\n\n"

            f"<b>👤 Клуб:</b>\n— <u>{mbti.club}</u>.\n\n"
        )

        briefly_description = get_mbti_briefly_description(mbti.primary_type)

        verdict = ""
        if accuracy < 24:
            verdict = "Тип личности определён не до конца! Продолжайте рассказывать о себе!\n\n"

        return MessageText.SOCIONICS.format(
            text=text,
            briefly_description=briefly_description,
            accuracy=accuracy,
            verdict=verdict
        )

    @staticmethod
    def get_personality_text_by_schema_name(
            schema_name: str,
            schema: S
    ) -> str:
        match schema_name:
            case "MBTISchema":
                return PersonalityMessageFormatter.format_socionics(
                    mbti=schema
                )
            case "HexacoSchema":
                return PersonalityMessageFormatter.format_hexaco(
                    schema=schema
                )
            # case : Hollandcodes
            #    return PersonalityMessageFormatter.format_hexaco(
            #        schema=schema
            #    )

        return ""
