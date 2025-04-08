import json
from redis.asyncio.client import Redis

from database_reader.config.redis_config import RedisConfig


class RedisClient:
    def __init__(self, config: RedisConfig):
        self._storage = Redis(
            host=config.host,
            port=config.port,
            password=config.password,
            db=config.db
        )

    async def put(self, key: str, value: dict):
        value_json = json.dumps(value)
        await self._storage.set(key, value_json)
    
    async def get(self, key: str) -> dict:
        data = await self._storage.get(key)
        return json.loads(data)
    
    async def delete(self, key):
        await self._storage.delete(key)
