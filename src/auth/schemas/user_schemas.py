from typing import Optional
from pydantic import BaseModel, ConfigDict, Field, EmailStr, field_validator

class UserCreate(BaseModel):
    model_config = ConfigDict(regex_engine='python-re')
    
    login: str = Field(
        min_length=7,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Логин не должен быть менее 7 символов. Также может содержить только буквы цифры и нижние подчеркивания"
    )
    password: str = Field(  
        min_length=8,
        description="Пароль должен содержать: "
            "1 заглавную букву, 1 строчную букву, 1 цифру, 1 спецсимвол (!@#$%^&*()), длина не менее 8 символов"
    )
    email: Optional[EmailStr] = Field(
        default=None,
        description="Почтовый email"
    )
    phone: Optional[str] = Field(
        default=None,
        pattern=r"^[\+]?[(]?[0-9]{3}[)]?[-\s\.]?[0-9]{3}[-\s\.]?[0-9]{4,6}$",
        description="Номер телефона"
    )



class UserLogin(BaseModel):
    login: str
    password: str

class UserUpdate(BaseModel):
    login: str
    password: str