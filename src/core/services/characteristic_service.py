import logging

from core.consts import MIN_CHARS_LENGTH_TO_GENERATE
from infrastructure.database.models.base import S
from infrastructure.database.repository.characteristic_repo import CharacteristicRepository

logger = logging.getLogger(__name__)


class CharacteristicService:
    def __init__(
            self,
            repo: CharacteristicRepository
    ):
        self.repo = repo,
        self.min_chars = MIN_CHARS_LENGTH_TO_GENERATE

    def should_generate_characteristic(
            self,
            new_log: str,
            table_name: ...  # таблица характеристики
    ) -> bool:
        """
        Определяет, пора ли генерировать/обновлять характеристику

        Если недостаточно длины, записывает лог в таблицу батчей.
        Если достаточно, обновляет таблицу характеристики и удаляет таблицу батчей.
        """
        old_logs: tuple = ...

        old_logs_length = sum(len(log) for log in old_logs)
        new_log_lenght = len(new_log)

        if (old_logs_length + new_log_lenght) >= self.min_chars:
            # self.generate_with_history(...)
            ...
        else:
            # запись в таблицу батчей
            ...

        ...

    def generate_characteristic(
            self,

    ) -> None:
        """
        Генерирует характеристику с учетом прошлой (если она есть.)
        """
        old_characteristic: S = ...
        new_characteristic: S = ...  # assistant_service...

        # update characteristic
        self.repo
