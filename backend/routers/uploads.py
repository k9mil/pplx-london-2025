from fastapi import APIRouter, File, UploadFile, HTTPException, Body
from fastapi.responses import JSONResponse
from typing import List, Optional, Dict, Any
from PIL import Image
import io
import vertexai
from vertexai.preview.generative_models import GenerativeModel, Part

from config import settings
from gcs_storage import get_storage_client
from schemas import ImageToTextRequest, ImageToTextResponse
from pathlib import Path
from datetime import datetime
import os

from api.services.image_merger import ImageMerger

router = APIRouter(prefix="/api", tags=["uploads"])

gcs_storage = get_storage_client()

vertex_ai_initialized = False
if settings.VERTEX_AI_PROJECT:
    try:
        from google.oauth2 import service_account as sa

        if settings.GCS_CREDENTIALS_PATH and os.path.exists(
            settings.GCS_CREDENTIALS_PATH
        ):
            credentials = sa.Credentials.from_service_account_file(
                settings.GCS_CREDENTIALS_PATH
            )
            vertexai.init(
                project=settings.VERTEX_AI_PROJECT,
                location=settings.VERTEX_AI_LOCATION,
                credentials=credentials,
            )
        else:
            vertexai.init(
                project=settings.VERTEX_AI_PROJECT, location=settings.VERTEX_AI_LOCATION
            )
        vertex_ai_initialized = True
    except Exception as e:
        print(f"Warning: Vertex AI initialization failed: {e}")


def validate_image(file: UploadFile) -> None:
    if not file.filename:
        raise HTTPException(status_code=400, detail="Filename is required")

    file_ext = Path(file.filename).suffix.lower()
    if file_ext not in settings.ALLOWED_EXTENSIONS:
        raise HTTPException(
            status_code=400,
            detail=f"Invalid file type. Allowed types: {', '.join(settings.ALLOWED_EXTENSIONS)}",
        )


async def save_upload_file(upload_file: UploadFile) -> dict:
    try:
        if not upload_file.filename:
            raise HTTPException(status_code=400, detail="Filename is required")

        contents = await upload_file.read()

        if len(contents) > settings.MAX_FILE_SIZE_BYTES:
            raise HTTPException(
                status_code=400,
                detail=f"File too large. Maximum size: {settings.MAX_FILE_SIZE_MB}MB",
            )

        try:
            image = Image.open(io.BytesIO(contents))
            width, height = image.size
            format_type = image.format
        except Exception:
            raise HTTPException(status_code=400, detail="Invalid image file")

        if settings.USE_GCS and gcs_storage:
            try:
                file_info = gcs_storage.upload_image(
                    file_data=contents,
                    filename=upload_file.filename,
                    content_type=upload_file.content_type or "image/jpeg",
                    make_public=True,
                )
                file_info["storage"] = "gcs"

                print("\n" + "=" * 80)
                print("✅ FILE UPLOADED TO GCP")
                print("=" * 80)
                print(f"📁 Filename: {file_info.get('original_filename')}")
                print(f"🌐 PUBLIC URL: {file_info.get('public_url')}")
                print(f"📦 Bucket: {file_info.get('bucket')}")
                print(f"📍 Blob path: {file_info.get('blob_name')}")
                print(f"📏 Size: {file_info.get('size')} bytes")
                print(
                    f"📐 Dimensions: {file_info.get('width')}x{file_info.get('height')}"
                )
                print("=" * 80 + "\n")

                return file_info
            except Exception as e:
                raise HTTPException(
                    status_code=500, detail=f"Error uploading to GCS: {str(e)}"
                )

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
            "content_type": upload_file.content_type,
        }

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error saving file: {str(e)}")


@router.post("/upload")
async def upload_image(file: UploadFile = File(...)):
    try:
        validate_image(file)
        print("validate image done")
        file_info = await save_upload_file(file)
        print("file info 2 : ", file_info)
        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "File uploaded successfully",
                "data": file_info,
            },
        )

    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code, content={"success": False, "message": e.detail}
        )
    except Exception as e:
        return JSONResponse(
            status_code=500,
            content={"success": False, "message": f"Internal server error: {str(e)}"},
        )


