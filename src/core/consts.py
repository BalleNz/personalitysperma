MIN_CHARS_LENGTH_TO_GENERATE = 700  # минимальное количество символов для генерации
MIN_CHARS_LENGTH_TO_GENERATE_PERSONALITY = 800  # минимальное количество символов для генерации ТИПОВ ЛИЧНОСТИ


def get_min_chars_to_generate(generated_by_user_today_count: int) -> int:
    # TODO убрать. подумать над логикой уменьшения количества уведомлений (не ограничивая количество генераций)
    """
    ВОЗВРАЩАЕТ КОЛИЧЕСТВО СИМВОЛОВ НЕОБХОДИМЫХ ДЛЯ ГЕНЕРАЦИИ
    В ЗАВИСИМОСТИ ОТ СГЕНЕРИРОВАННЫХ ХАРАКТЕРИСТИК СЕГОДНЯ
    """
    if generated_by_user_today_count in [0, 1, 2, 3, 4]:
        return MIN_CHARS_LENGTH_TO_GENERATE

    return int(MIN_CHARS_LENGTH_TO_GENERATE * (generated_by_user_today_count + 1) // 5)


# [ CHARGES ]
FREE_VOICE_MESSAGES_COUNT = 3

# [ DIARY: summarize logs ]
MAX_LOGS_SIZE = 75
MAX_CHARS = 1500  # per log

DIARIES_ROW_COUNT_AT_KEYBOARD = 4
