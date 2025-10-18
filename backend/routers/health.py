"""
Health check and info endpoints
"""
from fastapi import APIRouter
from datetime import datetime
from config import settings

router = APIRouter(tags=["health"])


@router.get("/")
async def root():
    """Root endpoint with API information"""
    return {
        "message": f"Welcome to {settings.APP_TITLE}",
        "version": settings.APP_VERSION,
        "storage": "GCS" if settings.USE_GCS else "Local",
        "endpoints": {
            "health": "/health",
            "upload": "/api/upload",
            "upload_multiple": "/api/upload/multiple",
            "list_uploads": "/api/uploads",
            "process": "/api/process",
            "docs": "/docs"
        }
    }


@router.get("/health")
async def health_check():
    """Health check endpoint"""
    return {
        "status": "healthy",
        "timestamp": datetime.now().isoformat(),
        "storage": "gcs" if settings.USE_GCS else "local"
    }

