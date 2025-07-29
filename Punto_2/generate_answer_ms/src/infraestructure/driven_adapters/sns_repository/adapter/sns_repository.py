"""This module contains the implementation of the SnsRepository class"""
import asyncio
import boto3
from botocore.exceptions import (
    ClientError,
    ParamValidationError,
    BotoCoreError,
    NoRegionError,
    NoCredentialsError,
)
from src.domain.model import MessageErrorRepository
from src.domain.model.message_error.message_error_model import MessageError
from src.infraestructure.driven_adapters.sns_repository.error\
    .sns_repository_error import SnsRepositoryError


class SnsRepository(MessageErrorRepository):
    """Sns repository class."""

    def __init__(self, config, logger):
        self.sns_client = boto3.client(
            "sns", **config.aws.model_dump())
        self.logger = logger
        self.sns_arn = config.sns_error_arn

    async def send(self, message: MessageError):
        """Send message."""
        self.logger.info(f"Sending message to SNS topic with {message}")
        try:
            response = await asyncio.to_thread(
                self.sns_client.publish,
                TargetArn=self.sns_arn,
                Subject=message.subject_message,
                Message=message.content_message,
            )

            self.logger.info(f"Published the message to SNS topic. {response}")
            return response
        except (ClientError, ParamValidationError, BotoCoreError,
                NoRegionError, NoCredentialsError) as error:
            msg_exception = f"""SNS Exception: Failed on
                [SnsRepository][send] while send a message.
                Error Details: {error}"""
            self.logger.error("ERROR: " + str(error))
            self.logger.info(msg_exception)
            raise SnsRepositoryError(message=str(msg_exception)) from error
