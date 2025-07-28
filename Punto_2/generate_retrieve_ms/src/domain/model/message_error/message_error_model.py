"Message error model definition."
from pydantic import BaseModel


class MessageError(BaseModel):
    """
    Message model.

    Attributes:
        subject_message (str): The subject of the message.
        content_messagge (str): The content of the message.
    """
    subject_message: str
    content_message: str
