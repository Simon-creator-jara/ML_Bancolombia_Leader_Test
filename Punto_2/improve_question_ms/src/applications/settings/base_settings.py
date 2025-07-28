from pydantic import BaseModel, ConfigDict
from pydantic_settings import BaseSettings, SettingsConfigDict


class GeneralBaseSettings(BaseSettings):
    """Base settings for all applications."""
    model_config = SettingsConfigDict(
        case_sensitive=True,
        extra="ignore",
        arbitrary_types_allowed=True,
    )


class GeneralBaseModel(BaseModel):
    """Base model for all applications."""
    model_config = ConfigDict(extra="ignore", arbitrary_types_allowed=True)
