from pathlib import Path
from pydantic import field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

class AuthJWTConfig(BaseSettings):
    ACCESS_TOKEN_LIFETIME: int
    REFRESH_TOKEN_LIFETIME: int 
    REFRESH_TOKEN_ROTATE_MIN_LIFETIME: int 
    PRIVATE_KEY_NAME: str = "jwt-private.pem"
    PUBLIC_KEY_NAME: str = "jwt-public.pem"
    ALGORITHM: str = "RS256"

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix='auth_', 
        case_sensitive=False,
        extra="allow"
    )
    
    @field_validator("PRIVATE_KEY_NAME")
    @classmethod
    def private_key_exists(cls, value: str):
        private_key_path = Path().absolute() / "certs" / value
        if not private_key_path.exists():
            raise FileExistsError(f"Отсутствует приватный ключ по пути {private_key_path}")
        return value
    
    @field_validator("PUBLIC_KEY_NAME")
    @classmethod
    def public_key_exists(cls, value: str):
        public_key_path = Path().absolute() / "certs" / value 
        if not public_key_path.exists():
            raise FileExistsError(f"Отсутствует публичный ключ по пути {public_key_path}")
        return value

    @property
    def PRIVATE_KEY(self)->bytes:
        private_key_path = Path().absolute() / "certs" / self.PRIVATE_KEY_NAME
        with private_key_path.open("rb") as f:
            text = f.read()
        return text
    
    @property
    def PUBLIC_KEY(self)->bytes:
        public_key_path = Path().absolute() / "certs" / self.PUBLIC_KEY_NAME
        with public_key_path.open("rb") as f:
            text = f.read()
        return text

settings_auth_jwt = AuthJWTConfig()