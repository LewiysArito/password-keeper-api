from typing import Optional
from pydantic_settings import BaseSettings, SettingsConfigDict
from redis.asyncio import Redis

class ConfigRedis(BaseSettings):
    USER: str
    PASSWORD: str
    HOST: str
    PORT: int = 6379
    DB_NUMBER: int = 0
    SESSION_COUNT: int = 5

    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix='redis_', 
        extra="allow"
    )
    
    @property
    def url(self) -> str:
        return (
            f"redis://{self.USER}:{self.PASSWORD}@"
            f"{self.HOST}:{self.PORT}/{self.DB_NUMBER}"
        )

settings_redis = ConfigRedis()