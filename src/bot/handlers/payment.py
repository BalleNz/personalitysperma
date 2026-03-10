from aiogram import Router
from aiogram.types import CallbackQuery

from src.bot.callbacks.callbacks import GetFullAccessCallback

router = Router()


async def get_full_access(

):
    """предложение купить полный доступ"""
    pass


@router.callback_query(GetFullAccessCallback.filter())
async def get_full_access_from_voice_limit(
     callback_query: CallbackQuery
):
    """предложение купить полный доступ с лимита голосовых"""
    await callback_query.answer()

    pass
