from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, ForeignKey

from database_reader.models.base_model import BaseModel
from database_reader.models.user import User
from database_reader.models.role import Role


class UserRole(BaseModel):
    __tablename__ = 'userrole'
    user_role_id: Mapped[int] = mapped_column('user_role_id', BigInteger, primary_key=True)
    user_id: Mapped[int] = mapped_column(ForeignKey(User.user_id))
    role_id: Mapped[int] = mapped_column(ForeignKey(Role.role_id))
