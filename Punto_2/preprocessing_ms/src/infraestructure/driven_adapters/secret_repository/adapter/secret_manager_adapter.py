import json
from json.decoder import JSONDecodeError
from typing import Any, Dict
import boto3
from botocore.exceptions import ClientError
from src.applications.settings.logger import Logger
from src.applications.settings.settings import AWSSecrets
from src.infraestructure.driven_adapters.secret_repository.errors.\
    secret_manager_errors import SecretManagerError


class SecretManagerService():
    """Class to invoke secret manager service."""

    def __init__(self, aws_config: AWSSecrets, logger: Logger):
        self.logger = logger
        self.client = boto3.client(
            "secretsmanager",
            **aws_config.model_dump()
        )

    def get_secret(self, secret_name: str) -> Dict[str, Any]:
        try:
            response = self.client.get_secret_value(SecretId=secret_name)
            self.logger.debug(f"get secret: {response} - {secret_name}")
            if response.get("SecretString"):
                return json.loads(response.get("SecretString"))
            return {}
        except (ClientError, KeyError, TypeError, JSONDecodeError) as error:
            msg = f"[SecretManagerService][get_secret] Details: {str(error)}"
            self.logger.error(msg)
            raise SecretManagerError(msg) from error
