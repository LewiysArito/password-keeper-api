from fastapi import HTTPException 
from src.auth.schemas.token_schemas import TokenInfo
from src.config.auth.auth_helper import jwt_helper
from src.models.user_model import UserTable as UserModel
from src.repositories.user_repository import UserRepository, user_repository
from src.schemas.user_schemas import UserCreate, UserLogin, UserUpdate
from src.services.base_service import BaseService
from src.utils.password_utils import PasswordUtils

from starlette.status import (
    HTTP_409_CONFLICT
)
class AuthService(BaseService[UserModel, UserCreate, UserUpdate]):
    
    @property
    def _user_repository(self) -> UserRepository:
        return self.repository
    
    async def register(self, model: UserCreate)->UserModel:
        """
        Регистрирует нового пользователя
        """
        user_exists = await self._user_repository.exists(login=model.login)
        if user_exists:
            raise HTTPException(HTTP_409_CONFLICT, "A user with the specified login is already registered")
        
        user_exists = model.email and await self._user_repository.exists(email=model.email)
        if user_exists:
            raise ValueError(HTTP_409_CONFLICT, "A user with the specified email is already registered")

        user_exists = model.phone and await self._user_repository.exists(phone=model.phone)
        if user_exists:
            raise ValueError(HTTP_409_CONFLICT,"A user with the specified phone is already registered")

        hashed_password = PasswordUtils.hash_password(model.password)        

        model_with_hashed = model.model_copy(update={"password": hashed_password})
        
        return await user_repository.create(model_with_hashed)

    async def login_for_access_token(self, model: UserLogin)->TokenInfo:
        login_dict = {"login":model.login}
        user = await self._user_repository.get_one(**login_dict)

        if not user or not PasswordUtils.validate_password(model.password, user.password):
            raise HTTPException(status_code=401, detail="Incorrect login or password")
        
        jwt_payload = {
            "sub": str(user.id),
            "username": user.login
        }
        
        access_token = jwt_helper.encode(
            jwt_payload
        )

        return TokenInfo(
            access_token=access_token,
            token_type="Bearer"
        )
    

auth_service = AuthService(
    repository=user_repository
)

