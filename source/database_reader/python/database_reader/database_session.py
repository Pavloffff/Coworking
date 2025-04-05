from sqlalchemy.ext.asyncio import create_async_engine, AsyncSession
from sqlalchemy.orm import sessionmaker

from database_reader.config.database_config import DatabaseConfig


class DatabaseSession:
    def __init__(self, config: DatabaseConfig):
        self._engine = create_async_engine(
            config.url,
            query_cache_size=config.query_cache_size,
            pool_size=config.pool_size,
            max_overflow=config.max_overflow,
            future=config.future,
            echo=config.echo,
        )
        
    async def create(self):
        async with self._engine.begin() as conn:
            from database_reader.models.base_model import BaseModel
            await conn.run_sync(BaseModel.metadata.create_all)

        return sessionmaker(
            bind=self._engine,
            expire_on_commit=False,
            class_=AsyncSession
        )
