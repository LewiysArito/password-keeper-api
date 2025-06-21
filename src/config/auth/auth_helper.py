import jwt
from typing import Any, Dict
from src.config.auth.auth_config import settings_auth_jwt
from datetime import datetime, timezone, timedelta
from src.constants.token_type_constants import TokenType

class AuthJWTHelper:
    def __init__(self,
        private_key: bytes = settings_auth_jwt.PRIVATE_KEY,
        public_key: bytes = settings_auth_jwt.PUBLIC_KEY,
        algorithm : str = settings_auth_jwt.ALGORITHM,
        access_token_lifetime: int = settings_auth_jwt.ACCESS_TOKEN_LIFETIME,
        refresh_token_lifetime: int = settings_auth_jwt.REFRESH_TOKEN_LIFETIME,
        refresh_token_rotate_min_lifetime: int = settings_auth_jwt.REFRESH_TOKEN_ROTATE_MIN_LIFETIME
    ): 
        self._private_key = private_key
        self._public_key = public_key
        self._algorithm = algorithm
        self._access_token_lifetime = access_token_lifetime
        self._refresh_token_lifetime = refresh_token_lifetime
        self._refresh_token_rotate_min_lifetime = refresh_token_rotate_min_lifetime

    def encode_token(self, payload: Dict[str, Any], token_lifetime: int) -> str:
        """
        Функция для создание токена
        """
        to_encode = payload.copy()
        now = datetime.now(timezone.utc)
        expire = now + timedelta(minutes=token_lifetime)
        to_encode.update(
            exp=expire,
            iat=now
        )

        return jwt.encode(
            payload = to_encode,
            key = self._private_key,
            algorithm=self._algorithm
        )
    
    def create_access_token(self, sub: str | int, username: str):
        """
        Функции для создания токена доступа
        :param sub: идентификатор пользователя
        :param username: имя пользователя 
        """
        jwt_payload = {
            "sub": str(sub),
            "username": username,
            "type": TokenType.ACCESS_TOKEN_TYPE.value
        }
        return self.encode_token(jwt_payload, token_lifetime=self._access_token_lifetime)

    def create_refrash_token(self, sub: str | int):
        """
        Cоздает refrash токена
        :param: идентификатор пользователя
        """
        jwt_payload = {
            "sub": str(sub),
            "type": TokenType.REFRASH_TOKEN_TYPE.value
        }
        return self.encode_token(jwt_payload, token_lifetime=self._refresh_token_lifetime)
    
    def decode_token(self, token: bytes | str)->Dict[str, Any]:
        """
        Функция для проверки токена доступа
        """
        try:
            return jwt.decode(
                jwt = token,
                key = self._public_key,
                algorithms=[self._algorithm]
            )
        except jwt.ExpiredSignatureError:
            raise jwt.PyJWTError("Token expired")
        except jwt.InvalidTokenError:
            raise jwt.PyJWTError("Token is bad")
    
jwt_helper = AuthJWTHelper(
    private_key = settings_auth_jwt.PRIVATE_KEY,
    public_key = settings_auth_jwt.PUBLIC_KEY,
    algorithm = settings_auth_jwt.ALGORITHM,
    access_token_lifetime = settings_auth_jwt.ACCESS_TOKEN_LIFETIME,
    refresh_token_lifetime = settings_auth_jwt.REFRESH_TOKEN_LIFETIME,
    refresh_token_rotate_min_lifetime = settings_auth_jwt.REFRESH_TOKEN_ROTATE_MIN_LIFETIME
)