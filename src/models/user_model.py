from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.role_model import Role
from src.models.base_model import Base 

class User(Base):
    """Модель пользователя"""
    __doc__ = "Пользователь приложения."
    
    login: Mapped[str] = mapped_column(String(256), unique=True)
    password: Mapped[str] = mapped_column(String(256))
    email: Mapped[Optional[str]] = mapped_column(String(256), nullable=True, unique=True)
    phone: Mapped[Optional[str]] = mapped_column(String(16), nullable=True, unique=True)
    role_id: Mapped[int] = mapped_column(ForeignKey('roles.id'))
    role: Mapped["Role"] = relationship()