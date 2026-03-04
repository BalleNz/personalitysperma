import random

from src.core.enums.user import GENDER, TALKING_MODES


class MessageText:
    # [ START ]
    # TODO больше текста и форматирования
    HELLO_GENDER_SELECT = (
        "🌀 ୨୧ привет милейшее создание ♡\n\n"
        "я — твой личный дневник хаоса, где можно вывалить все триггеры, внутренние голоса и странные мысли в 3 ночи.\n\n"
        "скажи, как тебя называть сегодня? парень, девочка или просто walking glitch в этой симуляции?"
    )

    HELLO_GIRL = (
        "🌀 ♡ шиза дневник открывает для тебя свои розовые странички...\n\n"
        "моя любимая ♡\n\n"
        "я буду слушать каждый твой поток сознания "
        "и самые странные мысли 4 утра. Потом соберу из этого полный разбор твоей личности "
        "и помогу найти того, кто не убежит от твоей шизы.\n\n"
        "давай начинать? кидай своё нытьё голосом или текстом. 🤍🫧\n\n"
    )

    HELLO_MALE = (
        "🌀 ୧ шиза дневник поможет тебе стать лучшей версией себя ୨\n\n"
        "привет, дорогой друг.\n\n"
        "я выслушаю тебя, а потом разберу твою личность.\n\n"
        "можешь начать слать мне голосовые или текстовые сообщения!"
    )

    # [ MODE ]
    @staticmethod
    def choose_talking_mode(mode: TALKING_MODES) -> str:
        if mode == TALKING_MODES.RESEARCH:
            return (
                "<b>Выбран режим</b>\n\n"
                "🔍 Изучение себя:\n"
                "<blockquote>"
                "Я буду задавать вопросы для <b>изучения</b> вашей личности"
                "</blockquote>\n\n"
            )
        elif mode == TALKING_MODES.INDIVIDUAL_PSYCHO:
            return (
                "<b>Выбран режим</b>\n\n"
                "🧚 Индивидуальный психолог:\n"
                "<blockquote> "
                "Я буду учитывать твои <b>типы личности</b> и <b>характеристику</b> во время нашей тёплой беседы."
                "</blockquote>\n\n"
            )
        return ""

    # [ query messages ]
    VOICE_PROCESS = "Обработка голосового сообщения ^^"

    # [ LIMITS ]
    VOICE_LIMIT = "У тебя закончились голосовые сообщения!"

    # [ MESSAGES ABOVE KEYBOARD ]
    CHARACTERISTIC_LISTING_MESSAGE = "🌀 Выбери доступную для тебя характеристику!"
    CHARACTERISTIC_LISTING_MESSAGE_EMPTY = "На данный момент у тебя нет характеристик!\n\nПродолжай заполнять дневник ^^"

    PERSONALITY_LISTING_MESSAGE = "🌀 Здесь расположены твои типы личности! з:"

    # [ LISTING FORMATTER ]
    CHARACTERISTIC_LISTING = (
        "🌀 <b>{characteristic_name}</b>\n\n"
        "{characteristic}"
        "<b>Точность оценки:</b> {accuracy_percent}%\n"
        "<b>Последнее обновление:</b> {last_update}\n\n"
        "<i>{verdict}</i>"
    )
    CHARACTERISTIC_LISTING_GROUP = (
        "🌀 <b>{group_name}</b>\n\n"
        "{all_text}"
        "<b>Точность оценки:</b> {accuracy_percent}%\n"
        "<b>Последнее обновление:</b> {last_update}\n\n"
        "<i>{verdict}</i>"
    )

    # [ Diary ]
    @staticmethod
    def get_diary_listing_text(gender: GENDER) -> str:
        # Варианты для девочек (оригинальные + лёгкая тикток-эстетика)
        female_variants = [
            (
                "📙 <b>твой дневник</b>\n\n"
                "ежедневно в 00:00 новая страница (ну если ты сегодня опять общалась со мной до посинения)\n\n"
                "ещё один день рефлексии.. вау! 🫧"
            ),
            (
                "📙 <b>welcome to my little healing corner</b>\n\n"
                "новые записи для тебя появляются ровно в 00:00\n\n"
                "я не осуждаю. никогда. 🤍"
            ),
            (
                "୨୧ ⋅ ˚₊‧ ౨ৎ ‧₊˚ ⋅ <b>твой личный pink journal</b>\n\n"
                "каждый день в полночь — новая страничка, если ты сегодня делилась со мной своими мыслями ♡\n\n"
                "я не осуждаю. никогда. 🩰"
            ),
            (
                "📙 <b>твой секретный safe space</b>\n\n"
                "новые страницы появляются в 00:00, если сегодня ты хотя бы чуть-чуть поговорила со мной\n\n"
                "тут можно быть максимально неидеальной и всё равно любимой 🫂🪞"
            )
        ]

        male_variants = [
            (
                "📙 <b>твой дневник</b>\n\n"
                "каждый день в 00:00 новая страница (если сегодня ты общался со мной)\n\n"
                "ещё один день в разборе себя…"
            ),
            (
                "📙 <b>твой уголок для мыслей</b>\n\n"
                "новая запись появляется в полночь\n\n"
                "никакого осуждения. никогда."
            ),
            (
                "📙 <b>твой личный дневник</b>\n\n"
                "в 00:00 ждёт чистая страница, если сегодня ты поделился своими мыслями.\n\n"
                "здесь можно быть честным."
            ),
            (
                "📙 <b>твой safe space</b>\n\n"
                "новые страницы в 00:00, если ты говорил со мной\n\n"
                "тут можно не быть идеальным."
            )
        ]

        if gender == GENDER.GIRL:
            return random.choice(female_variants)

        elif gender == GENDER.MALE:
            return random.choice(male_variants)

        return (
            "📙 <b>Твой дневник</b>\n\n"
            "каждый день в 00:00 новая страница\n\n"
            "саморефлексия — лучший инструмент для развития."
        )

    DIARY_RECORD = (
        "<b>Запись:</b>\n\n"
        "— <u>{diary_context}</u>\n\n"
        "<blockquote>{text}</blockquote>\n\n"
        "<i>{date_str}</i>\n"
    )

    # [ SOCIONICS ]
    SOCIONICS = (
        "👾 <b>MBTI</b>\n\n"
        "<b>Вероятные типы</b>:\n"
        "{text}"
        "{briefly_description}\n\n"
        "<u>точность:</u> {accuracy}%\n\n"
        "<i>{verdict}</i>"
    )

    REININ_SOCIONICS = (
        "<b>🔍 <u>Глубокий анализ {mbti_type}</u></b>\n\n"
        "{text}\n\n"
    )

    SOCIONICS_RELATIONSHIPS_BRIEFLY = (
        "<b>🫂 <u>Совместимость {mbti_type} с другими типами</u></b>\n\n"
        "{text}\n\n"
        "<b>Хочешь узнать совместимость с конкретным человеком?</b>\n"
        "— Напиши его MBTI тип в сообщении 4мя буквами!"
    )

    SOCIONICS_RELATIONSHIPS = (
        "<b>🫂 <u>Совместимость {mbti_type_1} с {mbti_type_2}</u></b>\n\n"
        "{text}\n\n"
    )
