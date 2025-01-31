from datetime import time
from typing import Set

from pydantic_settings import BaseSettings, SettingsConfigDict
from pydantic import SecretStr


class Settings(BaseSettings):
    DATABASE_URL: str
    TELEGRAM_BOT_API_TOKEN: SecretStr
    ADMINS_TELEGRAM_ID: Set[int]
    NOTIFICATION_TIME: time = time(20, 0)

    model_config = SettingsConfigDict(env_file=".env", env_file_encoding="utf-8")


settings = Settings()
