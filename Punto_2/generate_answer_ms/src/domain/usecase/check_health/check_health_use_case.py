from datetime import datetime
from src.applications.settings.settings import Config
from src.domain.model.health.health_model import HealthResponse


class CheckHealthUseCase:
    """Health check use case."""

    def __init__(self, config: Config, logger):
        self.config = config
        self.logger = logger

    @staticmethod
    async def check() -> HealthResponse:
        """Check health."""
        timestamp = str(datetime.now().isoformat())
        result = {"check_state": True, "message": "ALIVE", "date": timestamp}
        return HealthResponse(**result)
