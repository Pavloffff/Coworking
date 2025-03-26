import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from servers_configurator.api import api_router
from servers_configurator.logger import _logger
from servers_configurator.config import _config
from servers_configurator.kafka_utils import Writer, KafkaSettings

class ServersConfigurator:
    def __init__(self):
        self._app = FastAPI(
            title=_config.SERVICE_NAME,
            openapi_url=f'{_config.API_V1_STR}/openapi.json'
        )
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self._app.include_router(api_router, prefix=_config.API_V1_STR)
        self._app.add_event_handler('startup', self._startup_handler(self._app))
    
    @staticmethod
    def _startup_handler(app: FastAPI):
        def startup() -> None:
            _logger.info("Running startup handler.")
            ServersConfigurator._startup(app)
        return startup

    @staticmethod
    def _startup(app: FastAPI):
        kafka_writer = Writer(
            KafkaSettings(
                host=_config.KAFKA_HOST,
                port=_config.KAFKA_PORT,
                topic='coworking_database_topic',
                initial_timeout=10,
                retry_timeout=10
            )
        )
        app.state.writer = kafka_writer

    def run(self):
        uvicorn.run(self._app, host=_config.HOST, port=_config.PORT)
