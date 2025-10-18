from google.cloud import storage
from google.oauth2 import service_account
from PIL import Image
import io
import os
from datetime import datetime, timedelta
from typing import Optional, Dict, Any
from config import settings


class GCSStorage:
    def __init__(
        self,
        bucket_name: str,
        credentials_path: Optional[str] = None,
        project_id: Optional[str] = None,
    ):
        self.bucket_name = bucket_name

        if credentials_path and os.path.exists(credentials_path):
            credentials = service_account.Credentials.from_service_account_file(
                credentials_path
            )
            self.client = storage.Client(credentials=credentials, project=project_id)
        else:
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
        timestamp = datetime.now().strftime("%Y%m%d_%H%M%S_%f")
        blob_name = f"{folder}/{timestamp}_{filename}"

        try:
            image = Image.open(io.BytesIO(file_data))
            width, height = image.size
            format_type = image.format
        except Exception as e:
            raise ValueError(f"Invalid image file: {str(e)}")

        blob = self.bucket.blob(blob_name)
        blob.content_type = content_type

        blob.cache_control = "public, max-age=31536000"

        blob.upload_from_string(file_data, content_type=content_type)

        if make_public:
            blob.make_public()

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
        blob = self.bucket.blob(blob_name)
        blob.delete()
        return True

    def get_signed_url(self, blob_name: str, expiration_minutes: int = 60) -> str:
        blob = self.bucket.blob(blob_name)
        url = blob.generate_signed_url(
            expiration=timedelta(minutes=expiration_minutes), method="GET"
        )
        return url

    def list_files(self, prefix: str = "uploads/", max_results: int = 100) -> list:
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
        blob = self.bucket.blob(blob_name)
        return blob.exists()


def get_storage_client() -> Optional[GCSStorage]:
    if not settings.GCS_BUCKET_NAME:
        return None

    return GCSStorage(
        bucket_name=settings.GCS_BUCKET_NAME,
        credentials_path=settings.GCS_CREDENTIALS_PATH
        if settings.GCS_CREDENTIALS_PATH
        else None,
        project_id=settings.GCP_PROJECT_ID if settings.GCP_PROJECT_ID else None,
    )
