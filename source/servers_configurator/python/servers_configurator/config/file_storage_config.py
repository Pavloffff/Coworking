from dataclasses import dataclass


@dataclass
class FileStorageConfig:
    host: str
    port: str
    access_key: str
    secret_key: str
    bucket_name: str

    @property
    def url(self):
        return f'{self.host}:{self.port}'
