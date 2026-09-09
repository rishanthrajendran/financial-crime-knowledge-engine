"""
Application configuration using Pydantic Settings.

All configuration is loaded from environment variables with sensible defaults
for local development. Use .env.example as a template for .env files.

IMPORTANT: The env_file path is set to an absolute path based on this file's
location to prevent parent-directory .env leakage. The application will ONLY
load .env from the apps/api/ directory, not from parent directories.
"""

from functools import lru_cache
from pathlib import Path
from typing import Literal

from pydantic import Field, field_validator
from pydantic_settings import BaseSettings, SettingsConfigDict

# Get the directory where this config file is located
_CONFIG_DIR = Path(__file__).resolve().parent


class Settings(BaseSettings):
    """Application settings loaded from environment variables."""

    model_config = SettingsConfigDict(
        # Use absolute path to prevent parent directory .env leakage
        env_file=str(_CONFIG_DIR / ".env"),
        env_file_encoding="utf-8",
        case_sensitive=False,
        extra="ignore",
    )

    # Application
    app_name: str = "Financial Crime Knowledge Engine"
    app_version: str = "0.1.0"
    app_env: Literal["development", "staging", "production"] = "development"
    debug: bool = False

    # API Server
    api_host: str = "0.0.0.0"
    api_port: int = 8000
    api_workers: int = 1
    cors_origins: list[str] = Field(default=["http://localhost:3000", "http://127.0.0.1:3000"])

    @field_validator("cors_origins", mode="before")
    @classmethod
    def parse_cors_origins(cls, v: str | list[str]) -> list[str]:
        if isinstance(v, str):
            return [origin.strip() for origin in v.split(",")]
        return v

    # Database
    database_url: str = "postgresql+asyncpg://fcke:fcke_dev@localhost:5432/fcke"
    database_pool_size: int = 10
    database_max_overflow: int = 20
    database_echo: bool = False

    # Redis
    redis_url: str = "redis://localhost:6379/0"

    # Worker (for reference)
    worker_concurrency: int = 2
    worker_max_retries: int = 3

    # Feature Flags
    feature_auth_enabled: bool = False
    feature_rag_enabled: bool = False
    feature_graph_search_enabled: bool = False
    feature_embeddings_enabled: bool = False

    # Knowledge Base
    knowledge_base_version: str = "v3.0.1"

    @property
    def is_production(self) -> bool:
        return self.app_env == "production"

    @property
    def is_development(self) -> bool:
        return self.app_env == "development"


@lru_cache
def get_settings() -> Settings:
    """Get cached settings instance."""
    return Settings()


# Export for convenience
settings = get_settings()
