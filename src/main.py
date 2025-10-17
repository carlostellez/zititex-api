"""Main application entry point."""

from contextlib import asynccontextmanager
from typing import AsyncGenerator

from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse

from src.infrastructure.config.settings import get_settings
from src.presentation.api.v1.router import api_router


@asynccontextmanager
async def lifespan(app: FastAPI) -> AsyncGenerator[None, None]:
    """Application lifespan events."""
    # Startup
    print("🚀 Starting Zititex API...")
    yield
    # Shutdown
    print("👋 Shutting down Zititex API...")


def create_application() -> FastAPI:
    """Create and configure FastAPI application."""
    settings = get_settings()

    application = FastAPI(
        title=settings.APP_NAME,
        description="Zititex API - Clean Architecture REST API",
        version=settings.API_VERSION,
        docs_url=f"/{settings.API_VERSION}/docs",
        redoc_url=f"/{settings.API_VERSION}/redoc",
        openapi_url=f"/{settings.API_VERSION}/openapi.json",
        lifespan=lifespan,
    )

    # Configure CORS
    application.add_middleware(
        CORSMiddleware,
        allow_origins=settings.CORS_ORIGINS,
        allow_credentials=settings.CORS_ALLOW_CREDENTIALS,
        allow_methods=settings.CORS_ALLOW_METHODS,
        allow_headers=settings.CORS_ALLOW_HEADERS,
    )

    # Include routers
    application.include_router(api_router, prefix=f"/{settings.API_VERSION}")

    # Health check endpoint
    @application.get("/health")
    async def health_check() -> JSONResponse:
        """Health check endpoint."""
        return JSONResponse(
            content={"status": "healthy", "version": settings.API_VERSION}
        )

    return application


app = create_application()

