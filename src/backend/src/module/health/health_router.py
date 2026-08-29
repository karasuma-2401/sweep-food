from typing import Annotated

from fastapi import APIRouter, Depends, status
from fastapi.responses import PlainTextResponse

from src.module.health.health_dependency import get_health_service
from src.module.health.health_dto import LivenessResponseDTO
from src.module.health.health_service import HealthService

health_router = APIRouter(prefix="/health", tags=["health"])


@health_router.get("/liveness", response_model=LivenessResponseDTO)
async def get_liveness(
    service: Annotated[HealthService, Depends(get_health_service)],
) -> LivenessResponseDTO:
    return service.get_liveness()


@health_router.get("/error")
async def get_error(
    service: Annotated[HealthService, Depends(get_health_service)],
) -> None:

    service.raise_forced_error()


@health_router.get(
    "/text",
    response_class=PlainTextResponse,
    status_code=status.HTTP_200_OK,
)
async def get_text(
    service: Annotated[HealthService, Depends(get_health_service)],
) -> PlainTextResponse:
    return PlainTextResponse(content=service.get_text())
