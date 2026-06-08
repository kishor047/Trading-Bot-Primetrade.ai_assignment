from __future__ import annotations

import logging
import os
from pathlib import Path

DEFAULT_LOG_FILE = "logs/trading_bot.log"


def setup_logging(log_path: str | None = None) -> logging.Logger:
    logger = logging.getLogger("trading_bot")
    if logger.handlers:
        return logger

    log_file = log_path or os.getenv("TRADING_BOT_LOG_FILE", DEFAULT_LOG_FILE)
    log_path_obj = Path(log_file)
    log_path_obj.parent.mkdir(parents=True, exist_ok=True)

    logger.setLevel(logging.INFO)
    formatter = logging.Formatter("%(asctime)s | %(levelname)s | %(name)s | %(message)s")

    file_handler = logging.FileHandler(log_path_obj)
    file_handler.setLevel(logging.INFO)
    file_handler.setFormatter(formatter)

    stream_handler = logging.StreamHandler()
    stream_handler.setLevel(logging.INFO)
    stream_handler.setFormatter(formatter)

    logger.addHandler(file_handler)
    logger.addHandler(stream_handler)
    logger.propagate = False
    return logger
