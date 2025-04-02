import uvicorn

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from servers_configurator.api import api_router
from servers_configurator.logger import _logger
from servers_configurator.config import Config
from servers_configurator.kafka_utils import Writer


class ServersConfigurator:
    def __init__(self):
        self._config: Config = Config.load()
        self._app = FastAPI(
            title=self._config.servers_configurator_config.service_name,
            openapi_url=f'{self._config.servers_configurator_config.api_v1_str}/openapi.json'
        )
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self._app.include_router(api_router, prefix=self._config.servers_configurator_config.api_v1_str)
        self._app.add_event_handler('startup', self._startup_handler())
    
    def _startup_handler(self):
        def startup() -> None:
            _logger.info("Running startup handler.")
            self._startup()
        return startup

    def _startup(self):
        kafka_writer = Writer(
            self._config.kafka_config
        )
        self._app.state.writer = kafka_writer

    def run(self):
        uvicorn.run(
            self._app, 
            host=self._config.servers_configurator_config.host, 
            port=self._config.servers_configurator_config.port
        )
