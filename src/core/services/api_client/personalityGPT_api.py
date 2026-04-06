from request_schemas.typification import TypificationRequest, TypificationGetQuestion, DeleteTypificationRequest, \
    TypificationGetStatisticsRequest
from src.api.request_schemas.check_in import CheckInRequest
from src.api.request_schemas.survey import ResearchSurveyFinishRequest
from src.api.response_schemas.characteristic import GetAllCharacteristicResponse
from src.api.response_schemas.check_in import AssistantResponse
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
    async def check_in(self, access_token: str, request: CheckInRequest) -> AssistantResponse:
        """check_in"""
        return await self._request(
            HTTPMethod.POST,
            request_body=request,
            endpoint="/v1/main/check_in",
            response_model=AssistantResponse,
            access_token=access_token
        )

    async def research_survey_finish(self, access_token: str, request: ResearchSurveyFinishRequest) -> AssistantResponse:
        """режим исследования: survey — финал"""
        return await self._request(
            HTTPMethod.POST,
            request_body=request,
            endpoint="/v1/main/research/survey/finish",
            response_model=AssistantResponse,
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

    # [ TYPIFICATION ]
    async def get_additional_text_on_mid_test(self, access_token: str, request: TypificationGetStatisticsRequest) -> str:
        """получить доп текст на середине теста"""
        response = await self._request(
            HTTPMethod.GET,
            endpoint="/v1/typifications/get_stats_on_middle_of_test",
            access_token=access_token,
            request_body=request
        )
        return response

    async def post_typification_results(self, access_token: str, request: TypificationRequest) -> None:
        """закончить типирование"""
        await self._request(
            HTTPMethod.POST,
            endpoint="/v1/typification/end_typification",
            access_token=access_token,
            request_body=request
        )

    async def get_next_question(self, access_token: str, request: TypificationGetQuestion) -> str:
        """склеить прошлый вопрос + ответ с новым вопросом"""
        return await self._request(
            HTTPMethod.GET,
            endpoint="/v1/typification/get_question",
            request_body=request,
            access_token=access_token
        )

    async def delete_typification(self, access_token: str, request: DeleteTypificationRequest) -> str:
        """склеить прошлый вопрос + ответ с новым вопросом"""
        return await self._request(
            HTTPMethod.PUT,
            endpoint="/v1/typification/delete_progress",
            request_body=request,
            access_token=access_token
        )
