from typing import Optional
from pydantic import BaseModel

from servers_configurator.schemas.user import User


class ChatItem(BaseModel):
    chat_item_id: int
    user: User
    text_channel_id: int
    text: Optional[str]
    file_url: Optional[str]
