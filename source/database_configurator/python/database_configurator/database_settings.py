from dataclasses import dataclass
from sqlalchemy.engine import URL

#TODO: все конфиги переделать
@dataclass
class DatabaseSettings:
    host: str
    port: str
    user: str
    password: str
    database: str
    query_cache_size: int = 1200
    pool_size: int = 10
    max_overflow: int = 200
    future: bool = True
    echo: bool = False
    driver: str = 'postgresql+asyncpg'
    
    @property
    def url(self) -> URL:
        return URL.create(
            drivername=self.driver,
            host=self.host,
            port=self.port,
            username=self.user,
            password=self.password,
            database=self.database
        )
