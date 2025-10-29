import os
from pydantic import BaseSettings

class Settings(BaseSettings):
    database_url: str = os.getenv("DATABASE_URL", "postgresql://signuser:signpass@localhost:5432/signdb")
    broker_url: str = os.getenv("CELERY_BROKER_URL", "redis://redis:6379/0")
    result_backend: str = os.getenv("CELERY_RESULT_BACKEND", "redis://localhost:6379/0")
    storage_path: str = os.getenv("STORAGE_PATH", "/app/storage")
    minio_endpoint: str = os.getenv("MINIO_ENDPOINT")
    minio_access_key: str = os.getenv("MINIO_ACCESS_KEY")
    minio_secret_key: str = os.getenv("MINIO_SECRET_KEY")
    minio_bucket: str = os.getenv("MINIO_BUCKET", "sign-dataset")
    access_token_secret: str = os.getenv("ACCESS_TOKEN_SECRET", "your-access-token-secret")
    refresh_token_secret: str = os.getenv("REFRESH_TOKEN_SECRET", "your-refresh-token-secret")

settings = Settings()
