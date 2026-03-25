from loguru import logger
import sys
from app.utils.config import settings

# Настройка логгера
logger.remove()
logger.add(sys.stderr, level=settings.log_level, format="{time} | {level} | {message}")
logger.add("logs/bot.log", rotation="1 day", retention="7 days", level="INFO")

def get_logger(name: str) -> logger:
    return logger.bind(module=name)