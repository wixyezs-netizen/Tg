from pydantic import BaseSettings
from typing import Optional
import os
from dotenv import load_dotenv

load_dotenv()

class Settings(BaseSettings):
    telegram_bot_token: str
    yoomoney_access_token: str
    yoomoney_wallet: str
    admin_id: int
    database_url: str = "sqlite:///shop.db"
    referral_bonus: int = 50
    log_level: str = "INFO"
    
    class Config:
        env_file = ".env"

settings = Settings()