from datetime import datetime
from typing import Optional

from sqlalchemy import ForeignKey, String, Integer
from sqlalchemy.orm import Mapped, mapped_column, relationship
from src.models.base_model import Base

class DataGroup(Base):
    """Группа паролей"""
    __doc__ = "Группа паролей."
    name = Mapped[str] = mapped_column(String(256), nullable=False)

    