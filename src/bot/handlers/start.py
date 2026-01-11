import logging

from aiogram import Router, Bot
from aiogram.filters import CommandStart
from aiogram.fsm.context import FSMContext
from aiogram.types import Message

from bot.lexicon.message_text import MessageText

router = Router(name=__name__)
logger = logging.getLogger(name=__name__)


@router.message(CommandStart())
async def start_dialog(
        message: Message,
        state: FSMContext,
        # api_client: ...,
        # access_token: str,
        bot: Bot
):
    await state.clear()

    user_id = str(message.from_user.id)
    command_parts = message.text.split()

    # user: UserSchema = await api_client.get_current_user(
    #     access_token
    # )

    # [ referrals check ]
    if len(command_parts) > 1 and command_parts[1].startswith('ref_'):
        token = command_parts[1][4:]  # skip: 'ref_'
        referrer_telegram_id = decode_referral_token(token)

        if referrer_telegram_id and referrer_telegram_id != user_id:
            logger.info(f"REFERRAL: User {user_id} came from {referrer_telegram_id} (token: {token})")

            try:
                await api_client.new_referral(
                    access_token=access_token,
                    referrer_telegram_id=referrer_telegram_id,
                    referral_telegram_id=user_id
                )
            except Exception as ex:
                logger.error(ex)
                pass

    await message.answer(text=MessageText.HELLO)
    logger.info(f"User {user_id} has started dialog.")
