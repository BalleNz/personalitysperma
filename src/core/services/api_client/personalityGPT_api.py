from src.api.request_schemas.psycho import PsychoRequest
from src.api.request_schemas.research import ResearchDefaultRequest, ResearchSurveyRequest, ResearchSurveyFinishRequest
from src.api.response_schemas.characteristic import GetAllCharacteristicResponse
from src.api.response_schemas.psycho import PsychoResponse
from src.api.response_schemas.research import ResearchSurveyResponse, ResearchSurveyFinishResponse, \
    ResearchDefaultResponse
from src.core.enums.user import GENDER, TALKING_MODES
from src.core.schemas.diary_schema import DiarySchema
from src.core.schemas.user_schemas import UserSchema, UserTelegramDataSchema
from src.core.services.api_client.base_http_client import BaseHttpClient, HTTPMethod


class PersonalityGPT_APIClient(BaseHttpClient):
    """Универсальный клиент для DrugSearch API"""

    async def telegram_auth(self, telegram_user_data: UserTelegramDataSchema) -> str:
        response: dict = await self._request(
            HTTPMethod.POST,
            "/v1/auth/",
            request_body=telegram_user_data.model_dump()
        )
        return response["token"]

    # [ USER ]
    async def get_current_user(self, access_token: str) -> UserSchema:
        """Получение текущего пользователя"""
        return await self._request(
            HTTPMethod.GET,
            "/v1/user/",
            response_model=UserSchema,
            access_token=access_token
        )

    async def increase_used_voices(self, access_token: str) -> None:
        """Отнимает 1 голосовой запрос + invalidate cache"""
        return await self._request(
            HTTPMethod.PUT,
            endpoint="/v1/user/increase_used_voices",
            access_token=access_token
        )

    # [ DIARY ]
    async def get_diary(self, access_token: str) -> list[DiarySchema]:
        return await self._request(
            HTTPMethod.GET,
            endpoint="/v1/user/diary",
            access_token=access_token
        )

    # [ CHARACTERISTIC ]
    async def individual_psycho_check_in(self, access_token: str, request: PsychoRequest) -> PsychoResponse:
        """режим психолога"""
        return await self._request(
            HTTPMethod.POST,
            request_body=request,
            endpoint="/v1/generation/individual_psycho",
            response_model=PsychoResponse,
            access_token=access_token
        )

    async def research_default_check_in(self, access_token: str, request: ResearchDefaultRequest) -> ResearchDefaultResponse:
        """режим исследования: обычный"""
        return await self._request(
            HTTPMethod.POST,
            request_body=request,
            endpoint="/v1/generation/research/default",
            response_model=ResearchDefaultResponse,
            access_token=access_token
        )

    async def research_survey_check_in(self, access_token: str, request: ResearchSurveyRequest) -> ResearchSurveyResponse:
        """режим исследования: survey"""
        return await self._request(
            HTTPMethod.POST,
            request_body=request,
            endpoint="/v1/generation/research/survey",
            response_model=ResearchSurveyResponse,
            access_token=access_token
        )

    async def research_survey_finish(self, access_token: str, request: ResearchSurveyFinishRequest) -> PsychoResponse:
        """режим исследования: survey — финал"""
        return await self._request(
            HTTPMethod.POST,
            request_body=request,
            endpoint="/v1/generation/research/survey/finish",
            response_model=PsychoResponse,
            access_token=access_token
        )

    async def get_characteristics(self, access_token: str) -> GetAllCharacteristicResponse:
        """получить все характеристики"""
        response = await self._request(
            HTTPMethod.GET,
            endpoint="/v1/characteristic/",
            access_token=access_token
        )
        return response

    # [ SETTINGS ]
    async def change_talk_mode(self, access_token: str, talk_mode: TALKING_MODES) -> None:
        """меняет режим общения"""
        await self._request(
            HTTPMethod.PUT,
            endpoint="/v1/user/change_talking_mode",
            access_token=access_token,
            request_body={
                "talk_mode": talk_mode
            }
        )

    async def change_gender(self, gender: GENDER, access_token: str) -> None:
        """поменять гендер"""
        await self._request(
            HTTPMethod.PUT,
            endpoint="/v1/user/change_gender",
            access_token=access_token,
            request_body={
                "gender": gender
            }
        )
