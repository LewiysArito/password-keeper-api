from sqlalchemy import CheckConstraint, Enum, ForeignKey, String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.src.models.data_group_model import DataGroup
from api.src.models.user_model import User
from src.models.base_model import Base
from src.constants.db_constants import Roles

class UserGroupPermission(Base):
    __doc__ =  "Пользовательский доступ к группам"

    __table_args__ = (
        CheckConstraint(
            f"role IN({', '.join(map(repr, Roles.names()))})",
            name="valid_roles"
        )
    )

    user_id: Mapped[int] = mapped_column(ForeignKey("user.id"))
    group_id: Mapped[int] = mapped_column(ForeignKey("data_group.id"))
    role: Mapped[str] = mapped_column(String(200)) 

    user: Mapped["User"] = relationship("User", back_populates="permissions")
    group: Mapped["DataGroup"] = relationship("DataGroup", back_populates="permissions")
