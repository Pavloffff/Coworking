from pydantic import BaseModel

from servers_configurator.schemas.server import Server


class TextChannel(BaseModel):
    text_channel_id: int
    name: str
    server_id: int
