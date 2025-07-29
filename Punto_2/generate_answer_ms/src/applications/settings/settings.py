"""Configuration settings module for the application."""
import logging
from typing import Optional, Union
from pydantic import (AliasChoices, ValidationInfo, field_validator, Field)
from src.applications.settings.base_settings import (GeneralBaseSettings)


class LoggerConfig(GeneralBaseSettings):
    """Settings for the application logging system."""
    LOGGER_FORMAT: str = "%(asctime)s - %(message)s"
    DATE_FORMAT: str = "%Y-%m-%d %H:%M:%S"
    LOG_LEVEL: Optional[Union[str, int]] = logging.INFO
    LOG_NAME: str = "uvicorn.access"

    LOGGER_DATE_FORMAT: str = Field("", validate_default=True)

    @field_validator("LOGGER_DATE_FORMAT", mode="before", check_fields=True)
    @classmethod
    def build_logger_date_format(cls, _: str, info: ValidationInfo) -> str:
        """Build formatted date string for logger output.

        Args:
            _: Placeholder for the value parameter (not used).
            info: Validation context information.

        Returns:
            str: Formatted date string enclosed in square brackets.
        """
        return "[" + info.data.get("DATE_FORMAT") + "]"


class AWSSecrets(GeneralBaseSettings):
    """AWS authentication and region configuration settings."""
    aws_access_key_id: Optional[str] = Field(
        None,
        alias='AWS_ACCESS_KEY_ID',
        validation_alias=AliasChoices("AWS_ACCESS_KEY_ID", "aws_access_key_id")
    )

    aws_secret_access_key: Optional[str] = Field(
        None,
        alias='AWS_SECRET_ACCESS_KEY',
        validation_alias=AliasChoices("AWS_SECRET_ACCESS_KEY",
                                      "aws_secret_access_key"))

    aws_session_token: Optional[str] = Field(
        None,
        alias='AWS_SESSION_TOKEN',
        validation_alias=AliasChoices("AWS_SESSION_TOKEN", "aws_session_token")
    )

    region_name: Optional[str] = Field(
        "us-east-1",
        alias='AWS_REGION',
        validation_alias=AliasChoices("AWS_REGION",
                                      "aws_region",
                                      "region_name")
    )


class Config(GeneralBaseSettings):
    """Main configuration containing URLs, AWS resources, and logging
    settings."""
    url_prefix: str
    account_id: str
    sns_error_arn: str
    openai_secret: str
    jwt_secret: str
    logger: LoggerConfig = LoggerConfig()
    aws: AWSSecrets = Field(default_factory=AWSSecrets)

    @field_validator("url_prefix", mode="before", check_fields=True)
    @classmethod
    def get_url_prefix(cls, v: str, info: ValidationInfo) -> str:
        """Normalize URL prefix to ensure consistent format.

        Args:
            v: The original URL prefix value.
            info: Validation context information.

        Returns:
            str: Normalized URL prefix with leading slash and no trailing
            slash.
        """
        if v and not v.startswith("/"):
            v = "/" + v
        v = v.rstrip("/")
        return v
