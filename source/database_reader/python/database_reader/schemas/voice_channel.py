from pydantic import BaseModel


class VoiceChannel(BaseModel):
    voice_channel_id: int
    name: str
    server_id: int
