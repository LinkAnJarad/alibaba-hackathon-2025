import os
from pydantic import BaseModel

class Settings(BaseModel):
    APP_NAME: str = "SmartBarangay Forms API"
    APP_VERSION: str = "0.1.0"
    JWT_SECRET: str = os.getenv("JWT_SECRET", "dev-secret")
    JWT_ALGORITHM: str = "HS256"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "mysql+aiomysql://user:password@localhost:3306/smartbarangay",
    )

settings = Settings()
