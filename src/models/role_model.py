from sqlalchemy import String, Text
from sqlalchemy.orm import Mapped, mapped_column
from src.models.base_model import Base 
from src.models.role_model import Role

class Role(Base):
    name: Mapped[str] = mapped_column(String(50), unique=True)
    description: Mapped[str] = mapped_column(Text, default="")

