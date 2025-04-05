from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import BigInteger
from database_reader.models.base_model import BaseModel


class ActivityType(BaseModel):
    __tablename__ = 'activitytype'
    activity_type_id: Mapped[int] = mapped_column('activity_type_id', BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