@router.post("/upload/multiple")
async def upload_multiple_images(files: List[UploadFile] = File(...)):
    if not files:
        raise HTTPException(status_code=400, detail="No files provided")

    if len(files) > settings.MAX_FILES_PER_UPLOAD:
        raise HTTPException(
            status_code=400,
            detail=f"Maximum {settings.MAX_FILES_PER_UPLOAD} files allowed",
        )

    uploaded_files = []
    errors = []

    for file in files:
        try:
            validate_image(file)
            file_info = await save_upload_file(file)
            uploaded_files.append(file_info)
        except Exception as e:
            errors.append({"filename": file.filename, "error": str(e)})

    return JSONResponse(
        status_code=200,
        content={
            "success": True,
            "message": f"Uploaded {len(uploaded_files)} file(s)",
            "data": {"uploaded": uploaded_files, "errors": errors},
        },
    )


@router.get("/uploads")
async def list_uploads(limit: int = 100):
    try:
        if settings.USE_GCS and gcs_storage:
            files = gcs_storage.list_files(max_results=limit)
            return {
                "success": True,
                "storage": "gcs",
                "count": len(files),
                "files": files,
            }
        else:
            if not settings.UPLOAD_DIR.exists():
                return {"success": True, "storage": "local", "count": 0, "files": []}

            files = []
            for file_path in settings.UPLOAD_DIR.glob("*"):
                if file_path.is_file():
                    files.append(
                        {
                            "name": file_path.name,
                            "size": file_path.stat().st_size,
                            "path": str(file_path),
                        }
                    )

            return {
                "success": True,
                "storage": "local",
                "count": len(files),
                "files": files[:limit],
            }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error listing files: {str(e)}")


@router.delete("/uploads/{blob_name:path}")
async def delete_upload(blob_name: str):
    try:
        if settings.USE_GCS and gcs_storage:
            gcs_storage.delete_file(blob_name)
            return {"success": True, "message": f"File {blob_name} deleted from GCS"}
        else:
            file_path = settings.UPLOAD_DIR / blob_name

            if not file_path.exists():
                raise HTTPException(status_code=404, detail="File not found")

            os.remove(file_path)
            return {
                "success": True,
                "message": f"File {blob_name} deleted from local storage",
            }
    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error deleting file: {str(e)}")


@router.post("/process")
async def process_image(file: UploadFile = File(...)):
    try:
        validate_image(file)
        file_info = await save_upload_file(file)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Image processed successfully",
                "data": {
                    "file": file_info,
                    "analysis": {
                        "status": "pending",
                        "message": "AI processing will be implemented here",
                    },
                },
            },
        )

    except HTTPException as e:
        return JSONResponse(
            status_code=e.status_code, content={"success": False, "message": e.detail}
        )


