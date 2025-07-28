from src.domain.model.health.health_model import HealthResponse
from src.domain.usecase import CheckHealthUseCase


class HealthHandler:
    """Health check use case."""

    def __init__(self, usecase: CheckHealthUseCase):
        self.usecase = usecase

    async def check(self) -> HealthResponse:
        """Check health."""
        return await self.usecase.check()
