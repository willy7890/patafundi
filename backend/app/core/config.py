from functools import lru_cache
from typing import List
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    APP_NAME: str = "PataFundi"
    APP_ENV: str = "development"
    DEBUG: bool = True
    API_V1_PREFIX: str = "/api/v1"

    DATABASE_URL: str = "postgresql://patafundi:patafundi_secret@localhost:5432/patafundi"

    SECRET_KEY: str = "change-this-to-a-long-random-secret-in-production-please"
    ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 30
    REFRESH_TOKEN_EXPIRE_DAYS: int = 7

    BACKEND_CORS_ORIGINS: List[str] = [
        "http://localhost:5173",
        "http://127.0.0.1:5173",
        "http://localhost:3000"
        "https://patafundi-eta.vercel.app/",
    ]

    REDIS_URL: str = "redis://localhost:6379/0"
    PAYMENT_MODE: str = "development"  # development | production
    UPLOAD_DIR: str = "./uploads"
    MAX_UPLOAD_SIZE_MB: int = 10
    INFRASTRUCTURE_MODE: str = "FREE"  # FREE | SCALING_REVIEW | PRODUCTION


@lru_cache
def get_settings() -> Settings:
    return Settings()


settings = get_settings()
