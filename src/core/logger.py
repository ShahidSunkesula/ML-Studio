"""
logger.py

Purpose:
    Configures and provides the application logger.

Author:
    Shahid

Project:
    ML Studio
"""

import logging

from src.config.config import PROJECT_ROOT


LOGS_DIR = PROJECT_ROOT / "logs"
LOGS_DIR.mkdir(parents=True, exist_ok=True)

LOG_FILE = LOGS_DIR / "ml_studio.log"


def get_logger(name: str) -> logging.Logger:
    """
    Return a configured logger instance.
    """

    logger = logging.getLogger(name)

    if logger.handlers:
        return logger

    logger.setLevel(logging.INFO)

    formatter = logging.Formatter(
        "%(asctime)s | %(levelname)s | %(name)s | %(message)s"
    )

    file_handler = logging.FileHandler(LOG_FILE)

    file_handler.setFormatter(formatter)

    console_handler = logging.StreamHandler()

    console_handler.setFormatter(formatter)

    logger.addHandler(file_handler)

    logger.addHandler(console_handler)

    logger.propagate = False

    return logger