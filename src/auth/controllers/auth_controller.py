from fastapi import APIRouter,Depends,HTTPException, status, Header, Response, Cookie
from fastapi.security import HTTPDigest, HTTPBasicCredentials
from starlette.status import HTTP_400_BAD_REQUEST, HTTP_204_NO_CONTENT
from typing import Annotated, Any
from time import time
from src.auth.schemas import *
from src.auth.schemas.user_schemas import UserCreate, UserLogin

router = APIRouter(prefix="/auth", tags=["Auth"])

@router.get("/login")
async def login(
    credentials: Annotated[HTTPBasicCredentials, Depends(HTTPDigest())],
):
    print(credentials)
    try:
        return await auth_service.register()
    except Exception as e:
        raise HTTPException(HTTP_400_BAD_REQUEST, str(e))

@router.post("/register")
def register(
    data: UserCreate
):
    pass