import os
from pydantic_settings import BaseSettings

class Settings(BaseSettings):
    APP_NAME: str = "SmartBarangay Forms API"
    APP_VERSION: str = "0.1.0"
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-secret-change-in-production")
    JWT_ALGORITHM: str = "HS256"
    ACCESS_TOKEN_EXPIRE_MINUTES: int = 60 * 24  # 24 hours
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "mysql+aiomysql://user:password@localhost:3306/smartbarangay",
    )

settings = Settings()
