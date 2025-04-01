from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from database_configurator.database_settings import DatabaseSettings


class DatabaseSession:
    def __init__(self, settings: DatabaseSettings):
        self._engine = create_async_engine(
            settings.url,
            query_cache_size=settings.query_cache_size,
            pool_size=settings.pool_size,
            max_overflow=settings.max_overflow,
            future=settings.future,
            echo=settings.echo,
        )
        
    async def create(self):
        async with self._engine.begin() as conn:
            from database_configurator.models.base_model import BaseModel
            await conn.run_sync(BaseModel.metadata.create_all)

        return sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            class_=AsyncSession
        )
