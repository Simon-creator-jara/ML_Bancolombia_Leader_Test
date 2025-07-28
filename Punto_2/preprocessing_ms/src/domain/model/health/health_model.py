from pydantic import BaseModel


class HealthResponse(BaseModel):
    """health response model."""

    check_state: bool
    message: str
    date: str
