import os
from dotenv import load_dotenv

load_dotenv()

class Config:
    DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///./test.db")
    SECRET_KEY = os.getenv("SECRET_KEY", "your-secret-key-change-in-production")
    REDIS_URL = os.getenv("REDIS_URL", "redis://localhost:6379")