from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from api.src.models.data_group_model import DataGroup
from src.models.base_model import Base

class PasswordData(Base):
    """Модель для логинов и паролей пользователя"""
    
    __doc__ = "Данные логини и пароля пользователя"
    name:Mapped[str] = mapped_column(String(256))
    login:  Mapped[str] = mapped_column(String(256))
    password: Mapped[str] = mapped_column(String(256))
    description : Mapped[str] = mapped_column(String(256), nullable=True)

    group_id: Mapped[Optional[int]] = mapped_column(Integer, ForeignKey("data_group.id"), nullable=True)

    group: Mapped["DataGroup"] = relationship("DataGroup", back_populates="passwords")