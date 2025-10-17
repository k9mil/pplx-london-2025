"""
Pydantic models for request/response validation
"""
from pydantic import BaseModel, Field
from typing import Optional, List, Any
from datetime import datetime


class FileUploadResponse(BaseModel):
    """Response model for file upload"""
    filename: str
    original_filename: str
    size: int
    width: int
    height: int
    format: str
    content_type: str
    storage: str
    public_url: Optional[str] = None
    path: Optional[str] = None
    bucket: Optional[str] = None
    blob_name: Optional[str] = None
    created_at: Optional[str] = None


class APIResponse(BaseModel):
    """Generic API response wrapper"""
    success: bool
    message: str
    data: Optional[Any] = None


class HealthCheckResponse(BaseModel):
    """Health check response"""
    status: str
    timestamp: str


class FileListResponse(BaseModel):
    """Response for file listing"""
    success: bool
    storage: str
    count: int
    files: List[dict]


class ProcessImageResponse(BaseModel):
    """Response for image processing"""
    success: bool
    message: str
    data: dict

