import random

from src.core.enums.user import GENDER, TALKING_MODES


class MessageText:
    # [ MAIN ]
    SURVEY_MESSAGE = (
        "{question}\n\n"
        "{answers}"
    )

    # [ HELLO START ]
    HELLO_GENDER_SELECT = (
        "🌀 ୨୧ привет <b>милейшее создание </b>♡\n\n"
        "я — <b>твой личный дневник</b>, который будет изучать тебя и строить твою личность во время нашего общения!\n\n"
        "скажи, <b>как тебя называть</b> сегодня? парень, девочка или... ты можешь выбрать любой гендер!"
    )

    HELLO_NON_BINARY = (
        "🌀 привет~ ✨\n\n"
        "я — шиза дневник, и я здесь, чтобы внимательно слушать тебя без каких-либо рамок и ожиданий.\n\n"
        "рассказывай всё, что чувствуешь и думаешь. я соберу это в глубокий разбор твоей личности.\n\n"
        "начинаем? пиши или присылай голосовые сообщения 🤍"
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

    def get_hello_message(self, gender: GENDER) -> str:
        if gender in (GENDER.WOMAN, GENDER.GIRL):
            return self.HELLO_GIRL
        elif gender in (GENDER.MALE, GENDER.MAN):
            return self.HELLO_MALE
        else:
            return self.HELLO_NON_BINARY

    # [ query messages ]
    @staticmethod
    def get_process_message(gender: GENDER) -> str:
        """Сообщение, когда бот думает над текстовым ответом"""
        PROCESS_TEXT_WOMAN = (
            "думаю над твоим ответом, моя хорошая~ ♡",
            "сейчас внимательно всё обдумаю и отвечу тебе~ ✨",
            "перевариваю твои слова, солнышко.. 💕",
            "ммм, интересно~ сейчас соберу мысли и напишу тебе~",
        )
        PROCESS_TEXT_MAN = (
            "думаю над твоим ответом..",
            "сейчас всё обдумаю и отвечу тебе.",
            "разбираюсь в твоих словах, сейчас отвечу.",
            "понял, сейчас подумаю и напишу развёрнутый ответ.",
        )
        PROCESS_TEXT_NON_BINARY = (
            "думаю над твоим ответом..",
            "сейчас внимательно всё обдумаю~",
            "перерабатываю твои слова, скоро отвечу.. ✨",
            "интересно.. сейчас соберу мысли и напишу тебе.",
        )

        if gender in (GENDER.WOMAN, GENDER.GIRL):
            return random.choice(PROCESS_TEXT_WOMAN)
        elif gender in (GENDER.MALE, GENDER.MAN):
            return random.choice(PROCESS_TEXT_MAN)
        else:
            return random.choice(PROCESS_TEXT_NON_BINARY)

    @staticmethod
    def get_process_voice(gender: str = "non_binary") -> str:
        """Сообщение, когда бот слушает голосовое сообщение"""
        PROCESS_VOICE_WOMAN = (
            "слушаю твой милый голос прямо сейчас~ ♡",
            "включаю внимательный режим.. слушаю тебя, солнышко uwu",
            "слушаю тебя очень внимательно.. 💕",
            "твой голос такой приятный~ слушаю сейчас.. ✨",
        )

        PROCESS_VOICE_MAN = (
            "слушаю тебя прямо сейчас..",
            "внимательно слушаю твой голос..",
            "слушаю.. ✨",
            "слушаю твой голос..",
        )

        PROCESS_VOICE_NON_BINARY = (
            "слушаю тебя прямо сейчас~",
            "внимательно слушаю твой голос..",
            "слушаю тебя.. говори всё, что хочешь ✨",
            "слушаю твой голос..",
        )

        if gender in (GENDER.WOMAN, GENDER.GIRL):
            return random.choice(PROCESS_VOICE_WOMAN)
        elif gender in (GENDER.MALE, GENDER.MAN):
            return random.choice(PROCESS_VOICE_MAN)
        else:
            return random.choice(PROCESS_VOICE_NON_BINARY)

    # [ LIMITS ]
    VOICE_LIMIT = "у тебя закончились голосовые сообщения ;(\n\n<i>п.с. с подпиской они будут безлимитные! ^^</i>"

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

    # [ MODE ]
    @staticmethod
    def choose_talking_mode(mode: TALKING_MODES) -> str:
        if mode == TALKING_MODES.RESEARCH:
            return (
                "<b>выбран режим</b>\n\n"
                "🔍 Изучение себя:\n"
                "<blockquote>"
                "я буду задавать вопросы для <b>изучения</b> твоей личности ^^"
                "</blockquote>\n\n"
            )
        elif mode == TALKING_MODES.INDIVIDUAL_PSYCHO:
            return (
                "<b>выбран режим</b>\n\n"
                "🧚 Индивидуальный психолог:\n"
                "<blockquote> "
                "я буду учитывать твои <b>типы личности</b> и <b>характеристику</b> во время нашей тёплой беседы."
                "</blockquote>\n\n"
            )
        return ""

    # [ DIARY ]
    @staticmethod
    def get_diary_listing_text(gender: GENDER) -> str:
        # Варианты для девочек (оригинальные + лёгкая тикток-эстетика)
        female_variants = [
            (
                "📙 <b>твой дневник</b>\n\n"
                "ежедневно в 00:00 новая страница (ну если ты общалась со мной до посинения)\n\n"
                "ещё один день рефлексии.. вау! 🫧"
            ),
            (
                "📙 <b>welcome to my little healing corner</b>\n\n"
                "новые записи для тебя появляются ровно в 00:00\n\n"
                "я не осуждаю. никогда. 🤍"
            ),
            (
                "୨୧ ⋅ ˚₊‧ ౨ৎ ‧₊˚ ⋅ <b>твой личный pink journal</b>\n\n"
                "каждый день в полночь — новая страничка, если ты делилась со мной своими мыслями в этот день ♡\n\n"
                "я не осуждаю. никогда. 🩰"
            ),
            (
                "📙 <b>твой секретный safe space</b>\n\n"
                "новые страницы появляются в 00:00, если ты хотя бы чуть-чуть поговорила со мной\n\n"
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
        non_binary_variants = [
            (
                "📙 <b>твой дневник</b>\n\n"
                "каждый день в 00:00 новая страница.\n\n"
                "ещё один день в разборе себя…"
            ),
            (
                "📙 <b>твой уголок для мыслей</b>\n\n"
                "новая запись появляется в полночь\n\n"
                "никакого осуждения. никогда."
            ),
            (
                "📙 <b>твой личный дневник</b>\n\n"
                "в 00:00 ждёт чистая страница.\n\n"
            ),
            (
                "📙 <b>твой safe space</b>\n\n"
                "новые страницы в 00:00.\n\n"
                "тут можно не быть идеальным."
            ),
            (
                "📙 <b>твой дневник</b>\n\n"
                "каждый день в 00:00 новая страница\n\n"
                "саморефлексия — лучший инструмент для развития."
            )
        ]

        if gender in (GENDER.WOMAN, GENDER.GIRL):
            return random.choice(female_variants)
        elif gender in (GENDER.MALE, GENDER.MAN):
            return random.choice(male_variants)
        else:
            return random.choice(non_binary_variants)

    DIARY_RECORD = (
        "<b>твоя запись:</b>\n\n"
        "— <u>{diary_context}</u>\n\n"
        "<blockquote>{text}</blockquote>\n\n"
        "<i>за {date_str}</i>\n"
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
        "<b>🔍 <u>твой глубокий анализ {mbti_type}</u></b>\n\n"
        "{text}\n\n"
    )

    SOCIONICS_RELATIONSHIPS_BRIEFLY = (
        "<b>🫂 <u>твоя совместимость {mbti_type} с другими типами</u></b>\n\n"
        "{text}\n\n"
        "<b>Хочешь узнать совместимость с конкретным человеком?</b>\n"
        "— Напиши его MBTI тип в сообщении 4мя буквами!"
    )

    SOCIONICS_RELATIONSHIPS = (
        "<b>🫂 <u>твоя совместимость {mbti_type_1} с {mbti_type_2}</u></b>\n\n"
        "{text}\n\n"
    )

    # [ TYPIFICATION ]
    TYPIFICATION_LISTING = (
        "📑 выбери доступное для тебя типирование c:"
    )

    TYPIFICATION_LISTING_EMPTY = (
        "📑 все типирования пройдены!\n\n"
        "если хочешь стереть один из типов личности и пройти заново тесты — напиши /reset\n"
        "— тебе откроется меню с выбором характеристик, которые ты можешь стереть ^^"
    )

    @staticmethod
    def get_typification_end_message(
            gender: GENDER,
            typification_name_text: str
    ) -> str:
        typification_end_phrases_girls: tuple[str, ...] = (
            f"ты успешно прошла типирование «{typification_name_text}» ‧₊˚\n\n"
            f"хочешь результаты? ~",

            f"готовооо~ ты прошла «{typification_name_text}» ‧₊˚\n\n"
            f"погнали смотреть что получилось?",

            f"вау, ты прошла типирование {typification_name_text} ‧₊˚\n\n"
            f"хочешь результаты? ~",

            f"типирование «{typification_name_text}» пройдено ‧₊˚\n\n"
            f"посмотрим твой результат? ~",
        )

        typification_end_phrases_boys: tuple[str, ...] = (
            f"ты успешно прошёл типирование «{typification_name_text}»\n\n"
            f"хочешь посмотреть результаты?",

            f"готово. «{typification_name_text}» пройдено\n\n"
            f"хочешь посмотреть результаты?",

            f"типирование «{typification_name_text}» завершено\n\n"
            f"хочешь посмотреть результаты?",

            f"всё, ты прошёл «{typification_name_text}»\n\n"
            f"хочешь посмотреть результаты?",
        )

        typification_end_phrases_non_binary: tuple[str, ...] = (
            f"ты успешно прошёл(а) типирование «{typification_name_text}» ✨\n\n"
            f"хочешь посмотреть результаты?",

            f"готово~ типирование «{typification_name_text}» пройдено 🌟\n\n"
            f"хочешь посмотреть результаты? ~",

            f"типирование «{typification_name_text}» завершено\n\n"
            f"хочешь посмотреть результаты? ~",

            f"всё, ты прошёл(а) «{typification_name_text}»\n\n"
            f"хочешь посмотреть результаты? ~",
        )

        if gender in (GENDER.WOMAN, GENDER.GIRL):
            phrases = typification_end_phrases_girls
        elif gender in (GENDER.MALE, GENDER.MAN):
            phrases = typification_end_phrases_boys
        else:
            phrases = typification_end_phrases_non_binary

        return random.choice(phrases)

    @staticmethod
    def get_typification_process_message(
            is_first_question: bool,
            question: str,
            gender: GENDER,
            additional_text: str | None = ""
    ) -> str:
        """получить вопрос типирования с рандомной фразой"""
        start_phrases_first_girls: tuple[str, ...] = (
            "ответь на вопрос максимально подробно, пожалуйста~ ♡",
            "расскажи мне всё-всё как можно подробнее, ладно? з:",
            "хочу услышать твои мысли максимально подробно~ не стесняйся! uwu",
            "пиши развёрнуто и от души, моя хорошая~ мне очень-очень интересно! 💕",
            "давай честно и максимально подробно, я вся во внимании~ ✨",
            "расскажи мне прям от души, как можно подробнее, окей? nya~",
            "очень прошу ответить максимально подробно! Буду читать с огромным интересом ♡",
            "солнышко, ответь пожалуйста максимально подробно~ я очень жду твоего ответа! 💖",
        )
        start_phrases_first_man: tuple[str, ...] = (
            "ответь на вопрос максимально подробно, пожалуйста.",
            "расскажи всё как можно подробнее, хорошо?",
            "хочу услышать твой ответ максимально развёрнуто — не стесняйся.",
            "пиши подробно и от души, мне действительно интересно.",
            "давай честно и максимально подробно, я внимательно читаю.",
            "расскажи всё как есть, с максимальными деталями, окей?",
            "очень прошу ответить максимально подробно — буду внимательно читать.",
            "ответь пожалуйста максимально подробно, мне важно понять тебя правильно.",
        )
        start_phrases_first_non_binary: tuple[str, ...] = (
            "ответь на вопрос максимально подробно, пожалуйста~",
            "расскажи мне всё как можно подробнее, хорошо? ♡",
            "хочу услышать твой ответ максимально развёрнуто — не стесняйся ✨",
            "пиши подробно и от души, мне очень интересно!",
            "давай честно и максимально подробно, я внимательно слушаю~",
            "расскажи всё как можно подробнее, окей?",
            "очень прошу ответить максимально подробно — буду читать с интересом ♡",
            "ответь пожалуйста максимально подробно, я здесь и внимательно тебя читаю.",
        )

        start_phrases_process_girls: tuple[str, ...] = (
            "c: пока я обрабатываю твой предыдущий ответ, ответь пожалуйста на:",
            "♡ пока я анализирую то, что ты написал(а), расскажи мне подробненько вот это~",
            "uwu~ я сейчас обрабатываю твой прошлый ответ, а ты пока ответь максимально подробно на:",
            "ня~ пока я думаю над твоим предыдущим ответом, будь лапочкой и расскажи развёрнуто про:",
            "💕 пока я обрабатываю то, что ты мне уже рассказал(а), ответь пожалуйста очень подробно на:",
            "c: солнышко, я сейчас анализирую твой прошлый ответик~ а ты пока ответь как можно подробнее на:",
            "✨ пока я перевариваю твой предыдущий ответ, расскажи мне всё-всё-всё про вот этот вопросик:",
        )
        start_phrases_process_man: tuple[str, ...] = (
            "c: пока я обрабатываю твой предыдущий ответ, ответь пожалуйста на:",
            "Пока я анализирую твой прошлый ответ, расскажи максимально подробно вот это:",
            "Я сейчас разбираюсь с твоим предыдущим ответом, а ты пока ответь развёрнуто на:",
            "Пока я обрабатываю то, что ты написал, будь добр, ответь как можно подробнее на:",
            "Я анализирую твой прошлый ответ — а ты пока расскажи всё по делу и максимально подробно про:",
            "Пока я думаю над твоим предыдущим сообщением, ответь пожалуйста очень подробно на этот вопрос:",
            "Я сейчас перерабатываю твой прошлый ответ, а ты давай подробно разбери вот это:",
        )
        start_phrases_process_non_binary: tuple[str, ...] = (
            "c: пока я обрабатываю твой предыдущий ответ, ответь пожалуйста на:",
            "Пока я анализирую твой прошлый ответ, расскажи мне максимально подробно вот это~",
            "Я сейчас обрабатываю твой предыдущий ответ, а ты ответь как можно подробнее на:",
            "Пока я думаю над твоим прошлым сообщением, будь добр(а), расскажи развёрнуто про:",
            "Я внимательно анализирую то, что ты уже написал(а) — а ты пока ответь очень подробно на:",
            "Пока я перерабатываю твой предыдущий ответ, расскажи пожалуйста максимально подробно вот это:",
            "Я сейчас разбираюсь с твоим прошлым ответом~ ответь как можно подробнее на:",
        )

        message: str
        if is_first_question:
            if gender in (GENDER.WOMAN, GENDER.GIRL):
                message = (
                    f"{random.choice(start_phrases_first_girls)}\n\n"
                    f"{question}"
                )
            elif gender in (GENDER.MALE, GENDER.MAN):
                message = (
                    f"{random.choice(start_phrases_first_man)}\n\n"
                    f"{question}"
                )
            else:
                message = (
                    f"{random.choice(start_phrases_first_non_binary)}\n\n"
                    f"{question}"
                )
        else:
            if gender in (GENDER.WOMAN, GENDER.GIRL):
                message = (
                    f"{random.choice(start_phrases_process_girls)}\n\n"
                    f"{question}"
                )
            elif gender in (GENDER.MALE, GENDER.MAN):
                message = (
                    f"{random.choice(start_phrases_process_man)}\n\n"
                    f"{question}"
                )
            else:
                message = (
                    f"{random.choice(start_phrases_process_non_binary)}\n\n"
                    f"{question}"
                )
        return message + f"\n{additional_text}"
