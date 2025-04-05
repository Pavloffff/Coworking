from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, ForeignKey

from database_reader.models.base_model import BaseModel
from database_reader.models.server import Server


class TextChannel(BaseModel):
    __tablename__ = 'textchannel'
    text_channel_id: Mapped[int] = mapped_column('text_channel_id', BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    server_id: Mapped[int] = mapped_column(ForeignKey(Server.server_id))
