from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, ForeignKey

from database_reader.models.base_model import BaseModel
from database_reader.models.user import User
from database_reader.models.voice_channel import VoiceChannel

class VoiceItem(BaseModel):
    __tablename__ = 'voiceitem'
    voice_item_id: Mapped[int] = mapped_column('voice_item_id', BigInteger, primary_key=True)
    voice_channel_id: Mapped[int] = mapped_column(ForeignKey(VoiceChannel.voice_channel_id))
    user_id: Mapped[int] = mapped_column(ForeignKey(User.user_id))
