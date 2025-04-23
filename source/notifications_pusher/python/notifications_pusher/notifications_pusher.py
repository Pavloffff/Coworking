import json
import asyncio

from uvicorn import Config as UvicornConfig, Server
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from notifications_pusher.api import api_router
from notifications_pusher.api.routes.notifications import manager as ws_manager
from notifications_pusher.config import Config
from notifications_pusher.kafka_utils import Reader
from notifications_pusher.logger import _logger
from notifications_pusher.waiter.waiter_strategy import WaiterStrategy
from notifications_pusher.redis_utils.client import RedisClient
from notifications_pusher.api.utils.token_processor import TokenProcessor
from notifications_pusher.getters.user_getter import UserGetter
from notifications_pusher.database_reader_utils.client import DatabaseReaderClient


class NotificationsPusher:
    def __init__(self):
        self._config = Config.load()
        self._app = FastAPI(
            title=self._config.notifications_pusher_config.service_name,
            openapi_url=f'{self._config.notifications_pusher_config.api_v1_str}/openapi.json'
        )
        self._app.add_middleware(
            CORSMiddleware,
            allow_origins=["*"],
            allow_credentials=True,
            allow_methods=["*"],
            allow_headers=["*"],
        )
        self._app.include_router(api_router, prefix=self._config.notifications_pusher_config.api_v1_str)
        self._app.add_event_handler('startup', self._startup_handler())
        self._kafka_reader = Reader(
            config=self._config.kafka_config
        )
        self._database_reader_client = DatabaseReaderClient(
            self._config.database_reader_config
        )
        self._waiter_strategy = WaiterStrategy(
            client=self._database_reader_client
        )
    
    async def run(self):
        server = Server(
            UvicornConfig(
                app=self._app,
                host=self._config.notifications_pusher_config.host,
                port=self._config.notifications_pusher_config.port,
                loop=asyncio.get_event_loop()
            )
        )

        server_task = asyncio.create_task(server.serve())
        kafka_task = asyncio.create_task(self._listen_kafka())
        
        try:
            await asyncio.gather(server_task, kafka_task)
        finally:
            await server.shutdown()
            server_task.cancel()
            kafka_task.cancel()
    
    def _startup_handler(self):
        def startup() -> None:
            _logger.info("Running startup handler.")
            self._startup()
        return startup
    
    def _startup(self):
        self._app.state.config = self._config
        redis_client = RedisClient(
            config=self._config.redis_config
        )
        self._app.state.redis_client = redis_client
    
    async def _listen_kafka(self):
        async for message in self._kafka_reader.listen():
            try:
                _logger.debug(f"Received message: {message}")
                await self._process_message(message)
            except Exception as ex:
                _logger.exception(f"Error processing message: {ex.with_traceback()}")

    async def _process_message(self, message: dict):
        model = message['model']
        method = message['method']
        data = message['data']
        access_token = message.get('access_token')
        
        response_list = await self._waiter_strategy.wait(model, method, data, access_token)
        if response_list is not None:
            for response_data in response_list:
                users_to_notify = await UserGetter.get(
                    self._database_reader_client, response_data, model, access_token
                )
                for user in users_to_notify:
                    await ws_manager.send_to_user(
                        message=json.dumps(message),
                        current_user=user['email'],
                        storage=self._app.state.redis_client,
                    )
