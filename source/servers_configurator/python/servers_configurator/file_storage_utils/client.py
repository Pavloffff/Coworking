import io
import uuid
from minio import Minio

from servers_configurator.config.file_storage_config import FileStorageConfig
from servers_configurator.logger import _logger

class Client:
    def __init__(self, config: FileStorageConfig):
        self._client = Minio(
            config.url,
            access_key=config.access_key,
            secret_key=config.secret_key,
            secure=False
        )
        self._bucket_name = config.bucket_name
        if self._client.bucket_exists(config.bucket_name):
            _logger.error(f"{config.bucket_name} exists")
        else:
            _logger.error(f"{config.bucket_name} does not exist. creating...")
            self._bucket = self._client.make_bucket(
                self._bucket_name
            )

    def insert(self, file_name: str, data: bytes) -> str:
        name, extension = file_name.split('.')
        result = self._client.put_object(
            bucket_name=self._bucket_name,
            object_name=f'{name}_{uuid.uuid4()}.{extension}',
            data=io.BytesIO(data),
            length=-1,
            part_size=10*1024*1024
        )
        return result.object_name
    
    def get(self, object_name: str) -> bytes:
        try:
            response = self._client.get_object(
                self._bucket_name,
                object_name
            )
            return response.data
        finally:
            response.close()
            response.release_conn()
    
    def delete(self, object_name: str) -> None:
        self._client.remove_object(
            self._bucket_name,
            object_name
        )
