from typing import Optional
from pydantic import BaseModel

from notifications_pusher.schemas.user import User


class ChatItem(BaseModel):
    chat_item_id: int
    user_id: int
    text_channel_id: int
    text: Optional[str]
    file_url: Optional[str]
