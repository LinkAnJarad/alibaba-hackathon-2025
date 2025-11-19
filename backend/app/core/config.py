import os
from pydantic_settings import BaseSettings
from dotenv import load_dotenv

# Load .env file
load_dotenv()

class Settings(BaseSettings):
    APP_NAME: str = "SmartBarangay Forms API"
    APP_VERSION: str = "0.1.0"
    DATABASE_URL: str = os.getenv(
        "DATABASE_URL",
        "mysql+aiomysql://user:password@localhost:3306/smartbarangay",
    )
    # Alibaba Cloud credentials (placeholder)
    ALIBABA_ACCESS_KEY_ID: str = os.getenv("ALIBABA_ACCESS_KEY_ID", "")
    ALIBABA_ACCESS_KEY_SECRET: str = os.getenv("ALIBABA_ACCESS_KEY_SECRET", "")
    ALIBABA_OSS_BUCKET: str = os.getenv("ALIBABA_OSS_BUCKET", "smartbarangay-forms")
    ALIBABA_OSS_REGION: str = os.getenv("ALIBABA_OSS_REGION", "oss-ap-southeast-1")
    ALIBABA_PAI_ENDPOINT: str = os.getenv("ALIBABA_PAI_ENDPOINT", "")
    # Qwen model API endpoint
    QWEN_API_KEY: str = os.getenv("QWEN_API_KEY", "")
    QWEN_API_ENDPOINT: str = os.getenv("QWEN_API_ENDPOINT", "")

settings = Settings()
