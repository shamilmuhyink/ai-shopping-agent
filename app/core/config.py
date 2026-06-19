import os
from typing import List, Optional
from functools import lru_cache
from pathlib import Path

from dotenv import load_dotenv
from pydantic import AnyHttpUrl, Field, PostgresDsn, RedisDsn, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    APP_NAME: str = "Agentic AI Shopping Assistant"
    APP_ENV: str = "development"
    DEBUG: bool = False
    ALLOWED_ORIGINS: List[AnyHttpUrl] = []

    # Database
    DATABASE_URL: PostgresDsn
    DATABASE_POOL_SIZE: int = 10
    DATABASE_MAX_OVERFLOW: int = 20

    # Redis
    REDIS_URL: RedisDsn

    # LLM APIs
    GROQ_API_KEY: str = Field(...)
    OPENROUTER_API_KEY: Optional[str] = None

    # Internal Integration
    MAIN_BACKEND_URL: AnyHttpUrl
    SERVICE_TOKEN: str = Field(...)

    @field_validator("APP_ENV")
    @classmethod
    def validate_env(cls, v: str) -> str:
        allowed = {"development", "staging", "production"}
        if v not in allowed:
            raise ValueError(f"APP_ENV must be one of {allowed}")
        return v


@lru_cache
def get_settings() -> Settings:
    # Get the directory of the current file (app/core)
    # Then go up two levels to reach the ai-assistant root
    root_dir = Path(__file__).resolve().parent.parent.parent

    # 1. Look for APP_ENV in current environment
    # 2. If not found, try loading base .env using absolute path
    base_env = root_dir / ".env"
    load_dotenv(base_env)
    env = os.getenv("APP_ENV", "development")

    # 3. Load the environment-specific file using absolute path
    env_file = root_dir / f".env.{env}"

    # If the specific file doesn't exist, fall back to base .env
    if not env_file.exists():
        env_file = base_env

    return Settings(_env_file=str(env_file))
