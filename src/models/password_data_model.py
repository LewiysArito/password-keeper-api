from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base_model import Base

class PasswordData(Base):
    """Модель для логинов и паролей пользователя"""
    
    __doc__ = "Данные логини и пароля пользователя"
    name = mapped_column(String(256))
    login =  Mapped[str] = mapped_column(String(256))
    secret = Mapped[str] = mapped_column(String(256))
    descrtiption = [Mapped[str]] = mapped_column(String(256))