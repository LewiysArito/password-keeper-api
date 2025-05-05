from typing import List, Optional

from sqlalchemy import Boolean, ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base_model import Base 
from src.models.user_group_permissions_model import UserGroupPermission

class User(Base):
    """Модель пользователя"""
    __doc__ = "Пользователь приложения."
    
    login: Mapped[str] = mapped_column(String(256), unique=True)
    password: Mapped[str] = mapped_column(String(256))
    email: Mapped[Optional[str]] = mapped_column(String(256), nullable=True, unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(16), nullable=True, unique=True)
    is_active: Mapped[bool] = mapped_column(Boolean, default=True, comment="Пользователь может пользоваться системой")

    permissions: Mapped[List["UserGroupPermission"]] = relationship("UserGroupPermission", back_populates="user")