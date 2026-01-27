import logging
import uuid

from sqlalchemy import select
from sqlalchemy.dialects.postgresql import insert
from sqlalchemy.ext.asyncio import AsyncSession
from sqlalchemy.orm import selectinload

from src.core.schemas.user_schemas import UserSchema, UserTelegramDataSchema
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
        """Возвращает модель юзер со всеми смежными таблицами"""
        stmt = (
            select(User).where(
                User.id == user_id
            )
            .options(
                # core traits
                selectinload(User.social_profile),
                selectinload(User.cognitive_profile),
                selectinload(User.emotional_profile),
                selectinload(User.behavioral_profile),

                # Юмор, тёмная триада
                selectinload(User.humor_profile),
                selectinload(User.dark_triads),

                # HEXACO, Соционика, Holland
                selectinload(User.hexaco),
                selectinload(User.socionics),
                selectinload(User.holland_codes),

                # Клинические / патологические профили
                selectinload(User.personality_disorders),
                selectinload(User.anxiety_disorders),
                selectinload(User.mood_disorders),
                selectinload(User.clinical_profile),
                selectinload(User.neuro_disorders),

                # Отношения / любовь / сексуальность
                # selectinload(User.relationship_preference),
                # selectinload(User.love_language),
                # selectinload(User.sexual_preference)
            )
        )
        result = await self.session.execute(stmt)
        user: User | None = result.scalar_one_or_none()
        if not user:
            return None

        return user.get_schema()

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

    def __del__(self):
        logger.info("USER REPO IS COLLECTED BY GARBAGE COLLECTOR")
