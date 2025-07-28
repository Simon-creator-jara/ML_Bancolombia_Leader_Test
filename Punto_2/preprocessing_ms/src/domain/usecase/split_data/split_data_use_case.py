from typing import List
import pandas as pd
from src.domain.model.chunks.gateway.chunks_gateway import Splitter
from src.domain.model.message_error.message_error_model import MessageError
from src.domain.model.message_error.gateways.message_error_repository import (
    MessageErrorRepository,
)


class SplitterImpl(Splitter):
    """Concrete splitter implementation."""

    def __init__(self, logger, sns_notifier: MessageErrorRepository):
        self.logger = logger
        self.sns_notifier = sns_notifier

    async def split(self, df: pd.DataFrame, chunk_size: int) -> List[pd.DataFrame]:
        try:
            return [df[i:i + chunk_size] for i in range(0, len(df), chunk_size)]
        except Exception as error:
            self.logger.error(f"Error splitting file: {error}")
            error_message = f"Error Details: {error}"
            subject_message = ("Error executing Splitter")
            message_error = MessageError(subject_message=subject_message,
                                         content_message=error_message)
            await self.sns_notifier.send(message_error)
            raise
