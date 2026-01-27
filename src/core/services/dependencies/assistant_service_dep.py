from src.core.services.assistant_service import AssistantService


async def get_assistant_service() -> AssistantService:
    """Возвращает синглтон ассистента с клиентом ()"""
    return AssistantService()
