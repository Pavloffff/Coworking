from dataclasses import dataclass


@dataclass
class DatabaseConfig:
    driver: str
    user: str
    password: str
    host: str
    port: str
    database: str

    @property
    def url(self):
        return f'{self.driver}://{self.user}:{self.password}@{self.host}:{self.port}/{self.database}'
