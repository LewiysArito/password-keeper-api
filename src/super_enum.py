from enum import Enum
class SuperEnum(Enum):
    @classmethod
    def values(cls):
        """Возвращает список значений Enum"""
        return [member.value for member in cls]

    @classmethod
    def names(cls):
        """Возвращает список имен (ключей) Enum"""
        return [member.name for member in cls]

    def __str__(self):
        """Возвращает строковое представление значения"""
        return str(self.value)