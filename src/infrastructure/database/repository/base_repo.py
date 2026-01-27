import asyncio
from functools import wraps
from typing import Generic, Type, Optional, Sequence, Callable, Any
from uuid import UUID

from sqlalchemy import update, delete, select
from sqlalchemy.ext.asyncio import AsyncSession

from infrastructure.database.models.base import M, S


def check_model_initialized(method: Callable) -> Callable:
    """Декоратор для проверки инициализации модели перед выполнением метода."""

    @wraps(method)
    async def async_wrapper(self: "BaseRepository", *args: Any, **kwargs: Any) -> Any:
        if self.model is None:
            raise ValueError("Модель не установлена")
        return await method(self, *args, **kwargs)

    @wraps(method)
    def sync_wrapper(self: "BaseRepository", *args: Any, **kwargs: Any) -> Any:
        if self.model is None:
            raise ValueError("Модель не установлена")
        return method(self, *args, **kwargs)

    # Возвращаем соответствующую обертку в зависимости от типа метода
    if asyncio.iscoroutinefunction(method):
        return async_wrapper
    return sync_wrapper


class BaseRepository(Generic[M]):
    def __init__(
            self,
            model: Type[M] | None,
            session: AsyncSession,
    ):
        self.model = model
        self.session = session

    @check_model_initialized
    async def save(self, model: M) -> S:
        """Saves all changes and refresh model."""
        self.session.add(model)
        await self.session.commit()
        await self.session.refresh(model)
        return model.get_schema()

    @check_model_initialized
    async def save_from_schema(self, schema: S) -> S:
        """Saves all changes and refresh model."""
        model: M = self.model.from_pydantic(schema)
        return await self.save(model)

    @check_model_initialized
    async def get(self, id: UUID) -> Optional[S]:
        """Get schema by primary key ID."""
        model: M = await self.session.get(self.model, id)
        return model.get_schema()

    @check_model_initialized
    async def get_model(self, id: UUID) -> Optional[M]:
        """Get model by primary key ID."""
        model: M = await self.session.get(self.model, id)
        return model

    @check_model_initialized
    async def get_all(self) -> Sequence[S]:
        """Returns all models"""
        result = await self.session.execute(select(self.model))
        models = result.scalars().all()
        return [model.get_schema() for model in models]

    @check_model_initialized
    async def create(self, model: M) -> S:
        """Create new model by instance."""
        try:
            self.session.add(model)
            await self.session.commit()
            await self.session.refresh(model)  # refresh from db (generated ID for example)
            return model.get_schema()
        except:
            await self.session.rollback()
            raise

    @check_model_initialized
    async def update(self, id: UUID, **values) -> Optional[S]:
        """
        Refresh model if exist on DB, or returns None.
        """
        stmt = (
            update(self.model)
            .where(self.model.id == id)
            .values(**values)
            .returning(self.model)
        )
        result = await self.session.execute(stmt)
        await self.session.commit()
        model: M = result.scalar_one_or_none()
        if model:
            return model.get_schema()
        return None

    @check_model_initialized
    async def delete(self, id: UUID) -> bool:
        """Delete model by ID. Returns True if deleted, False if not found."""
        result = await self.session.execute(
            delete(self.model).where(self.model.id == id)
        )
        await self.session.commit()
        return result.rowcount > 0
