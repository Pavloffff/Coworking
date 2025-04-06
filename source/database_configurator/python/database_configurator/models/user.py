from sqlalchemy.orm import Mapped, mapped_column

from sqlalchemy import BigInteger
from database_configurator.models.base_model import BaseModel


class User(BaseModel):
    __tablename__ = 'user'
    user_id: Mapped[int] = mapped_column('user_id', BigInteger, primary_key=True)
    name: Mapped[str] = mapped_column(nullable=False)
    email: Mapped[str] = mapped_column('email', unique=True)
    tag: Mapped[int] = mapped_column('tag', BigInteger, unique=True)
    password_hash: Mapped[str] = mapped_column(nullable=False)
    password_salt: Mapped[str] = mapped_column(nullable=False)
    avatar_url: Mapped[str] = mapped_column(nullable=False)
