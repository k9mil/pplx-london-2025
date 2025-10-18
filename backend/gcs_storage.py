"""
Storage utilities for handling file uploads (GCS and local)
"""

from google.cloud import storage
from google.oauth2 import service_account
from PIL import Image
import io
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from config import settings


class GCSStorage:
    """Google Cloud Storage handler for file uploads"""

    def __init__(
        self,
        bucket_name: str,
        credentials_path: Optional[str] = None,
        project_id: Optional[str] = None,
    ):
        """
        Initialize GCS client

        Args:
            bucket_name: Name of the GCS bucket
            credentials_path: Path to service account JSON file (optional)
            project_id: GCP project ID (optional)
        """
        self.bucket_name = bucket_name

        # Initialize client with credentials if provided
        if credentials_path and os.path.exists(credentials_path):
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path
            )
            self.client = storage.Client(credentials=credentials, project=project_id)
        else:
            # Use default credentials (from GOOGLE_APPLICATION_CREDENTIALS env var)
            self.client = storage.Client(project=project_id)

        self.bucket = self.client.bucket(bucket_name)

    def upload_image(
        self,
        file_data: bytes,
        filename: str,
        content_type: str = "image/jpeg",
        make_public: bool = True,
        folder: str = "uploads",
    ) -> Dict[str, Any]:
        """
        Upload image to GCS

        Args:
            file_data: Image file bytes
            filename: Original filename
            content_type: MIME type of the file
            make_public: Whether to make the file publicly accessible
            folder: Folder/prefix in the bucket

        Returns:
            Dict with upload information including public URL
        """
        # Generate unique filename with timestamp
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        blob_name = f"{folder}/{timestamp}_{filename}"

        # Validate image
        try:
            image = Image.open(io.BytesIO(file_data))
            width, height = image.size
            format_type = image.format
        except Exception as e:
            raise ValueError(f"Invalid image file: {str(e)}")

        # Create blob and upload
        blob = self.bucket.blob(blob_name)
        blob.content_type = content_type

        # Set cache control for better performance
        blob.cache_control = "public, max-age=31536000"

        # Upload the file
        blob.upload_from_string(file_data, content_type=content_type)

        # Make public if requested
        if make_public:
            blob.make_public()

        # Get public URL
        public_url = blob.public_url

        return {
            "filename": blob_name,
            "original_filename": filename,
            "public_url": public_url,
            "bucket": self.bucket_name,
            "blob_name": blob_name,
            "size": len(file_data),
            "width": width,
            "height": height,
            "format": format_type,
            "content_type": content_type,
            "created_at": datetime.now().isoformat(),
        }

    def delete_file(self, blob_name: str) -> bool:
        """
        Delete a file from GCS

        Args:
            blob_name: Name/path of the blob to delete

        Returns:
            True if successful
        """
        blob = self.bucket.blob(blob_name)
        blob.delete()
        return True

    def get_signed_url(self, blob_name: str, expiration_minutes: int = 60) -> str:
        """
        Generate a signed URL for temporary access

        Args:
            blob_name: Name/path of the blob
            expiration_minutes: URL expiration time in minutes

        Returns:
            Signed URL string
        """
        blob = self.bucket.blob(blob_name)
        url = blob.generate_signed_url(
            expiration=timedelta(minutes=expiration_minutes), method="GET"
        )
        return url

    def list_files(self, prefix: str = "uploads/", max_results: int = 100) -> list:
        """
        List files in the bucket

        Args:
            prefix: Folder/prefix to filter by
            max_results: Maximum number of results

        Returns:
            List of blob information
        """
        blobs = self.client.list_blobs(
            self.bucket_name, prefix=prefix, max_results=max_results
        )

        files = []
        for blob in blobs:
            files.append(
                {
                    "name": blob.name,
                    "size": blob.size,
                    "content_type": blob.content_type,
                    "public_url": blob.public_url,
                    "created": blob.time_created.isoformat()
                    if blob.time_created
                    else None,
                    "updated": blob.updated.isoformat() if blob.updated else None,
                }
            )

        return files

    def file_exists(self, blob_name: str) -> bool:
        """
        Check if a file exists in the bucket

        Args:
            blob_name: Name/path of the blob

        Returns:
            True if file exists
        """
        blob = self.bucket.blob(blob_name)
        return blob.exists()


def get_storage_client() -> Optional[GCSStorage]:
    """
    Get configured GCS storage client from settings

    Returns:
        GCSStorage instance or None if not configured
    """
    if not settings.GCS_BUCKET_NAME:
        return None

    return GCSStorage(
        bucket_name=settings.GCS_BUCKET_NAME,
        credentials_path=settings.GCS_CREDENTIALS_PATH
        if settings.GCS_CREDENTIALS_PATH
        else None,
        project_id=settings.GCP_PROJECT_ID if settings.GCP_PROJECT_ID else None,
    )
