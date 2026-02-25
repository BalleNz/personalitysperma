from src.bot.lexicon.message_text import MessageText
from src.core.schemas.personality_types.socionics_type import UserSocionicsSchema
from src.core.utils.mbti_formatter import get_reinin_descriptions, get_relationships_description


class Formatter:
    @staticmethod
    def format_reinin_socionics(
            mbti: UserSocionicsSchema
    ) -> str:
        text: str = str()

        reinin_text: str = get_reinin_descriptions(mbti)

        text = (
            f"{reinin_text}"
        )

        return MessageText.REININ_SOCIONICS.format(
            mbti_type=mbti.primary_type,
            text=text
        )

    @staticmethod
    def format_relationships_socionics(
            mbti_1: str,
            mbti_2: str
    ) -> str:
        """Сообщение о Взаимоотношениях между двумя mbti типами """

        text: str = get_relationships_description(mbti_1, mbti_2)

        return MessageText.SOCIONICS_RELATIONSHIPS.format(
            mbti_type=mbti_1,
            text=text
        )
