import json
import logging
import uuid
from typing import Type, Sequence

from src.api.response_schemas.research import Characteristic
from src.core.consts import (
    MIN_CHARS_LENGTH_TO_GENERATE, MIN_CHARS_LENGTH_TO_GENERATE_PERSONALITY
)
from src.core.schemas.log_schemas import CharacteristicBatchLogSchema
from src.core.services.assistant_service import AssistantService
from src.core.utils.funcs import clean_characteristic_json
from src.infrastructure.database.models.base import S, M
from src.infrastructure.database.repository.characteristic_repo import CharacteristicFormat, CharacteristicRepository, \
    CHARACTERISTIC_SCHEMAS_TO_MODELS, PERSONALITY_SCHEMAS

logger = logging.getLogger(__name__)


class CharacteristicService:
    def __init__(
            self,
            repo: CharacteristicRepository,
            assistant_service: AssistantService
    ):
        self.repo = repo
        self.min_chars = MIN_CHARS_LENGTH_TO_GENERATE
        self.min_chars_personality = MIN_CHARS_LENGTH_TO_GENERATE_PERSONALITY
        self.assistant_service = assistant_service

    async def research_survey_finish(
            self,
            user_id: uuid.UUID,
            telegram_id: str,
            new_characteristics: list[Characteristic]
    ):
        """улучшает / меняет характеристику после ответа на вопрос юзера"""
        for characteristic in new_characteristics:
            schema_cls: type[S] = CharacteristicFormat.get_cls_from_schema_name(
                characteristic.characteristic_name
            )

            characteristic.characteristic["user_id"] = user_id
            data = schema_cls.model_validate(characteristic.characteristic)

            await self.repo.append_characteristic(
                user_id,
                data,
                telegram_id=telegram_id
            )

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

        Если недостаточно длины —> записывает лог в таблицу батчей.

        Если достаточно —> обновляет таблицу характеристики и удаляет таблицу батчей.

        :param message_text: текст пользователя
        :param schema_type: схема, полученная из CHECK_IN
        """
        model_type: Type[M] = CHARACTERISTIC_SCHEMAS_TO_MODELS.get(schema_type)
        if not model_type:
            raise ValueError(f"Неизвестный тип схемы: {schema_type}")

        # [ создаем батч для этого профиля харки ]
        await self.repo.create_log_in_batch(
            user_id=user_id,
            characteristic_type=model_type,
            message=message_text
        )

        # [ получаем все батчи этого профиля]
        batch_logs: Sequence[CharacteristicBatchLogSchema] = await self.repo.get_batch_logs(
            user_id=user_id,
            characteristic_type=model_type
        )

        logs = [log.message for log in batch_logs]
        logs_length = sum(len(log) for log in logs)

        min_chars: int
        match schema_type:
            case x if x in PERSONALITY_SCHEMAS:  # типы личности
                min_chars = self.min_chars_personality
            case _:  # дефолт
                min_chars = self.min_chars

        if logs_length >= min_chars:
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
        old_characteristic: S | None = (await self.repo.cache_service.get_characteristic_row(
            characteristic_name=characteristic_type.__name__,
            access_token=access_token,
            telegram_id=telegram_id
        ))[0]

        # [ batch logs + old characteristic + fields instruction]
        all_text: list[str] = [log.message + "\n" for log in batch_logs]

        cleaned: dict = clean_characteristic_json(old_characteristic or characteristic_type, False)
        header = "Текущая характеристика пользователя: "

        all_text.append(header + json.dumps(cleaned, ensure_ascii=False, indent=2))

        combined_text: str = ' '.join(all_text)

        new_characteristic: S = await self.assistant_service.generate_characteristic(
            old_characteristic=combined_text,
            characteristic_type=characteristic_type
        )
        await self.repo.append_characteristic(user_id=user_id, characteristic=new_characteristic, telegram_id=telegram_id)
