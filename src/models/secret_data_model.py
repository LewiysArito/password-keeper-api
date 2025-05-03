from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base_model import Base

class SecretData(Base):
    """Модель для чувствительных данных пользователя"""
    
    __doc__ = "Секретные данные пользователя"
    name = mapped_column(String(256))
    alias =  Mapped[str] = mapped_column(String(256))
    secret = Mapped[str] = mapped_column(String(256))
    descrtiption = [Mapped[str]] = mapped_column(String(256))