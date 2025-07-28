"""Dependency injection container module for the application."""
from pathlib import Path
from openai import OpenAI
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, SSLError

from src.applications.settings import APP_CONFIG_FILE as CONFIG_FILE
from src.applications.settings.base_settings import GeneralBaseModel
from src.applications.settings.logger import Logger
from src.applications.settings.settings import Config
from src.domain.usecase import (CheckHealthUseCase)
from src.infraestructure.driven_adapters import (SnsRepository)
from src.infraestructure.helpers.utils import load_json_file
from src.domain.usecase.improve_question.improve_question_use_case import ImproveQuestionUseCase
from src.domain.model.question.question_model import question
from src.infraestructure.driven_adapters.openai.adapter.openai_adapter import OpenAIQuestionImprover
from src.infraestructure.driven_adapters.secret_repository.adapter.secret_manager_adapter import SecretManagerService


class SettingsPaths(GeneralBaseModel):
    """Container for configuration file paths."""
    CONFIG_PATH: Path


class Container(GeneralBaseModel):
    """Dependency injection container for application services
    and use cases."""
    app_config: Config
    check_health_use_case: CheckHealthUseCase
    improver_use_case: ImproveQuestionUseCase
    logger: Logger
    jwt: str


def get_deps_container() -> Container:
    """Create and configure the dependency injection container.
    Returns:
        Container: Fully configured application container with
        all dependencies.
    """
    config_paths = SettingsPaths(CONFIG_PATH=(CONFIG_FILE))
    dict_app_config = load_json_file(config_paths.CONFIG_PATH)
    dict_app_config["region_name"] = (
        boto3.session.Session().region_name
        if boto3.session.Session().region_name
        else "us-east-1"
    )
    try:
        dict_app_config["account_id"] = (
            boto3.client("sts").get_caller_identity().get("Account")
        )
        dict_app_config["sns_error_arn"] = ":".join([
            "arn:aws:sns",
            str(dict_app_config["region_name"]),
            str(dict_app_config["account_id"]),
            str(dict_app_config["error_notification_service_name"])
        ])
    except (NoCredentialsError, ClientError, SSLError):
        dict_app_config["account_id"] = ""
        dict_app_config["sns_error_arn"] = ""

    app_config = Config(**dict_app_config)
    logger = Logger(app_config.logger)
    logger.info("Configs load successfully.")
    secret_service = SecretManagerService(
        aws_config=app_config.aws, logger=logger)
    check_health_use_case = CheckHealthUseCase(app_config, logger)
    sns_repository = SnsRepository(app_config, logger)
    openai_secret = secret_service.get_secret(
        app_config.openai_secret)
    client = OpenAI(api_key=openai_secret["key"])
    jwt_secret = secret_service.get_secret(app_config.jwt_secret)
    gateway = OpenAIQuestionImprover(client)
    improve_use_case = ImproveQuestionUseCase(gateway, sns_repository, logger)
    logger.info("Generate the dependencies container successfully.")
    return Container(
        app_config=app_config,
        check_health_use_case=check_health_use_case,
        improver_use_case=improve_use_case,
        logger=logger,
        jwt=jwt_secret["jwt"]
    )
