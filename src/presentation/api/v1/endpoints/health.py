"""Health check endpoints."""

from fastapi import APIRouter
from pydantic import BaseModel

router = APIRouter()


class HealthResponse(BaseModel):
    """Health check response schema."""

    status: str
    message: str


@router.get("/", response_model=HealthResponse)
async def health_check() -> HealthResponse:
    """
    Health check endpoint.

    Returns:
        HealthResponse: Health status.
    """
    return HealthResponse(status="ok", message="Service is healthy")


@router.get("/liveness", response_model=HealthResponse)
async def liveness() -> HealthResponse:
    """
    Liveness probe endpoint.

    Returns:
        HealthResponse: Liveness status.
    """
    return HealthResponse(status="ok", message="Service is alive")


@router.get("/readiness", response_model=HealthResponse)
async def readiness() -> HealthResponse:
    """
    Readiness probe endpoint.

    Returns:
        HealthResponse: Readiness status.
    """
    return HealthResponse(status="ok", message="Service is ready")

