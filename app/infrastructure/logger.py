import sys

from loguru import logger
import logging

# Настройка логирования
logger.remove()  # Удаляем стандартную настройку loguru (если она есть)

# Логирование в файл с ротацией (пишет в app.log)
logger.add("app.log", rotation="10 MB", level="INFO")

# Логирование на консоль
logger.add(sys.stdout, level="INFO")

# Теперь можно использовать logger.info(), logger.error() и т.д. везде в приложении
