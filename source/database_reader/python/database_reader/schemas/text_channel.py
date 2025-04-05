from pydantic import BaseModel


class TextChannel(BaseModel):
    text_channel_id: int
    name: str
    server_id: int
