"""
Upload endpoints for handling image uploads
"""
from fastapi import APIRouter, File, UploadFile, HTTPException, Body
from fastapi.responses import JSONResponse
from typing import List
from PIL import Image
import io
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

from config import settings
from gcs_storage import get_storage_client, GCSStorage
from schemas import APIResponse, FileListResponse, ImageToTextRequest, ImageToTextResponse
from pathlib import Path
from datetime import datetime

router = APIRouter(prefix="/api", tags=["uploads"])

# Initialize GCS storage client
gcs_storage = get_storage_client()

# Initialize Vertex AI
vertex_ai_initialized = False
if settings.VERTEX_AI_PROJECT:
    try:
        vertexai.init(
            project=settings.VERTEX_AI_PROJECT,
            location=settings.VERTEX_AI_LOCATION
        )
        vertex_ai_initialized = True
    except Exception as e:
        print(f"Warning: Vertex AI initialization failed: {e}")


def validate_image(file: UploadFile) -> None:
    """Validate uploaded image file"""
    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}"
        )


async def save_upload_file(upload_file: UploadFile) -> dict:
    """Save uploaded file to GCS or local storage and return file info"""
    try:
        # Read file content
        contents = await upload_file.read()
        
        # Validate file size
        if len(contents) > settings.MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE_MB}MB"
            )
        
        # Validate it's a valid image
        try:
            image = Image.open(io.BytesIO(contents))
            width, height = image.size
            format_type = image.format
        except Exception as e:
            raise HTTPException(status_code=400, detail="Invalid image file")
        
        # Upload to GCS if configured
        if settings.USE_GCS and gcs_storage:
            try:
                file_info = gcs_storage.upload_image(
                    file_data=contents,
                    filename=upload_file.filename,
                    content_type=upload_file.content_type or "image/jpeg",
                    make_public=True
                )
                file_info["storage"] = "gcs"
                return file_info
            except Exception as e:
                raise HTTPException(
                    status_code=500,
                    detail=f"Error uploading to GCS: {str(e)}"
                )
        
        # Fallback to local storage
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S")
        filename = f"{timestamp}_{upload_file.filename}"
        file_path = settings.UPLOAD_DIR / filename
        
        with open(file_path, "wb") as f:
            f.write(contents)
        
        return {
            "filename": filename,
            "original_filename": upload_file.filename,
            "path": str(file_path),
            "storage": "local",
            "size": len(contents),
            "width": width,
            "height": height,
            "format": format_type,
            "content_type": upload_file.content_type
        }
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    """
    Upload a single image file
    
    - **file**: Image file (jpg, jpeg, png, gif, webp)
    
    Returns file information including path, size, and dimensions
    """
    try:
        # Validate image
        validate_image(file)
        
        # Save file and get info
        file_info = await save_upload_file(file)
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "File uploaded successfully",
                "data": file_info
            }
        )
    
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "success": False,
                "message": e.detail
            }
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={
                "success": False,
                "message": f"Internal server error: {str(e)}"
            }
        )


@router.post("/upload/multiple")
async def upload_multiple_images(files: List[UploadFile] = File(...)):
    """
    Upload multiple image files
    
    - **files**: List of image files (jpg, jpeg, png, gif, webp)
    
    Returns information for all uploaded files
    """
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")
    
    if len(files) > settings.MAX_FILES_PER_UPLOAD:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum {settings.MAX_FILES_PER_UPLOAD} files allowed"
        )
    
    uploaded_files = []
    errors = []
    
    for file in files:
        try:
            validate_image(file)
            file_info = await save_upload_file(file)
            uploaded_files.append(file_info)
        except Exception as e:
            errors.append({
                "filename": file.filename,
                "error": str(e)
            })
    
    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": f"Uploaded {len(uploaded_files)} file(s)",
            "data": {
                "uploaded": uploaded_files,
                "errors": errors
            }
        }
    )


