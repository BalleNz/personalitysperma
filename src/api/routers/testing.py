from typing import Annotated

from fastapi import APIRouter, Depends

from src.api.utils.auth import get_auth_user
from src.core.schemas.user_schemas import UserSchema
from src.core.services.dependencies.user_service_dep import get_user_service
from src.core.services.user_service import UserService
from src.core.task_logic.tasks.summarize_daily_logs import summarize_daily_logs

router = APIRouter(prefix="/testing")


@router.post(path="")
async def test_summary_logs(
        user: Annotated[UserSchema, Depends(get_auth_user)]
):
    """проверка генерации отчета для дневника

    берутся все логи активных юзеров за вчерашний день.
    """
    response = await summarize_daily_logs(
        None
    )

    return {
        "response": response
    }
