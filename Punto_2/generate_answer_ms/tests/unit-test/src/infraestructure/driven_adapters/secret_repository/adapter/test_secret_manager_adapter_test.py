import pytest
from unittest.mock import MagicMock, patch
import json
from botocore.exceptions import ClientError
from src.infraestructure.driven_adapters.secret_repository.adapter.secret_manager_adapter import SecretManagerService
from src.applications.settings.settings import AWSSecrets
from src.applications.settings.logger import Logger
from src.infraestructure.driven_adapters.secret_repository.errors.secret_manager_errors import SecretManagerError


@pytest.fixture
def mock_aws_config():
    """Fixture to provide a mock AWSSecrets instance."""
    mock_config = MagicMock(spec=AWSSecrets)
    mock_config.model_dump.return_value = {"region_name": "us-east-1"}
    return mock_config

@pytest.fixture
def mock_logger():
    """Fixture to provide a mock Logger instance."""
    mock_log = MagicMock(spec=Logger)
    return mock_log

@pytest.fixture
def mock_boto3_client():
    """
    Fixture to mock boto3.client for 'secretsmanager'.
    It will return a mock client with a mock get_secret_value method.
    """
    with patch("boto3.client") as mock_client_factory:
        mock_secretsmanager_client = MagicMock()
        mock_client_factory.return_value = mock_secretsmanager_client
        yield mock_secretsmanager_client # Yield the mock client instance

@pytest.fixture
def secret_manager_service(mock_aws_config, mock_logger, mock_boto3_client):
    """
    Fixture to create an instance of SecretManagerService with mocked dependencies.
    The mock_boto3_client is already yielded from its fixture, so it's available here.
    """
    # The mock_boto3_client fixture already handles patching boto3.client,
    # so SecretManagerService will receive the mock when instantiated.
    service = SecretManagerService(aws_config=mock_aws_config, logger=mock_logger)
    return service


def test_get_secret_success_with_secret_string(secret_manager_service, mock_boto3_client, mock_logger):
    """
    Tests successful retrieval of a secret when SecretString is present and valid JSON.
    """
    secret_name = "test/secret/name"
    mock_secret_string_value = {"api_key": "12345", "db_url": "mock_db_url"}
    mock_boto3_client.get_secret_value.return_value = {
        "SecretString": json.dumps(mock_secret_string_value)
    }

    result = secret_manager_service.get_secret(secret_name)

    mock_boto3_client.get_secret_value.assert_called_once_with(SecretId=secret_name)
    mock_logger.debug.assert_called_once() # Check that debug was called
    assert result == mock_secret_string_value

def test_get_secret_simple_success(secret_manager_service, mock_boto3_client):
    """
    A simple test for successful secret retrieval.
    """
    secret_name = "my_simple_secret"
    expected_secret = {"user": "testuser", "pass": "testpass"}
    mock_boto3_client.get_secret_value.return_value = {
        "SecretString": json.dumps(expected_secret)
    }

    result = secret_manager_service.get_secret(secret_name)
    assert result == expected_secret
    mock_boto3_client.get_secret_value.assert_called_once_with(SecretId=secret_name)