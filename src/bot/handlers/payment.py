from aiogram import Router

from src.bot.callbacks.callbacks import GetFullAccessCallback

router = Router()


async def get_full_access(

):
    """предложение купить полный доступ"""
    pass


@router.callback_query(GetFullAccessCallback.filter())
async def get_full_access_from_voice_limit(

):
    """предложение купить полный доступ с лимита голосовых"""

    pass
