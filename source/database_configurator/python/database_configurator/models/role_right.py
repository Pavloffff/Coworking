from sqlalchemy.orm import Mapped, mapped_column
from sqlalchemy import BigInteger, ForeignKey

from database_configurator.models.base_model import BaseModel
from database_configurator.models.right import Right
from database_configurator.models.role import Role

class RoleRight(BaseModel):
    __tablename__ = 'roleright'
    role_right_id: Mapped[int] = mapped_column('role_right_id', BigInteger, primary_key=True)
    right_id: Mapped[int] = mapped_column(ForeignKey(Right.right_id))
    role_id: Mapped[int] = mapped_column(ForeignKey(Role.role_id))
