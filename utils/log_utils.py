# utils/log_utils.py
from loguru import logger

from config.settings import INFO_FILE, DEBUG_FILE, ERROR_FILE
# Функция для настройки логгера


def configure_logger():
    """
    Настройка логгера с использованием трех уровней: INFO, DEBUG, ERROR.
    Логи сохраняются в файлы с автоматическим разбиением по размеру (10 MB).
    """
    logger.remove()  # Удаляем все предыдущие конфигурации логгера
    logger.add(
        INFO_FILE,
        format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}",
        level="INFO",
        filter=lambda record: record["level"].name == "INFO",
        rotation="10 MB",
    )
    logger.add(
        DEBUG_FILE,
        format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}",
        level="DEBUG",
        filter=lambda record: record["level"].name == "DEBUG",
        rotation="10 MB",
    )
    logger.add(
        ERROR_FILE,
        format="{time:DD-MM-YYYY at HH:mm:ss} | {level} | {message}",
        level="ERROR",
        filter=lambda record: record["level"].name == "ERROR",
        rotation="10 MB",
    )
