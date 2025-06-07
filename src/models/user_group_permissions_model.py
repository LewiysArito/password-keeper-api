from typing import TYPE_CHECKING
from sqlalchemy import CheckConstraint, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.constants.db_constants import Roles
from src.models.base_model import Base

if TYPE_CHECKING:
    from src.models.data_group_model import DataGroup
    from src.models.user_model import UserTable

class UserGroupPermission(Base):
    __doc__ =  "Пользовательский доступ к группам"

    __table_args__ = (
        CheckConstraint(
            f"role IN({', '.join(map(repr, Roles.names()))})",
            name="valid_roles"
        ),
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("user_table.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("data_group.id"))
    role: Mapped[str] = mapped_column(String(200))

    user: Mapped["UserTable"] = relationship("UserTable", back_populates="permissions")
    group: Mapped["DataGroup"] = relationship("DataGroup", back_populates="permissions")
