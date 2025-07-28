import re
import ftfy
import pandas as pd
from src.domain.model.dataset.gateway.dataset_gateway import (
    DatasetCleaner,
)
from src.domain.model.dataset.dataset_model import (
    RawDataset,
)
from src.domain.model.message_error.message_error_model import MessageError
from src.domain.model.message_error.gateways.message_error_repository import (
    MessageErrorRepository,
)


class DatasetCleanerImpl(DatasetCleaner):
    """Dataset cleaner implementation."""

    def __init__(self, logger, sns_notifier: MessageErrorRepository):
        self.logger = logger
        self.sns_notifier = sns_notifier

    async def process(self, inputs: RawDataset) -> pd.DataFrame:
        """Cleans title and plot text fields and adds text_to_embed column."""
        self.logger.info(f"Reading dataset from {inputs.file_path}")
        try:
            df = pd.read_csv(inputs.file_path)
            df = self._clean_text(df, 'title')
            df = self._clean_text(df, 'plot')
            df["text_to_embed"] = df["title"].str.strip() + " " + \
                df["plot"].str.strip()
            return df
        except Exception as error:
            self.logger.error(f"Error reading file: {error}")
            error_message = f"Error Details: {error}"
            subject_message = ("Error executing DataCleaner")
            message_error = MessageError(subject_message=subject_message,
                                         content_message=error_message)
            await self.sns_notifier.send(message_error)
            raise

    def _clean_text(self, df: pd.DataFrame, text_field: str) -> pd.DataFrame:
        patternURLEMAIL = r'(\w+[.]?\w+@(\w+\.)+\w+)|((http:\/\/www\.|https:\/\/www\.|http:\/\/|https:\/\/)?\w+([\-\.]{1}\w+)*\.[a-z]{2,5}(\/)?(([^\s@])*(\/)?)*)'
        patternHashtagMention = r'(@\\w+)|(#\\w+)'

        df[text_field] = df[text_field].apply(lambda x: str(x))
        df[text_field] = df[text_field].apply(lambda x: re.sub(r"\'", '', x))
        df[text_field] = df[text_field].apply(lambda x: re.sub(r"\*", ' ', x))
        df[text_field] = df[text_field].apply(lambda x: re.sub(r"\|", ' ', x))
        df[text_field] = df[text_field].apply(
            lambda x: re.sub(r"\s*\([^)]*\)", '', x))
        df[text_field] = df[text_field].apply(
            lambda x: re.sub(patternURLEMAIL, '', x))
        df[text_field] = df[text_field].apply(
            lambda x: re.sub(patternHashtagMention, '', x))
        df[text_field] = df[text_field].apply(
            lambda x: re.sub(r'(\&gt\;)|(\&lt\;)', '', x))
        df[text_field] = df[text_field].apply(
            lambda x: re.sub(r'(a\.m)|(p\.m)', '', x))
        df[text_field] = df[text_field].apply(lambda x: re.sub(r'[|]', '', x))
        df[text_field] = df[text_field].apply(lambda x: re.sub(r'-', ' ', x))
        df[text_field] = df[text_field].apply(
            lambda x: re.sub(r"\{\{[^{}]*\}\}", '', x))
        df[text_field] = df[text_field].apply(
            lambda x: re.sub(r"<ref[^>]*?>.*?</ref>", '', x))
        df[text_field] = df[text_field].apply(
            lambda x: re.sub(r"<ref[^/]*/>", '', x))
        df[text_field] = df[text_field].apply(
            lambda x: re.sub(r"<[^>]+>", '', x))
        df[text_field] = df[text_field].apply(
            lambda x: re.sub(r"\[\[(File|Image):.*?\]\]", '', x))
        df[text_field] = df[text_field].apply(lambda x: re.sub(r'\s+', ' ', x))
        df[text_field] = df[text_field].apply(lambda x: ftfy.fix_text(x))
        return df
