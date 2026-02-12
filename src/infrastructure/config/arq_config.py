import logging
from typing import cast

from arq.connections import RedisSettings
from arq.cron import cron
from arq.typing import WorkerCoroutine

from src.core.task_logic.tasks.summarize_daily_logs import summarize_daily_logs
from src.infrastructure.config.config import config
from src.infrastructure.config.loggerConfig import configure_logging


class WorkerSettings:
    # Функции которые может выполнять worker
    functions = [
        summarize_daily_logs
    ]

    cron_jobs = [
        cron(
            cast(WorkerCoroutine, summarize_daily_logs),
            minute=55,
            hour=20,  # 23:55 (важно для datetime) MSK каждый день
            # unique=True,              # если нужно избегать дубликатов
            # timeout=600,              # можно переопределить глобальный
            # max_tries=3,
        )
    ]

    # Настройки Redis
    redis_settings = RedisSettings.from_dsn(config.ARQ_REDIS_URL)

    # Настройки worker
    queue_name = config.ARQ_REDIS_QUEUE
    max_jobs = config.ARQ_MAX_JOBS
    job_timeout = 600  # 10 минут timeout на задачу
    keep_result = 600  # Хранить результат 10 мин

    # [ Logger ]
    async def on_startup(self):
        """Вызывается при запуске worker"""
        configure_logging()
        logger = logging.getLogger(__name__)
        logger.info("ARQ worker started with logging configured")

    # Retry политика
    retry_jobs = True
    max_tries = 3
