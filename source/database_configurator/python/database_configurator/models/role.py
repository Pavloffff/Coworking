from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, ForeignKey

from database_configurator.models.base_model import BaseModel
from database_configurator.models.server import Server


class Role(BaseModel):
    __tablename__ = 'role'
    role_id: Mapped[int] = mapped_column('role_id', BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    server_id: Mapped[int] = mapped_column(ForeignKey(Server.server_id))
