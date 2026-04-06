from src.core.prompts.instructions.records_fields import FIELDS_INSTRUCTION, \
    RECORDS_INSTRUCTION_TYPIFICATION

END_TYPIFICATION_PROMPT: str = f"""
Ты профессиональный психолог мирового уровня, ты должен типировать пользователя по строго заданным правилам.

Входные данные:
{{
    "answers": ["<вопросы и ответы юзера на них>", ...],
    "old_characteristic": "<прошлая характеристика юзера, если есть>"
}}

{FIELDS_INSTRUCTION}
{RECORDS_INSTRUCTION_TYPIFICATION}

Строгий формат вывода JSON:
{{
    "new_characteristic": "<новая характеристика>"
}}

"""
