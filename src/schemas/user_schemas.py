import re
from typing import Optional
from pydantic import ConfigDict, Field, EmailStr, field_validator
from src.schemas.base_schema import BaseSchema, CreateSchema, UpdateSchema

class UserCreate(CreateSchema):
    model_config = ConfigDict(regex_engine='python-re')
    
    login: str = Field(
        min_length=7,
        description="Логин не должен быть менее 7 символов. Также может содержить только буквы цифры и нижние подчеркивания"
    )
    password: str = Field(  
        description="Пароль должен содержать: "
            "хотя бы 1 заглавную букву, 1 строчную букву, 1 цифру, 1 спецсимвол (!@#$%^&*()), длина не менее 8 символов"
    )
    email: Optional[EmailStr] = Field(
        default=None,
        description="Почтовый email"
    )
    phone: Optional[str] = Field(
        default=None,
        pattern=r"^((8|\+374|\+994|\+995|\+375|\+7|\+380|\+38|\+996|\+998|\+993)[\- ]?)?\(?\d{3,5}\)?[\- ]?\d{1}[\- ]?\d{1}",
        description="Номер телефона"
    )

    @field_validator("password")
    def check_password(cls, value):
        "проверяет пароль"
        pattern="(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{8,}"
        
        if not re.match(pattern, value):
            raise ValueError("Пароль должен содержать: "
            "хотя бы 1 заглавную букву, 1 строчную букву, 1 цифру, 1 спецсимвол (!@#$%^&*()), длина не менее 8 символов")
        
        return value

class UserLogin(BaseSchema):
    login: str
    password: str

class UserUpdate(UpdateSchema):
    login: str = Field(
        min_length=7,
        pattern=r"^[a-zA-Z0-9_]+$",
        description="Логин не должен быть менее 7 символов. Также может содержить только буквы цифры и нижние подчеркивания"
    )
    password: str = Field(  
        description="Пароль должен содержать: "
            "хотя бы 1 заглавную букву, 1 строчную букву, 1 цифру, 1 спецсимвол (!@#$%^&*()), длина не менее 8 символов"
    )
    @field_validator("password")
    def check_password(cls, value):
        "проверяет пароль"
        pattern="(?=.*[0-9])(?=.*[!@#$%^&*])(?=.*[a-z])(?=.*[A-Z])[0-9a-zA-Z!@#$%^&*]{8,}"
        
        if not re.match(pattern, value):
            raise ValueError("Пароль должен содержать: "
            "хотя бы 1 заглавную букву, 1 строчную букву, 1 цифру, 1 спецсимвол (!@#$%^&*()), длина не менее 8 символов")

        return value