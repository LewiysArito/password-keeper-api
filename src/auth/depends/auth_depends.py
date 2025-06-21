from typing import Annotated, Any, Dict
from fastapi import Cookie, Depends, HTTPException, Response
from fastapi.security import HTTPAuthorizationCredentials, HTTPBearer
from jwt import PyJWTError
from src.config.auth.auth_helper import jwt_helper

security = HTTPBearer()
def get_current_user(token: Annotated[HTTPAuthorizationCredentials, Depends(security)])->Dict[str, Any]:
    """
    Проверить авторизован ли текущей пользователь или же нет
    """
    try:
        payload = jwt_helper.decode_token(token.credentials)
        return payload
    except PyJWTError as e:
        raise HTTPException(status_code=401, detail="Problem with JWT-Token")

def get_refresh_token_from_cookies(refresh_token: str = Cookie(None))->Dict[str, Any]:
    """
    Проверяет, что refrash token не является просроченным
    """
    if not refresh_token:
        raise HTTPException(status_code=401, detail="No refresh token in cookies")
    try:
        payload = jwt_helper.decode_token(refresh_token)
        return payload
    except PyJWTError:
        raise HTTPException(status_code=401, detail="Problem with JWT-Token")