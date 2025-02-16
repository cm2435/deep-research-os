import logging
from logging import Logger, StreamHandler, Formatter
from typing import Optional


class RichLogger:
    def __init__(self, name: str, level: int = logging.INFO, fmt: Optional[str] = None):
        self.logger = logging.getLogger(name)
        self.logger.setLevel(level)
        handler = StreamHandler()
        handler.setLevel(level)
        formatter = Formatter(
            fmt or "%(asctime)s - %(name)s - %(levelname)s - %(message)s"
        )
        handler.setFormatter(formatter)
        self.logger.addHandler(handler)
        self.logger.info(
            f"Logger {name} initialized with level {logging.getLevelName(level)}"
        )

    def get_logger(self) -> Logger:
        return self.logger


def get_logger(
    name: str, level: int = logging.INFO, fmt: Optional[str] = None
) -> Logger:
    return RichLogger(name, level, fmt).get_logger()
