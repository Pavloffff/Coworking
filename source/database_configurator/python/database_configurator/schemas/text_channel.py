from pydantic import BaseModel

from database_configurator.schemas.server import Server


class TextChannel(BaseModel):
    text_channel_id: int
    name: str
    server: Server
