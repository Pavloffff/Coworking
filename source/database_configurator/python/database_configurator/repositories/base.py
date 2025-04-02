from abc import ABC, abstractmethod
from sqlalchemy.ext.asyncio import AsyncSession


class BaseRepository(ABC):
    @staticmethod
    @abstractmethod
    async def insert(session: AsyncSession, data: dict):
        pass
    
    @staticmethod
    @abstractmethod
    async def update(session: AsyncSession, data: dict):
        pass
    
    @staticmethod
    @abstractmethod
    async def delete(session: AsyncSession, data: dict):
        pass
