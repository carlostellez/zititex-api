"""
Main FastAPI application.

This module creates and configures the FastAPI application with
all necessary middleware, CORS, and route registration.
"""

from contextlib import asynccontextmanager
from typing import Any

from fastapi import FastAPI, Request
from fastapi.middleware.cors import CORSMiddleware
from fastapi.responses import JSONResponse
from mangum import Mangum
from app.api.v1 import contact
from app.core.config import settings


@asynccontextmanager
async def lifespan(app: FastAPI) -> Any:
    """
    Application lifespan manager.

    Handles startup and shutdown events for the application,
    including database table creation in development mode.
    """
    # Startup
    print("🚀 Starting Zititex API...")

    # Import models to ensure they're registered with SQLAlchemy
    from app.models import Client  # noqa: F401

    # Create database tables in development mode
    if settings.debug:
        print("🔧 Debug mode: Creating database tables if they don't exist...")
        from app.core.database import create_tables

        try:
            await create_tables()
            print("✅ Database tables ready")
        except Exception as e:
            print(f"⚠️ Warning: Could not create tables: {e}")
            print("   This is normal if database is not configured yet")

    print("✅ Application started successfully")

    yield

    # Shutdown
    print("👋 Shutting down Zititex API...")
    print("✅ Application shutdown complete")


def create_app() -> FastAPI:
    """
    Create and configure the FastAPI application.

    Returns:
        Configured FastAPI application instance with middleware,
        CORS, exception handlers, and API routes.
    """
    app = FastAPI(
        title=settings.app_name,
        version=settings.app_version,
        description="FastAPI-based REST API for Zititex application with MySQL integration",
        docs_url="/docs",  # Siempre habilitado
        redoc_url="/redoc",  # Siempre habilitado
        lifespan=lifespan,
    )

    # Add CORS middleware
    app.add_middleware(
        CORSMiddleware,
        allow_origins=settings.allowed_origins,
        allow_credentials=True,
        allow_methods=settings.allowed_methods,
        allow_headers=settings.allowed_headers,
    )

    # Add no-cache middleware
    @app.middleware("http")
    async def add_no_cache_headers(request: Request, call_next):
        """Add headers to prevent caching."""
        response = await call_next(request)
        response.headers["Cache-Control"] = "no-cache, no-store, must-revalidate"
        response.headers["Pragma"] = "no-cache"
        response.headers["Expires"] = "0"
        return response

    # Global exception handler
    @app.exception_handler(Exception)
    async def global_exception_handler(
        request: Request, exc: Exception
    ) -> JSONResponse:
        """Global exception handler."""
        print(f"❌ Global exception handler caught: {exc}")
        print(f"❌ Exception type: {type(exc).__name__}")
        import traceback

        print(f"❌ Traceback: {traceback.format_exc()}")

        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": "Internal server error",
                "detail": str(exc)
                if settings.debug
                else "An unexpected error occurred",
            },
        )

    # Include API routes
    app.include_router(contact.router, prefix="/api/v1")

    # Health check endpoint
    @app.get("/health")
    async def health_check() -> dict[str, Any]:
        """Health check endpoint."""
        return {
            "status": "healthy",
            "service": settings.app_name,
            "version": settings.app_version,
        }

    # Root endpoint
    @app.get("/")
    async def root() -> dict[str, Any]:
        """Root endpoint."""
        return {
            "message": f"Welcome to {settings.app_name}",
            "version": settings.app_version,
            "docs": "/docs",
            "redoc": "/redoc",
        }

    return app


# Create the application instance
app = create_app()

# Create Mangum handler for AWS Lambda
handler = Mangum(app, lifespan="off")
