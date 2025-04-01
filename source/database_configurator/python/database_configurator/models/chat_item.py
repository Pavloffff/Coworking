from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, ForeignKey

from database_configurator.models.base_model import BaseModel
from database_configurator.models.user import User
from database_configurator.models.text_channel import TextChannel

class ChatItem(BaseModel):
    __tablename__ = 'chatitem'
    chat_item_id: Mapped[int] = mapped_column('chat_item_id', BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.user_id))
    text_channel_id: Mapped[int] = mapped_column(ForeignKey(TextChannel.text_channel_id))
    text: Mapped[str]
    file_url: Mapped[str]
