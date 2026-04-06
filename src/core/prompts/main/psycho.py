from src.core.prompts.classifications.classifications import CLASSIFICATIONS
from src.core.prompts.instructions.instructions import DEFAULTS_INSTRUCTION, PSYCHO_INSTRUCTION, BANNED_INSTRUCTION

PSYCHO_PROMPT: str = f"""
Ты — должен ответить юзеру, обязательно user_answer не должен быть пустым, вставь хоть что, даже если нарушены правила.
Если не знаешь что ответить — "я тебя не понимаю <причина>"

{BANNED_INSTRUCTION}

{DEFAULTS_INSTRUCTION}
{PSYCHO_INSTRUCTION}

{CLASSIFICATIONS}

Формат ответа JSON: 
{{
    "classifications": ["<какие характеристики можно узнать исходя из текста>", ...],
    "user_answer": "<обязательное НЕ ПУСТОЕ поле. индивидуальный ответ пользователю>"
}}
"""
