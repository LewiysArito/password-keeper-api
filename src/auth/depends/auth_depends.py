from typing import Annotated, Any, Dict
from fastapi import Depends, HTTPException
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWTError
from src.config.auth.auth_helper import jwt_helper

security = HTTPBearer()
def get_current_user(token: Annotated[HTTPAuthorizationCredentials, Depends(security)])->Dict[str, Any]:
    """
    Проверить авторизован ли текущей пользователь или же нет
    """
    try:
        payload = jwt_helper.decode(token.credentials)
        return payload
    except PyJWTError as e:
        raise HTTPException(status_code=401, detail="Problem with JWT-Token")