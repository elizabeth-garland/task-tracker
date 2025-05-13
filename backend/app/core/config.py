from pydantic_settings import BaseSettings
from pydantic import PostgresDsn
from typing import Optional


class Settings(BaseSettings):
    PROJECT_NAME: str = "My FastAPI Project"
    PROJECT_DESCRIPTION: str = "A FastAPI project with proper structure"
    PROJECT_VERSION: str = "0.1.0"

    API_V1_STR: str = "/api/v1"

    DATABASE_URL: PostgresDsn

    # Add other settings as needed: JWT, CORS, etc.

    class Config:
        env_file = ".env"
        case_sensitive = True


settings = Settings()
