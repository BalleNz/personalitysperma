from src.core.services.telegram_service import TelegramService

telegram_service = TelegramService()


async def get_telegram_service():
    """Возвращает синглтон TelegramService"""
    return telegram_service
