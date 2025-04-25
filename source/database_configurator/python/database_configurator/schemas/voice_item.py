from typing import Optional
from pydantic import BaseModel


class VoiceItem(BaseModel):
    voice_item_id: int
    user_id: int
    voice_channel_id: int
    server_id: int
