import asyncio
import json
from json.decoder import JSONDecodeError

import boto3
from botocore.exceptions import ClientError

from src.domain.model.output_aio.gateway.output_aio_gateway import \
    QueueNotifier
from src.domain.model.output_aio.output_aio_model import Message
from src.infraestructure.driven_adapters.sqs_repository.error.\
    sqs_repository_error import (
        SqsRepositoryError,
    )


class SqsRepository(QueueNotifier):
    """Implementation of AWS SQS client for sending messages to queues."""

    def __init__(self, config, logger):
        """Initialize SQS repository with configuration and logger.

        Args:
            config: Application configuration with AWS credentials and queue
            URL.
            logger: Logger instance for recording messaging operations.
        """
        self.sqs_client = boto3.client(
            "sqs", **config.aws.model_dump())
        self.logger = logger
        self.queue_url = config.queue_url

    async def send_result(self, message: Message) -> bool:
        """Send a message to the configured SQS queue.

        Args:
            message: Message object containing the data to be sent.

        Returns:
            None

        Raises:
            SqsRepositoryError: If sending the message fails.
        """
        self.logger.info(f"Sending message to sqs {message.request_id}")
        mes = json.dumps(message.model_dump())
        try:
            await asyncio.to_thread(
                self.sqs_client.send_message,
                QueueUrl=self.queue_url,
                MessageBody=mes,
                MessageGroupId=message.request_id
            )
            return True
        except (ClientError, KeyError, TypeError, JSONDecodeError) as error:
            msg = f"[SqsAdapter][notify] Details: {str(error)}"
            raise SqsRepositoryError(message=str(msg)) from error
