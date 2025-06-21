from typing import Annotated, Dict
from fastapi import APIRouter,Depends, HTTPException, Response, Cookie
from fastapi.security import OAuth2PasswordRequestForm
from starlette.status import (
    HTTP_201_CREATED,
    HTTP_200_OK,
    HTTP_500_INTERNAL_SERVER_ERROR
)
from src.auth.depends.auth_depends import get_current_user, get_refresh_token_from_cookies
from src.auth.schemas.token_schemas import AccessTokenInfo, TokenInfo
from src.auth.services.auth_service import auth_service
from src.config.auth.auth_helper import jwt_helper
from src.schemas.user_schemas import UserCreate, UserLogin
router = APIRouter(prefix="/auth", tags=["Auth"])

@router.post(
    "/login", 
    response_model=AccessTokenInfo,
    status_code=HTTP_200_OK,
    summary="User login",
    description="Authenticate user and return access token",
    responses={
        200: {"description": "Successful authentication"},
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"}
    }
)
async def login(
    credentials: Annotated[OAuth2PasswordRequestForm, Depends()],
    response: Response
):
    try:
        new_credentials = UserLogin(login=credentials.username, password=credentials.password)
        tokens_info = await auth_service.login(new_credentials)
        access_token: AccessTokenInfo = {
            "access_token": tokens_info.access_token,
            "token_type": tokens_info.token_type
        }

        response.set_cookie(
            key="refresh_token",
            value=tokens_info.refrash_token,
        )

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
    "/refresh",
    status_code=HTTP_200_OK,
    summary="User refresh token",
    responses={
        200: {"description": "Successful authentication"},
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"}
    }
)
async def refresh(
    token: Annotated[Dict, Depends(get_refresh_token_from_cookies)],
    response: Response
):
    try:
        tokens_info = await auth_service.refrash(token)

        access_token: AccessTokenInfo = {
            "access_token": tokens_info.access_token,
            "token_type": tokens_info.token_type
        }
        
        response.set_cookie(
            key="refresh_token",
            value=tokens_info.refrash_token,
            httponly=True
        )

        return access_token
    except HTTPException as e:
        raise HTTPException(e.status_code, e.detail)
    except Exception as e:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, str(e))

@router.post(
    "/logout",
    status_code=HTTP_200_OK,
    summary="Close user session",
    responses={
        200: {"description": "Successful logout"},
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"}
    }
)
async def logout(
    token: Annotated[Dict, Depends(get_refresh_token_from_cookies)],
    response: Response
):
    try:
        is_success = await auth_service.logout()
        response.delete_cookie("refresh_token")

        return {"is_success": True}
    except HTTPException as e:
        raise HTTPException(e.status_code, e.detail)
    except Exception as e:
        raise HTTPException(HTTP_500_INTERNAL_SERVER_ERROR, str(e))

@router.post(
    "/logout_all",
    status_code=HTTP_200_OK,
    summary="Close all user sessions",
    responses={
        200: {"description": "Successful logout from all accounts"},
        401: {"description": "Unauthorized"},
        500: {"description": "Internal server error"}
    }
)
async def logout_all(
    token: Annotated[Dict, Depends(get_refresh_token_from_cookies)],
    response: Response
):
    try:
        is_success = await auth_service.logout_all()
        response.delete_cookie("refresh_token")
        
        return {"is_success": True}
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

