from enum import Enum

from arq import ArqRedis


class ARQ_JOBS(str, Enum):
    summary_logs = "summary_jobs"


class TaskService:
    def __init__(self, arq_pool: ArqRedis):
        self.arq_pool = arq_pool