@router.post("/image-to-text", response_model=ImageToTextResponse)
async def image_to_text(request: ImageToTextRequest = Body(...)):
    try:
        if not vertex_ai_initialized:
            raise HTTPException(
                status_code=503,
                detail="Image-to-text service not configured. Vertex AI initialization failed.",
            )

        if not request.blob_name and not request.image_url:
            raise HTTPException(
                status_code=400,
                detail="Either 'blob_name' or 'image_url' must be provided",
            )

        image_data: Optional[bytes] = None
        image_info: Dict[str, Any] = {}
        gcs_uri: Optional[str] = None

        if request.blob_name:
            if not settings.USE_GCS or not gcs_storage:
                raise HTTPException(
                    status_code=400,
                    detail="GCS storage not configured. Cannot retrieve image by blob_name.",
                )

            if not gcs_storage.file_exists(request.blob_name):
                raise HTTPException(
                    status_code=404,
                    detail=f"Image not found in bucket: {request.blob_name}",
                )

            gcs_uri = f"gs://{settings.GCS_BUCKET_NAME}/{request.blob_name}"

            blob = gcs_storage.bucket.blob(request.blob_name)
            blob.reload()
            image_info = {
                "blob_name": request.blob_name,
                "bucket": settings.GCS_BUCKET_NAME,
                "size": blob.size,
                "content_type": blob.content_type,
                "created": blob.time_created.isoformat() if blob.time_created else None,
            }
        elif request.image_url:
            import requests

            response = requests.get(request.image_url, timeout=30)
            if response.status_code != 200:
                raise HTTPException(
                    status_code=400,
                    detail=f"Failed to download image from URL: {response.status_code}",
                )
            image_data = response.content
            image_info = {"image_url": request.image_url}

        default_prompt = (
            "Please provide a detailed, comprehensive description of this image. "
            "Include information about: the main subjects or objects, their colors, "
            "textures, materials, style, positioning, lighting, mood, and any other "
            "relevant visual details. Be thorough and descriptive as if explaining "
            "the image to someone who cannot see it."
        )

        if request.detail_level == "low":
            default_prompt = (
                "Provide a brief description of this image in 2-3 sentences."
            )
        elif request.detail_level == "medium":
            default_prompt = (
                "Provide a moderate description of this image, covering the main "
                "subjects, colors, and composition in a paragraph."
            )

        final_prompt = request.prompt if request.prompt else default_prompt

        model = GenerativeModel(settings.GEMINI_MODEL)

        if gcs_uri:
            image_part = Part.from_uri(gcs_uri, mime_type="image/jpeg")
        elif image_data:
            image_part = Part.from_data(image_data, mime_type="image/jpeg")
        else:
            raise HTTPException(status_code=500, detail="Failed to load image data")

        response = model.generate_content([final_prompt, image_part], stream=False)

        description = response.text if hasattr(response, "text") else str(response)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Image successfully converted to text using Gemini Vision",
                "description": description,
                "image_info": image_info,
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(
            status_code=500, detail=f"Error processing image to text: {str(e)}"
        )


@router.post("/merge-images")
async def merge_images(
    url1: str = Body(..., embed=True, description="URL of the first image"),
    url2: str = Body(..., embed=True, description="URL of the second image"),
    prompt: Optional[str] = Body(
        None, embed=True, description="Optional prompt for image merging"
    ),
):
    try:
        merger = ImageMerger()
        result = merger.merge_images(url1, url2, prompt)

        output_dir = os.path.join(os.path.dirname(__file__), "..", "image_temp_folder")
        os.makedirs(output_dir, exist_ok=True)

        saved_path = merger.save_merged_image(result, output_dir=output_dir)

        if not saved_path or not os.path.exists(saved_path):
            raise HTTPException(status_code=500, detail="Failed to save merged image")

        try:
            with open(saved_path, "rb") as file:
                file_contents = file.read()
                filename = os.path.basename(saved_path)

                upload_file = UploadFile(
                    filename=filename, file=io.BytesIO(file_contents)
                )

                validate_image(upload_file)
                file_info = await save_upload_file(upload_file)

                print("\n" + "🎨" * 40)
                print("✅ MERGED IMAGE UPLOADED")
                print("🎨" * 40)

                if file_info.get("storage") == "gcs" and file_info.get("public_url"):
                    print(f"🌐 PUBLIC URL: {file_info.get('public_url')}")
                    print(f"📦 Bucket: {file_info.get('bucket')}")
                elif file_info.get("storage") == "local" and file_info.get("path"):
                    print(f"📁 Local Path: {file_info.get('path')}")
                    print("💡 File saved locally (GCS not configured)")

                print(f"📏 Size: {file_info.get('size')} bytes")
                print(
                    f"📐 Dimensions: {file_info.get('width')}x{file_info.get('height')}"
                )
                print("🎨" * 40 + "\n")

        finally:
            if os.path.exists(saved_path):
                os.remove(saved_path)

        return JSONResponse(
            status_code=200,
            content={
                "success": True,
                "message": "Images merged and uploaded successfully",
                "data": {"file": file_info},
            },
        )

    except HTTPException:
        raise
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error merging images: {str(e)}")
