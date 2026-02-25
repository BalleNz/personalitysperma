import datetime as dt
import logging
import uuid

from src.core import consts
from src.core.schemas.assistant_response import SummaryResponseSchema
from src.core.services.assistant_service import AssistantService
from src.core.services.service_container import get_service_container
from src.infrastructure.database.repository.user_repo import UserRepository

logger = logging.getLogger(__name__)


async def summarize_daily_logs(ctx):
    """
    Ежедневная задача: сводка логов за вчера для активных пользователей.
    Запускается в 00:00.
    """

    logger.info("Cron-задача summarize_daily_logs запущена!")

    today = dt.date.today()

    logs_size = consts.MAX_LOGS_SIZE
    max_chars = consts.MAX_CHARS

    records: list[tuple[uuid.UUID, str, str]] = []
    telegram_ids: list[str] = []

    async with get_service_container() as container:
        user_repo: UserRepository = await container.get_user_repo()
        assistant_service: AssistantService = await container.assistant_service
        redis_service = await container.redis_service
        telegram_service = await container.telegram_service

        user_logs: dict[uuid.UUID, list[tuple[str, str]]] = await user_repo.get_active_user_logs(
            date_filter=today,
            max_logs_per_user=logs_size,
            max_chars=max_chars
        )  # user_id: [(log, str_time_hh_mm), ...]

        for user_id, logs_list in user_logs.items():
            logs_text = ' '.join([f"{time_text}: {log_text}" for log_text, time_text in logs_list])

            summary_text: SummaryResponseSchema = await assistant_service.summarize_user_daily_logs(
                user_logs=logs_text
            )

            records.append(
                (user_id, summary_text.summary_text, summary_text.context_text)
            )

            user = await user_repo.get_user(user_id)
            telegram_ids.append(user.telegram_id)

        await user_repo.bulk_create_diary_records(
            records
        )

        # [ рассылка о новой записи ]
        for tg_id in telegram_ids:
            await telegram_service.send_message(
                user_telegram_id=tg_id,
                message="у вас появилась новая запись в дневнике! ^^"
            )

        await redis_service.invalidate_all_diaries()
