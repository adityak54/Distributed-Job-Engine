from pydantic_settings import BaseSettings
from pydantic import Field


class Settings(BaseSettings):
    DATABASE_URL: str = "postgresql://engine_user:engine_password@localhost:5432/job_engine_db"
    REDIS_URL: str = "redis://localhost:6379/0"
    ENVIRONMENT: str = "dev"
    WORKER_CONCURRENCY: int = Field(default=4, ge=1)
    LOG_LEVEL: str = "INFO"
    WORKER_ID: str = "worker-1"

    model_config = {"env_file": ".env", "env_file_encoding": "utf-8"}


settings = Settings()
