import logging
import traceback
from typing import TYPE_CHECKING

if TYPE_CHECKING:
    from src.applications.settings.settings import LoggerConfig


class Logger:
    """Logger class."""

    def __init__(self, logger_config: "LoggerConfig"):
        formatter = logging.Formatter(
            fmt=logger_config.LOGGER_FORMAT,
            datefmt=logger_config.LOGGER_DATE_FORMAT,
        )
        handler = logging.StreamHandler()
        handler.setFormatter(formatter)
        handler.setLevel(int(logger_config.LOG_LEVEL))

        log = logging.getLogger(logger_config.LOG_NAME)
        log.handlers = [handler]

        self.log = log
        self.log.info(
            "Logger initialized with level %s", logger_config.LOG_LEVEL
        )

    def info(self, msg: str, **kwargs):
        """Log a message with severity 'INFO'."""
        self.log.info(msg, **kwargs)

    def error(self, msg: str, **kwargs):
        """Log a message with severity 'ERROR'."""
        self.log.error(msg, **kwargs)

    def debug(self, msg: str, **kwargs):
        """Log a message with severity 'DEBUG'."""
        self.log.debug(msg, **kwargs)

    def exceptions_handler(self, msg, **kwargs):
        """Especifica la traza del error y el tipo de error generado."""
        trace = traceback.format_exc(limit=1).replace("\n", "")
        self.error(f"{msg} - {trace.strip()}", **kwargs)
