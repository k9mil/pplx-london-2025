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


class ImageToTextRequest(BaseModel):
    """Request for image-to-text conversion"""
    blob_name: Optional[str] = Field(None, description="GCS blob name/path of the image")
    image_url: Optional[str] = Field(None, description="Public URL of the image")
    prompt: Optional[str] = Field(
        None, 
        description="Custom prompt for image description (optional)"
    )
    detail_level: Optional[str] = Field(
        "high",
        description="Level of detail: 'low', 'medium', or 'high'"
    )


class ImageToTextResponse(BaseModel):
    """Response for image-to-text conversion"""
    success: bool
    message: str
    description: Optional[str] = None
    image_info: Optional[dict] = None

