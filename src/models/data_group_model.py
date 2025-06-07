from datetime import datetime
from typing import TYPE_CHECKING, List, Optional

from sqlalchemy import String
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base_model import Base

if TYPE_CHECKING:
    from src.models.password_data_model import PasswordData
    from src.models.secret_data_model import SecretData
    from src.models.user_group_permissions_model import UserGroupPermission

class DataGroup(Base):
    """Группа паролей"""
    __doc__ = "Группа паролей."
    name: Mapped[str] = mapped_column(String(256), nullable=False)
    
    secrets: Mapped[List["SecretData"]] =  relationship("SecretData", back_populates="group")
    passwords: Mapped[List["PasswordData"]] = relationship("PasswordData", back_populates="group")
    
    permissions: Mapped[List["UserGroupPermission"]] = relationship("UserGroupPermission", back_populates="group")