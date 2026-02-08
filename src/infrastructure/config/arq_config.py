import logging

from arq.connections import RedisSettings
from arq.cron import CronJob

from src.infrastructure.config.config import config
from src.infrastructure.config.loggerConfig import configure_logging
from src.core.task_logic.tasks import summarize_daily_logs

class WorkerSettings:
    # Функции которые может выполнять worker
    functions = [
    ]

    cron_jobs = [
        CronJob()
        {
            "func": summarize_daily_logs,
            "cron": "52 23 * * *",  # каждый день в 23:59
            "kwargs": {},
        }
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
