import datetime
import logging
import uuid
from collections import defaultdict

import pytz
from sqlalchemy import select, update, func, text, desc
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.infrastructure.database.models.diary import UserDiary
from src.core.schemas.diary_schema import DiarySchema
from src.core.enums.user import TALKING_MODES
from src.core.schemas.user_schemas import UserSchema, UserTelegramDataSchema
from src.infrastructure.database.models.logs import UserLog
from src.infrastructure.database.models.user import User
from src.infrastructure.database.repository.base_repo import BaseRepository

logger = logging.getLogger(__name__)


class UserRepository(BaseRepository):
    def __init__(self, session: AsyncSession):
        super().__init__(model=User, session=session)

    async def get_user_from_telegram_id(self, telegram_id: str) -> UserSchema | None:
        """Возвращает схему юзера с телеграм айди"""
        stmt = (
            select(User).where(
                User.telegram_id == telegram_id
            )
        )
        result = await self.session.execute(stmt)
        user: User | None = result.scalar_one_or_none()

        if not user:
            return None

        return user.get_schema()

    async def get_user(self, user_id: uuid.UUID) -> UserSchema | None:
        """Возвращает модель юзера"""
        stmt = (
            select(User).where(
                User.id == user_id
            )
            .options(
                # [ diary ]
                selectinload(User.diary),
            )
        )
        result = await self.session.execute(stmt)
        user: User | None = result.scalar_one_or_none()
        if not user:
            return None

        return user.get_schema()

    async def get_user_diary(self, user_id: uuid.UUID) -> list[DiarySchema] | None:
        """возвращает записи с дневника пользователя"""
        stmt = (
            select(UserDiary).where(
                User.id == user_id
            )
            .order_by(desc(UserDiary.created_at))
        )
        result = await self.session.execute(stmt)
        diary_list: list[UserDiary] | None = result.scalars().all()
        if not diary_list:
            return None

        return [DiarySchema.model_validate(diary) for diary in diary_list]

    async def get_or_create_from_telegram(self, telegram_user: UserTelegramDataSchema) -> UserSchema | None:
        """
        Возвращает модель пользователя по Telegram ID если существует.
        Если не существует, создает нового пользователя по схеме из Telegram Web App.
        """
        stmt = insert(User).values(
            telegram_id=telegram_user.telegram_id,
            username=telegram_user.username,
            first_name=telegram_user.first_name,
            last_name=telegram_user.last_name
        ).on_conflict_do_update(
            index_elements=['telegram_id'],
            set_={
                'username': telegram_user.username,
                'first_name': telegram_user.first_name,
                'last_name': telegram_user.last_name
            }
        ).returning(User)

        result = await self.session.execute(stmt)
        user = result.scalar_one()
        await self.session.commit()
        return UserSchema.model_validate(user.__dict__)

    async def increase_used_voice_message(self, user_id: uuid.UUID) -> None:
        """Увеличивает использованные голосовые сообщения на 1"""
        await self.session.execute(
            update(User)
            .where(
                User.id == user_id,
                User.used_voice_messages > 0
            )
            .values(used_voice_messages=User.used_voice_messages - 1)
        )
        await self.session.flush()

    async def get_active_user_logs(
            self,
            date_filter: datetime.date,
            max_logs_per_user: int,
            max_chars: int = 500
    ) -> dict[uuid.UUID, list[tuple[str, str]]]:
        """
        Получение всех логов активных за сегодня юзеров
        """
        MSK_TZ = pytz.timezone('Europe/Moscow')

        start_date = MSK_TZ.localize(
            datetime.datetime.combine(date_filter, datetime.datetime.min.time())
        )
        end_date = MSK_TZ.localize(
            datetime.datetime.combine(
                date_filter + datetime.timedelta(days=1),
                datetime.datetime.min.time()
            )
        )
        stmt = (
            select(
                UserLog.user_id,
                func.substr(UserLog.log, 1, max_chars).label('short_log'),
                func.to_char(UserLog.created_at, 'HH24:MI').label('time_only')
            )
            .where(
                UserLog.created_at >= start_date,  # диапазон дат эффективнее работает
                UserLog.created_at <= end_date
            )
            .order_by(UserLog.user_id, UserLog.created_at.desc())
        )

        result = await self.session.execute(stmt)
        rows = result.all()

        user_logs: dict[uuid.UUID, list[tuple[str, str]]] = defaultdict(list)
        for user_id, log_text, time_str in rows:
            if len(user_logs[user_id]) < max_logs_per_user:
                user_logs[user_id].append((log_text, time_str))

        return dict(user_logs)

    async def create_log(self, user_id: uuid.UUID, log_text: str) -> None:
        """Сохраняет лог юзера"""
        stmt = """
            INSERT INTO user_logs (id, user_id, log)
            VALUES (:id, :user_id, :log)
        """

        params = {
            "id": uuid.uuid4(),
            "user_id": user_id,
            "log": log_text,
        }

        try:
            await self.session.execute(text(stmt), params)
            await self.session.commit()
            logger.info(f"Лог создан для пользователя {user_id}")
        except Exception as e:
            await self.session.rollback()
            logger.error(f"Ошибка создания лога: {e}")
            raise

    async def bulk_create_diary_records(self, records: list[tuple[uuid.UUID, str, str]]) -> int:
        """
        Массово создаёт записи в дневник (user_diary).

        Args:
            records: список кортежей (user_id: UUID, text: str)

        Returns:
            int: количество успешно вставленных записей
        """
        if not records:
            logger.info("Нет записей для массового создания в дневник")
            return 0

        data = [
            {
                "id": str(uuid.uuid4()),
                "user_id": str(user_id),
                "text": text_content,
                "created_at": datetime.date.today(),
                "context_text": context_text
            }
            for user_id, text_content, context_text in records
        ]

        stmt = text("""
            INSERT INTO user_diary (id, user_id, created_at, text, context_text)
            VALUES (:id, :user_id, :created_at, :text, :context_text)
            ON CONFLICT (user_id, created_at) DO NOTHING
        """)

        try:
            # Важно: execute со списком словарей → SQLAlchemy сам сделает executemany
            result = await self.session.execute(stmt, data)
            await self.session.commit()
            count = result.rowcount
            logger.info(f"Вставлено {count} записей")
            return count
        except Exception as e:
            await self.session.rollback()
            logger.error("Bulk insert failed", exc_info=True)
            raise

    async def change_talking_mode(
            self,
            user_id: uuid.UUID,
            mode: TALKING_MODES
    ) -> None:
        stmt = (
            update(User)
            .where(User.id == user_id)
            .values(talk_mode=mode.value)
            .returning(User.id)
        )

        try:
            await self.session.execute(stmt)

            await self.session.commit()
            logger.info(f"Режим общения пользователя {user_id} изменён на {mode.value}")

        except Exception as e:
            await self.session.rollback()
            logger.error(f"Ошибка при смене talk_mode для пользователя {user_id}: {e}", exc_info=True)
            raise

    def __del__(self):
        logger.info("USER REPO IS COLLECTED BY GARBAGE COLLECTOR")
