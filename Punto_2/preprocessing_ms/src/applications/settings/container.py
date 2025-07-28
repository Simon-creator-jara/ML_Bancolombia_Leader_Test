"""Dependency injection container module for the application."""
from pathlib import Path
import psycopg2.pool as pool_py
from openai import OpenAI
import boto3
from botocore.exceptions import ClientError, NoCredentialsError, SSLError

from src.applications.settings import APP_CONFIG_FILE as CONFIG_FILE
from src.applications.settings.base_settings import GeneralBaseModel
from src.applications.settings.logger import Logger
from src.applications.settings.settings import Config
from src.domain.usecase import (CheckHealthUseCase, DatasetCleanerImpl,
                                SplitterImpl)
# from src.infraestructure.driven_adapters import (S3OCRRepository,
# SnsRepository, SqsRepository)
from src.infraestructure.driven_adapters import (SnsRepository)
from src.infraestructure.helpers.utils import load_json_file
from src.domain.usecase.clean_data.clean_data_use_case import DatasetCleanerImpl
from src.domain.usecase.split_data.split_data_use_case import SplitterImpl
from src.domain.usecase.embed_store.embed_store_use_case import EmbedAndStoreUseCase
from src.domain.model.dataset.dataset_model import RawDataset
from src.infraestructure.driven_adapters.openai.adapter.openai_embedding_adapter import OpenAIEmbeddingAdapter
from src.infraestructure.driven_adapters.postgres.adapter.postgres_chunk_repository import PostgresChunkRepository
from src.infraestructure.driven_adapters.secret_repository.adapter.secret_manager_adapter import SecretManagerService


class SettingsPaths(GeneralBaseModel):
    """Container for configuration file paths."""
    CONFIG_PATH: Path


class Container(GeneralBaseModel):
    """Dependency injection container for application services
    and use cases."""
    app_config: Config
    check_health_use_case: CheckHealthUseCase
    dataset_cleaner_use_case: DatasetCleanerImpl
    splitter_use_case: SplitterImpl
    embed_store_use_case: EmbedAndStoreUseCase
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
    rds_secret = secret_service.get_secret(app_config.rds_secret)
    pool = pool_py.SimpleConnectionPool(
        user=rds_secret["username"],
        password=rds_secret["password"],
        database="postgres",
        host="demorag.cioitd2c2d12.us-east-1.rds.amazonaws.com",
        port=5432,
        minconn=1,
        maxconn=100
    )
    check_health_use_case = CheckHealthUseCase(app_config, logger)
    # s3_repository = S3OCRRepository(app_config, logger)
    sns_repository = SnsRepository(app_config, logger)
    # sqs_repository = SqsRepository(app_config, logger)
    dataset_cleaner_use_case = DatasetCleanerImpl(
        logger=logger, sns_notifier=sns_repository
    )
    splitter_use_case = SplitterImpl(
        logger=logger, sns_notifier=sns_repository
    )
    repo = PostgresChunkRepository(pool)
    openai_secret = secret_service.get_secret(
        app_config.openai_secret)
    client = OpenAI(api_key=openai_secret["key"])
    jwt_secret = secret_service.get_secret(app_config.jwt_secret)
    embedder = OpenAIEmbeddingAdapter(client)
    embed_store = EmbedAndStoreUseCase(logger, embedder, repo)
    logger.info("Generate the dependencies container successfully.")
    return Container(
        app_config=app_config,
        check_health_use_case=check_health_use_case,
        dataset_cleaner_use_case=dataset_cleaner_use_case,
        splitter_use_case=splitter_use_case,
        embed_store_use_case=embed_store,
        logger=logger,
        jwt=jwt_secret["jwt"]
    )
