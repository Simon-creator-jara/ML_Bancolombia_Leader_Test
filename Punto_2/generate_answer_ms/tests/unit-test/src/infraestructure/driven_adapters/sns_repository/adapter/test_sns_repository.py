from unittest.mock import MagicMock

import pytest
from botocore.exceptions import ClientError

from src.domain.model.message_error.message_error_model import MessageError
from src.infraestructure.driven_adapters.sns_repository.error.\
    sns_repository_error import SnsRepositoryError


@pytest.mark.asyncio
async def test_send_success(sns_repository):
    """Test successful message publication to SNS.

    Verifies that the SNS repository correctly:
    - Publishes the message to SNS
    - Returns the expected MessageId from the response
    - Logs the successful operation
    """
    sns_repository.sns_client.publish = MagicMock(
        return_value={"MessageId": "test-message-id"}
    )
    message = MessageError(
        subject_message="Test Subject",
        content_message="Test Content"
    )

    result = await sns_repository.send(message)

    assert result["MessageId"] == "test-message-id"
    sns_repository.logger.info.assert_called()


@pytest.mark.asyncio
async def test_send_failures(sns_repository):
    """Test error handling when SNS publication fails.

    Verifies that the SNS repository correctly:
    - Handles ClientError from the AWS SDK
    - Logs the error appropriately
    - Raises a custom SnsRepositoryError
    """
    sns_repository.sns_client.publish.side_effect = ClientError(
        error_response={"Error": {"Code": "InternalError",
                                  "Message": "Something went wrong"}},
        operation_name="Publish"
    )
    message = MessageError(
        subject_message="Test Subject",
        content_message="Test Content"
    )

    with pytest.raises(SnsRepositoryError):
        await sns_repository.send(message)

    sns_repository.logger.error.assert_called()
    sns_repository.logger.info.assert_called()
