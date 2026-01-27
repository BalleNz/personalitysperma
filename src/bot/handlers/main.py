from aiogram import Router
from aiogram.types import Message

from response_schemas.generation import CheckInResponse
from src.api.request_schemas.generation import CheckInRequest
from src.core.services.api_client.personalityGPT_api import PersonalityGPT_APIClient

router = Router()


@router.message()
async def main(
        message: Message,
        api_client: PersonalityGPT_APIClient,
        access_token: str
):
    """Главное действие пользователя:
    — check_in:
    —— generation (with notification) / add to batches"""

    message_reply = await message.reply("Ожидание ответа..")

    api_request: CheckInRequest = CheckInRequest(
        message=message.text
    )

    check_in_response: CheckInResponse = await api_client.check_in(access_token, api_request)
    await message.reply(check_in_response.precise_question)
    await message_reply.delete()
