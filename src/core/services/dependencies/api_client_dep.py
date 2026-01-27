from src.infrastructure.config.config import config
from services.api_client.personalityGPT_api import PersonalityGPT_APIClient


def get_api_client() -> PersonalityGPT_APIClient:
    return PersonalityGPT_APIClient(base_url=config.WEBHOOK_URL)
