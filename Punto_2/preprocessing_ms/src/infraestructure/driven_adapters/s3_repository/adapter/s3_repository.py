import json
from typing import Dict
import boto3
from botocore.exceptions import (BotoCoreError, ClientError,
                                 NoCredentialsError, NoRegionError,
                                 ParamValidationError)

from src.domain.model.repository.gateway.repository_gateway import \
    OCRRepositoryGateway
from src.infraestructure.driven_adapters.s3_repository.error \
    .s3_repository_error import S3RepositoryError


class S3OCRRepository(OCRRepositoryGateway):
    """AWS S3-based implementation of the OCR repository for file
    operations."""

    def __init__(self, config, logger):
        """Initialize S3 repository with configuration and logger.

        Args:
            config: Application configuration with AWS credentials.
            logger: Logger instance for recording repository operations.
        """
        self.s3_client = boto3.client('s3', **config.aws.model_dump())
        self.logger = logger

    def get_json(self, s3_path: str) -> Dict:
        """Download and parse a JSON file from S3.

        Args:
            s3_path: S3 path in format 's3://bucket-name/path/to/file.json'.

        Returns:
            Dict: Parsed JSON content as a dictionary.

        Raises:
            S3RepositoryError: If downloading or parsing fails.
        """
        self.logger.info(f"Downloading file from {s3_path}")
        try:
            bucket, key = self._split_s3_path(s3_path)
            response = self.s3_client.get_object(Bucket=bucket, Key=key)
            content = response["Body"].read().decode("utf-8")
            return json.loads(content)
        except (
            ClientError, ParamValidationError, BotoCoreError,
            NoRegionError, NoCredentialsError
        ) as error:
            msg_error = f"""Download Exception: Failed on
                [S3Repository][download] while download files.
                Error Details: {error}"""
            self.logger.error(msg_error)
            raise S3RepositoryError(message=str(msg_error)) from error

    def save_json(self, bucket: str, key: str, data: Dict) -> str:
        """Save dictionary data as a JSON file to S3.

        Args:
            bucket: S3 bucket name.
            key: Object key (path) within the bucket.
            data: Dictionary data to be saved as JSON.

        Returns:
            str: S3 path to the saved file in format 's3://bucket-name/key'.

        Raises:
            S3RepositoryError: If saving fails.
        """
        self.logger.info(f"Uploading file to {bucket}/{key}")
        try:
            self.s3_client.put_object(
                Bucket=bucket,
                Key=key,
                Body=json.dumps(
                    data, indent=2, ensure_ascii=False).encode("utf-8"),
                ContentType="application/json"
            )
            return f"s3://{bucket}/{key}"
        except (
            ClientError, ParamValidationError, BotoCoreError,
            NoRegionError, NoCredentialsError
        ) as error:
            msg_error = f"""Uploading Exception: Failed on
                [S3Repository][download] while upload files.
                Error Details: {error}"""
            self.logger.error(msg_error)
            raise S3RepositoryError(message=str(msg_error)) from error

    def _split_s3_path(self, s3_path: str):
        """Split S3 path into bucket name and key.

        Args:
            s3_path: S3 path in format 's3://bucket-name/path/to/file'.

        Returns:
            tuple: (bucket_name, key) pair.
        """
        path = s3_path.replace("s3://", "")
        bucket, key = path.split("/", 1)
        return bucket, key
