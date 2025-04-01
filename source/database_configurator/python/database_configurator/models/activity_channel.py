from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, ForeignKey

from database_configurator.models.activity_type import ActivityType
from database_configurator.models.base_model import BaseModel
from database_configurator.models.server import Server


class ActivityChannel(BaseModel):
    __tablename__ = 'activitychannel'
    activity_channel_id: Mapped[int] = mapped_column('activity_channel_id', BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    server_id: Mapped[int] = mapped_column(ForeignKey(Server.server_id))
    activity_type_id: Mapped[int] = mapped_column(ForeignKey(ActivityType.activity_type_id))
