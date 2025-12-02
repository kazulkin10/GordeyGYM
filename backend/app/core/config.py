from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    app_name: str = "Gordey GYM Admin API"
    env: str = Field(default="development")
    database_url: str = Field(default="postgresql://postgres:postgres@db:5432/gordeygym")
    secret_key: str = Field(default="changeme")
    access_token_expire_minutes: int = 60 * 24
    allow_entry_without_active_subscription: bool = False
    double_scan_seconds: int = 10

    class Config:
        env_file = ".env"


def get_settings() -> Settings:
    return Settings()
