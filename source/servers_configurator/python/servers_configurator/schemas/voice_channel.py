from pydantic import BaseModel

from servers_configurator.schemas.server import Server


class VoiceChannel(BaseModel):
    voice_channel_id: int
    name: str
    server_id: int
