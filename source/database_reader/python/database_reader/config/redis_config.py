from dataclasses import dataclass


@dataclass
class RedisConfig:
    host: str
    port: str
    db: str
    password: str

    @property
    def url(self):
        return f'redis://:{self.password}@{self.host}:{self.port}/{self.db}'
