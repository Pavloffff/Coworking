from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import BigInteger
from database_reader.models.base_model import BaseModel


class Server(BaseModel):
    __tablename__ = 'server'
    server_id: Mapped[int] = mapped_column('server_id', BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    owner_id: Mapped[int] = mapped_column('owner_id', BigInteger, nullable=False)
