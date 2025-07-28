import sys
import json
import pytest
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root)) 
from src.infraestructure.driven_adapters.sns_repository.adapter.\
    sns_repository import SnsRepository
from unittest.mock import MagicMock


CONFIG_FOLDER = "tests/unit-test/config_test"


def load_json(file_path):
    """Load and parse a JSON file.

    Args:
        file_path: Path to the JSON file.

    Returns:
        dict: Parsed JSON content.
    """
    with open(file_path, encoding="utf-8") as f:
        return json.load(f)


@pytest.fixture
def local_config_app():
    """Provide basic application configuration for testing.

    Returns:
        dict: Mock application configuration with test values.
    """
    return {
        "url_prefix": "/test",
        "account_id": "123456789012",
        "sns_error_arn": "arn:aws:sns:us-east-1:123456789012:test",
        "rds_secret": "arn:aws:secretsmanager:us-east-1:697289108405:secret:rds!db-30d01429-dc7d-4927-98a1-e016c10816ae-jemNHq",
        "openai_secret": "arn:aws:secretsmanager:us-east-1:697289108405:secret:openai-LfZpny",
        "jwt_secret": "arn:aws:secretsmanager:us-east-1:697289108405:secret:jwt_secret-37brE6"
    }


@pytest.fixture
def config_folder():
    """Provide test configuration folder path.

    Returns:
        str: Path to the test configuration folder.
    """
    return CONFIG_FOLDER


@pytest.fixture
def load_config_app():
    """Load extended application configuration from a JSON file.

    Returns:
        dict: Application configuration with AWS resource identifiers.
    """
    config_dict = load_json(CONFIG_FOLDER +
                            "/config.json")
    config_dict["max_message_per_queue_request"] = 1
    config_dict["region_name"] = 'us-east-1'
    config_dict["account_id"] = '123456789012'
    config_dict["error_notification_service_arn"] = (
        "arn:aws:sns:"
        + str(config_dict["region_name"])
        + ":"
        + str(config_dict["account_id"])
        + ":"
        + str(config_dict["error_notification_service_name"])
    )

    return config_dict


@pytest.fixture
def mock_boto3_client(mocker):
    """Mock boto3 client for AWS service testing.

    Args:
        mocker: Pytest mocker fixture.

    Returns:
        MagicMock: Mocked boto3 client.
    """
    return mocker.patch(
        "src.infraestructure.driven_adapters.s3_repository.adapter."
        "s3_repository.boto3.client"
    )


@pytest.fixture
def mock_logger(mocker):
    """Provide a mock logger for testing.

    Args:
        mocker: Pytest mocker fixture.

    Returns:
        MagicMock: Mock logger instance.
    """
    return mocker.MagicMock()

@pytest.fixture
def sns_repository(mock_boto3_client, mock_logger):
    """Create SNS repository with mocked dependencies.

    Args:
        mock_boto3_client: Mocked boto3 client.
        mock_logger: Mock logger instance.

    Returns:
        SnsRepository: SNS repository with mocked configuration.
    """
    mock_config = MagicMock()
    mock_config.aws.model_dump.return_value = {}
    mock_config.sns_error_arn = "arn:aws:sns:us-east-1:123456789012:test-topic"
    return SnsRepository(config=mock_config, logger=mock_logger)

