from typing import Annotated, Dict
from fastapi import APIRouter,Depends, HTTPException
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from src.auth.depends.auth_depends import get_current_user
from src.auth.schemas.token_schemas import TokenInfo
from src.auth.services.auth_service import auth_service
from src.config.auth.auth_helper import jwt_helper
from src.models.user_model import UserTable as UserModel
from src.schemas.user_schemas import UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/login", 
    response_model=TokenInfo,
    status_code=HTTP_200_OK,
    summary="User login",
    description="Authenticate user and return access token",
    responses={
        200: {"description": "Successful authentication"},
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"}
    }
)
async def login_for_access_token(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
):
    try:
        new_credentials = UserLogin(login=credentials.username, password=credentials.password)
        access_token = await auth_service.login_for_access_token(new_credentials)
        return access_token
    except HTTPException as e:
        raise HTTPException(e.status_code, e.detail)
    except Exception as e:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, str(e))

@router.post(
    "/register",
    status_code=HTTP_201_CREATED,
    summary="User register",
    description="Registrer new user",
    responses={
        201: {"description": "Successful register"},
        409 :{"description": "Conflict in exists data"},
        422: {"description": "Validation Error"},
        500: {"description": "Internal server error"}
    }
)
async def register(
    data: UserCreate
):
    try:
        user = await auth_service.register(data)
        return user
    except HTTPException as e:
        raise HTTPException(e.status_code, e.detail)
    except Exception as e:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, str(e))
    
@router.post(
    "/session_is_active", 
    status_code=HTTP_200_OK,
    summary="Check session status",
    responses={
        200: {"description": "Successful register"},
        401: {"description": "JWT Token problem"},
        403: {"description": "Forbidden"},
        500: {"description": "Internal server error"}
    }
)
async def session_is_active(
    token: Annotated[Dict, Depends(get_current_user)]
):
    try:
        return {
            "user_id": token["sub"],
            "username" : token["username"],
            "status": "active"
        }
    except HTTPException as e:
        raise HTTPException(e.status_code, e.detail)
    except Exception as e:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, str(e))