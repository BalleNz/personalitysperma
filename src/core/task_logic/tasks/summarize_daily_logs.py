import datetime as dt
import uuid

import consts
from src.infrastructure.database.repository.user_repo import UserRepository
from src.core.schemas.assistant_response import SummaryResponseSchema
from src.core.services.assistant_service import AssistantService
from src.core.services.service_container import get_service_container


async def summarize_daily_logs(ctx):
    """
    Ежедневная задача: сводка логов за вчера для активных пользователей.
    Запускается в 00:00.
    """
    yesterday = dt.date.today() - dt.timedelta(days=1)

    logs_size = consts.MAX_LOGS_SIZE
    max_chars = consts.MAX_CHARS

    async with get_service_container() as container:
        user_repo: UserRepository = await container.get_user_repo()
        assistant_service: AssistantService = await container.assistant_service

        user_logs: dict[uuid.UUID, list[tuple[str, str]]] = await user_repo.get_active_user_logs(
            date_filter=yesterday,
            max_logs_per_user=logs_size,
            max_chars=max_chars
        )  # user_id: [(log, str_time_hh_mm), ...]

        for user_id, logs_list in user_logs.items():
            logs_text = ' '.join([f"{time_text}: {log_text}" for log_text, time_text in logs_list])

            summary_text: SummaryResponseSchema = await assistant_service.summarize_user_daily_logs(
                date_string=yesterday.strftime("%Y-%m-%d"),
                user_logs=logs_text
            )

            return summary_text