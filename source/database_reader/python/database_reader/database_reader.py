import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from database_reader.api import api_router
from database_reader.logger import _logger
from database_reader.config import Config
from database_reader.file_storage_utils import FileStorageClient
from database_reader.database_session import DatabaseSession
from database_reader.redis_utils import RedisClient

class DatabaseReader:
    def __init__(self):
        self._config: Config = Config.load()
        self._app = FastAPI(
            title=self._config.database_reader_config.service_name,
            openapi_url=f'{self._config.database_reader_config.api_v1_str}/openapi.json'
        )
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self._app.include_router(api_router, prefix=self._config.database_reader_config.api_v1_str)
        self._app.add_event_handler('startup', self._startup_handler())
    
    def _startup_handler(self):
        def startup() -> None:
            _logger.info("Running startup handler.")
            self._startup()
        return startup

    def _startup(self):
        self._app.state.config = self._config
        file_storage_client = FileStorageClient(
            config=self._config.file_storage_config
        )
        self._app.state.file_storage_client = file_storage_client
        database_session = DatabaseSession(
            config=self._config.database_config
        )
        self._app.state.database_session = database_session
        redis_client = RedisClient()
        self._app.state.redis_client = redis_client

    def run(self):
        uvicorn.run(
            self._app, 
            host=self._config.database_reader_config.host, 
            port=self._config.database_reader_config.port
        )
