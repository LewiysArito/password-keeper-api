from abc import ABC
from typing import NewType
from src.models.user_model import User

class AbstractPermission(ABC):
    def __call__(self, *args, **kwargs):
        raise NotImplementedError

    def check_permissions(self, user: User) -> User:
        raise NotImplementedError
