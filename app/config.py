from pydantic_settings import BaseSettings
from functools import lru_cache


class Settings(BaseSettings):
    # Database
    database_url: str

    # Security
    secret_key: str
    algorithm: str = "HS256"
    access_token_expire_minutes: int = 1440

    # Redis
    redis_url: str

    # Email
    smtp_host: str
    smtp_port: int
    smtp_user: str
    smtp_password: str

    # CloudPayments
    cloudpayments_public_key: str
    cloudpayments_secret_key: str

    # CORS
    allowed_origins: list[str]

    # Application
    debug: bool = False
    environment: str = "production"

    class Config:
        env_file = ".env"


@lru_cache()
def get_settings():
    return Settings()


settings = get_settings()