@router.get("/uploads")
async def list_uploads(limit: int = 100):
    """List uploaded files"""
    try:
        if settings.USE_GCS and gcs_storage:
            files = gcs_storage.list_files(max_results=limit)
            return {
                "success": True,
                "storage": "gcs",
                "count": len(files),
                "files": files
            }
        else:
            # List local files
            if not settings.UPLOAD_DIR.exists():
                return {"success": True, "storage": "local", "count": 0, "files": []}
            
            files = []
            for file_path in settings.UPLOAD_DIR.glob("*"):
                if file_path.is_file():
                    files.append({
                        "name": file_path.name,
                        "size": file_path.stat().st_size,
                        "path": str(file_path)
                    })
            
            return {
                "success": True,
                "storage": "local",
                "count": len(files),
                "files": files[:limit]
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")


@router.delete("/uploads/{blob_name:path}")
async def delete_upload(blob_name: str):
    """Delete an uploaded file from GCS or local storage"""
    try:
        if settings.USE_GCS and gcs_storage:
            # Delete from GCS
            gcs_storage.delete_file(blob_name)
            return {
                "success": True,
                "message": f"File {blob_name} deleted from GCS"
            }
        else:
            # Delete from local storage
            file_path = settings.UPLOAD_DIR / blob_name
            
            if not file_path.exists():
                raise HTTPException(status_code=404, detail="File not found")
            
            import os
            os.remove(file_path)
            return {
                "success": True,
                "message": f"File {blob_name} deleted from local storage"
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")


@router.post("/process")
async def process_image(file: UploadFile = File(...)):
    """
    Process uploaded image and extract information
    
    This endpoint will be extended to integrate with AI services
    for image analysis and product matching
    """
    try:
        # Validate and save image
        validate_image(file)
        file_info = await save_upload_file(file)
        
        # TODO: Add AI processing logic here
        # - Image analysis
        # - Object detection
        # - Style extraction
        # - Product matching
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Image processed successfully",
                "data": {
                    "file": file_info,
                    "analysis": {
                        "status": "pending",
                        "message": "AI processing will be implemented here"
                    }
                }
            }
        )
    
    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code,
            content={
                "success": False,
                "message": e.detail
            }
        )


@router.post("/image-to-text", response_model=ImageToTextResponse)
async def image_to_text(request: ImageToTextRequest = Body(...)):
    """
    Convert an image to detailed text description using Google's Gemini Vision model.
    
    This endpoint is designed for integration with ElevenLabs agent or other 
    services that need text descriptions of images instead of direct image URLs.
    
    - **blob_name**: GCS blob path (e.g., "uploads/20241017_123456_image.jpg")
    - **image_url**: Public URL of the image (alternative to blob_name)
    - **prompt**: Optional custom prompt for specific description requirements
    - **detail_level**: low, medium, or high (default: high)
    
    Returns a detailed text description of the image content.
    """
    try:
        # Validate Vertex AI is configured
        if not vertex_ai_initialized:
            raise HTTPException(
                status_code=503,
                detail="Image-to-text service not configured. Vertex AI initialization failed."
            )
        
        # Validate request has either blob_name or image_url
        if not request.blob_name and not request.image_url:
            raise HTTPException(
                status_code=400,
                detail="Either 'blob_name' or 'image_url' must be provided"
            )
        
        # Get image data
        image_data = None
        image_info = {}
        gcs_uri = None
        
        if request.blob_name:
            # Use GCS URI directly for better performance
            if not settings.USE_GCS or not gcs_storage:
                raise HTTPException(
                    status_code=400,
                    detail="GCS storage not configured. Cannot retrieve image by blob_name."
                )
            
            # Check if file exists
            if not gcs_storage.file_exists(request.blob_name):
                raise HTTPException(
                    status_code=404,
                    detail=f"Image not found in bucket: {request.blob_name}"
                )
            
            # Build GCS URI
            gcs_uri = f"gs://{settings.GCS_BUCKET_NAME}/{request.blob_name}"
            
            # Get image metadata
            blob = gcs_storage.bucket.blob(request.blob_name)
            blob.reload()
            image_info = {
                "blob_name": request.blob_name,
                "bucket": settings.GCS_BUCKET_NAME,
                "size": blob.size,
                "content_type": blob.content_type,
                "created": blob.time_created.isoformat() if blob.time_created else None
            }
        elif request.image_url:
            # For external URLs, we'll need to download the image
            import requests
            response = requests.get(request.image_url, timeout=30)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to download image from URL: {response.status_code}"
                )
            image_data = response.content
            image_info = {"image_url": request.image_url}
        
        # Prepare the prompt
        default_prompt = (
            "Please provide a detailed, comprehensive description of this image. "
            "Include information about: the main subjects or objects, their colors, "
            "textures, materials, style, positioning, lighting, mood, and any other "
            "relevant visual details. Be thorough and descriptive as if explaining "
            "the image to someone who cannot see it."
        )
        
        if request.detail_level == "low":
            default_prompt = "Provide a brief description of this image in 2-3 sentences."
        elif request.detail_level == "medium":
            default_prompt = (
                "Provide a moderate description of this image, covering the main "
                "subjects, colors, and composition in a paragraph."
            )
        
        final_prompt = request.prompt if request.prompt else default_prompt
        
        # Initialize Gemini model
        model = GenerativeModel(settings.GEMINI_MODEL)
        
        # Prepare image part
        if gcs_uri:
            # Use GCS URI directly
            image_part = Part.from_uri(gcs_uri, mime_type="image/jpeg")
        else:
            # Use image data
            image_part = Part.from_data(image_data, mime_type="image/jpeg")
        
        # Generate content
        response = model.generate_content([final_prompt, image_part])
        
        # Extract description
        description = response.text
        
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Image successfully converted to text using Gemini Vision",
                "description": description,
                "image_info": image_info
            }
        )
    
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500,
            detail=f"Error processing image to text: {str(e)}"
        )

