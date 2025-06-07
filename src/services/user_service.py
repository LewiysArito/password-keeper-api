from src.schemas.user_schemas import UserCreate, UserUpdate
from src.services.base_service import BaseService
from src.repositories.user_repository import UserRepository, user_repository
from src.models.user_model import UserTable as UserModel

class UserService(BaseService[UserModel, UserCreate, UserUpdate]):
    @property
    def user_repository(self) -> UserRepository:
        return self.repository
    
    async def exists(self, login: str) -> bool:
        """
        Проверка, что существует пользователь с указанным логином 
        :param: login: логин пользователя
        """
        return await self.user_repository.exists(login=login)
    
    async def all(self) -> list[UserModel] | None:
        """ 
        Получение всех пользователей, которые есть в системе
        :param: login: логин пользователя
        """
        return await self.user_repository.all()


user_service = UserService(repository=user_repository)