"""POE Backend — Application settings (Pydantic Settings)."""

from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    environment: str = "development"
    log_level: str = "DEBUG"
    database_url: str
    redis_url: str = "redis://localhost:6379/0"
    nats_url: str = "nats://localhost:4222"
    secret_key: str
    jwt_algorithm: str = "HS256"
    jwt_expire_minutes: int = 60
    api_host: str = "0.0.0.0"
    api_port: int = 8000

    model_config = {
        "env_file": ".env",
        "env_file_encoding": "utf-8",
        "case_sensitive": False,
    }


settings = Settings()