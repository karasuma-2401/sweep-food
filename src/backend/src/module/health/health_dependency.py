from src.module.health.health_service import HealthService


def get_health_service() -> HealthService:
    return HealthService()
