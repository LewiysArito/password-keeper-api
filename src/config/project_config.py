from pydantic_settings import BaseSettings, SettingsConfigDict

class ProjectConfig(BaseSettings):
    DB_ECHO: bool
    NAME: str
    VERSION: str
    DEBUG: bool
    CORS_ALLOWED_ORIGINS: str
    PORT: str
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        env_prefix='project_', 
        extra="allow"
    )

settings_project = ProjectConfig()
