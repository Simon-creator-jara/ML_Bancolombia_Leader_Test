import logging
import pytest

from src.applications.settings.logger import Logger
from src.applications.settings.settings import Config


@pytest.mark.parametrize(
    "logger_type",
    [("info"),
     ("error"),
     ("debug"),
     ("exception")
     ]
)
def test_log(caplog, logger_type, local_config_app):
    """Test that all logger methods correctly log messages.

    Args:
        caplog: Pytest fixture to capture log output.
        logger_type: Type of logging method to test
        (info, error, debug, exception).
        local_config_app: Configuration fixture for application settings.
    """
    config = Config(**local_config_app)
    logger = Logger(config.logger)
    with caplog.at_level(logging.DEBUG, logger=logger.log.name):
        if logger_type == "info":
            logger.info("testing")
        elif logger_type == "error":
            logger.error("testing")
        elif logger_type == "exception":
            logger.exceptions_handler("testing")
        elif logger_type == "debug":
            logger.debug("testing")
    assert "testing" in caplog.text
