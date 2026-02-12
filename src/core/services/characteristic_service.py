import logging
import uuid
from typing import Type, Sequence, Any

from src.api.response_schemas.generation import CheckInResponse
from src.core.consts import MIN_CHARS_LENGTH_TO_GENERATE
from src.core.schemas.log_schemas import CharacteristicBatchLogSchema
from src.core.services.assistant_service import AssistantService
from src.infrastructure.database.models.base import S, M
from src.infrastructure.database.repository.characteristic_repo import CharacteristicRepository, \
    CHARACTERISTIC_SCHEMAS_TO_MODELS

logger = logging.getLogger(__name__)


class CharacteristicService:
    def __init__(
            self,
            repo: CharacteristicRepository,
            assistant_service: AssistantService
    ):
        self.repo = repo
        self.min_chars = MIN_CHARS_LENGTH_TO_GENERATE
        self.assistant_service = assistant_service

    async def check_in(
            self,
            message_text: str,
            user_characteristics: dict[str, dict[str, Any]] | None = None,
    ) -> CheckInResponse:
        """check in

        ответы с учетом текущих профилей пользователя (5 самых важных)
        """
        assistant_response: CheckInResponse = await self.assistant_service.get_check_in_response(
            user_message=message_text,
            user_characteristics=user_characteristics or {},  # передаём профиль
        )
        return assistant_response

    async def should_generate_characteristic(
            self,
            user_id: uuid.UUID,
            message_text: str,
            schema_type: Type[S],  # таблица характеристики
            telegram_id: str,
            access_token: str
    ) -> bool | None:
        """
        Определяет, пора ли генерировать/обновлять характеристику

        Если недостаточно длины, записывает лог в таблицу батчей.
        Если достаточно, обновляет таблицу характеристики и удаляет таблицу батчей.

        :param message_text: текст пользователя
        :param schema_type: схема, полученная из CHECK_IN
        """
        model_type: Type[M] = CHARACTERISTIC_SCHEMAS_TO_MODELS.get(schema_type)
        if not model_type:
            raise ValueError(f"Неизвестный тип схемы: {schema_type}")

        # Получаем существующие логи батчей
        batch_logs: Sequence[CharacteristicBatchLogSchema] = await self.repo.get_batch_logs(
            user_id=user_id,
            characteristic_type=model_type
        )

        old_logs = [log.message for log in batch_logs]
        old_logs_length = sum(len(log) for log in old_logs)
        new_log_length = len(message_text)

        if (old_logs_length + new_log_length) >= self.min_chars:
            # генерируем новую характеристику
            await self.generate_characteristic(
                user_id=user_id,
                characteristic_type=schema_type,
                batch_logs=batch_logs,
                telegram_id=telegram_id,
                access_token=access_token
            )

            # Удаляем старые логи батчей после генерации
            await self.repo.delete_batch_logs(
                user_id=user_id,
                characteristic_type=model_type
            )

            return True

        # иначе запись в таблицу батчей
        await self.repo.create_log_in_batch(
            user_id=user_id,
            characteristic_type=model_type,
            message=message_text
        )

        return False

    async def generate_characteristic(
            self,
            user_id: uuid.UUID,
            characteristic_type: type[S],
            batch_logs: Sequence[CharacteristicBatchLogSchema],
            telegram_id: str,
            access_token: str
    ) -> None:
        """
        Генерирует и сохраняет характеристику с учетом прошлой (если она есть.)
        """
        old_characteristic: S | None = await self.repo.cache_service.get_characteristic(
            characteristic_type=characteristic_type.__name__,
            access_token=access_token,
            telegram_id=telegram_id
        )

        # [ batch logs ]
        all_text = [log.message for log in batch_logs]
        if old_characteristic:
            all_text.append(str(old_characteristic.model_dump()))

        combined_text = ' '.join(all_text)

        new_characteristic: S = await self.assistant_service.generate_characteristic(
            messages_text=combined_text,
            characteristic_type=characteristic_type
        )

        if old_characteristic:
            # если старая была, нумерация продолжается
            new_characteristic.records = old_characteristic.records + 1

        await self.repo.append_characteristic(user_id=user_id, characteristic=new_characteristic,
                                              telegram_id=telegram_id)
