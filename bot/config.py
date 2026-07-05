import os
from pydantic_settings import BaseSettings, SettingsConfigDict
from typing import Optional

class Settings(BaseSettings):
    BOT_TOKEN: str = "123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ"
    BOT_OWNER_ID: int = 12345678  # Default placeholder, will be overridden
    
    DATABASE_URL: str = "sqlite+aiosqlite:///bot.db"
    REDIS_URL: Optional[str] = None  # None will fall back to MemoryStorage
    LOGS_CHANNEL_ID: Optional[int] = None
    
    # Enable Pydantic to read from environment variables or custom files
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        extra="ignore"
    )

# Instantiate settings
try:
    settings = Settings()
except Exception:
    # Fail-safe static config if .env is missing or invalid
    class FallbackSettings:
        BOT_TOKEN = os.getenv("BOT_TOKEN", "123456789:ABCdefGhIJKlmNoPQRsTUVwxyZ")
        BOT_OWNER_ID = int(os.getenv("BOT_OWNER_ID", "12345678"))
        DATABASE_URL = os.getenv("DATABASE_URL", "sqlite+aiosqlite:///bot.db")
        REDIS_URL = os.getenv("REDIS_URL", None)
        try:
            LOGS_CHANNEL_ID = int(os.getenv("LOGS_CHANNEL_ID")) if os.getenv("LOGS_CHANNEL_ID") else None
        except ValueError:
            LOGS_CHANNEL_ID = None
            
    settings = FallbackSettings()
