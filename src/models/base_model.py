import re
from datetime import datetime
from typing import TypeVar
from sqlalchemy import TIMESTAMP, func
from sqlalchemy.orm import DeclarativeBase, Mapped, declared_attr, mapped_column

class Base(DeclarativeBase):
    __abstract__ = True

    id: Mapped[int] = mapped_column(primary_key=True)
    created_at: Mapped[datetime] = mapped_column(TIMESTAMP(timezone=True), default=func.now())
    updated_at: Mapped[datetime] = mapped_column(
        TIMESTAMP(timezone=True),
        default=func.now(),
        onupdate=func.now()
    )
    
    @declared_attr.directive
    def __tablename__(cls) -> str:
        """
        Переопределение магический метод, связанный с таблицей, формирование на основе имени класса 
        """

        words = re.findall(r"[A-Z][a-z]*", cls.__name__)
        return "_".join(list(map(lambda a: a.lower(), words)))

ModelType = TypeVar("ModelType", bound=Base)