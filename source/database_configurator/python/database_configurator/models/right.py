from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import BigInteger
from database_configurator.models.base_model import BaseModel


class Right(BaseModel):
    __tablename__ = 'right'
    right_id: Mapped[int] = mapped_column('right_id', BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
