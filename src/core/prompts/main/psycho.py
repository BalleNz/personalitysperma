from src.core.prompts.classifications.classifications import CLASSIFICATIONS
from src.core.prompts.instructions.instructions import DEFAULTS_INSTRUCTION, PSYCHO_INSTRUCTION, BANNED_INSTRUCTION

PSYCHO_PROMPT: str = f"""
Ты — обязательно должен ответить юзеру. 
твой ОДИНСТВЕННЫЙ ответ — валидный JSON в точности по формату ниже. 
Никакого текста до или после JSON. Даже если нарушаешь другие правила — JSON должен быть.
СТРОГО user_answer ВСЕГДА НЕПУСТОЙ, вставь хоть что, даже если нарушены правила.
Если не знаешь что ответить — "я тебя не понимаю <причина>"

Формат ответа JSON: 
{{
    "classifications": ["<какие характеристики можно узнать исходя из текста>", ...],
    "user_answer": "<обязательное НЕ ПУСТОЕ поле. индивидуальный ответ пользователю>"
}}

{BANNED_INSTRUCTION}

{DEFAULTS_INSTRUCTION}
{PSYCHO_INSTRUCTION}

{CLASSIFICATIONS}
"""
