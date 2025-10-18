"""
Application configuration
"""
import os
from pathlib import Path
from dotenv import load_dotenv

# Load environment variables
load_dotenv()


class Settings:
    """Application settings"""
    
    # API Configuration
    API_HOST: str = os.getenv("API_HOST", "0.0.0.0")
    API_PORT: int = int(os.getenv("PORT", os.getenv("API_PORT", "8000")))
    
    # CORS Configuration
    ALLOWED_ORIGINS: list[str] = os.getenv(
        "ALLOWED_ORIGINS",
        "http://localhost:5173,http://localhost:3000"
    ).split(",")
    
    # File Upload Configuration
    MAX_FILE_SIZE_MB: int = int(os.getenv("MAX_FILE_SIZE_MB", "10"))
    MAX_FILE_SIZE_BYTES: int = MAX_FILE_SIZE_MB * 1024 * 1024
    ALLOWED_EXTENSIONS: set[str] = {".jpg", ".jpeg", ".png", ".gif", ".webp"}
    MAX_FILES_PER_UPLOAD: int = 10
    
    # Local Storage Configuration
    UPLOAD_DIR: Path = Path("uploads")
    
    # Google Cloud Storage Configuration
    GCS_BUCKET_NAME: str = os.getenv("GCS_BUCKET_NAME", "")
    GCP_PROJECT_ID: str = os.getenv("GCP_PROJECT_ID", "")
    GCS_CREDENTIALS_PATH: str = os.getenv("GCS_CREDENTIALS_PATH", "")
    GCS_FOLDER: str = "uploads"
    
    # Use GCS if bucket name is configured
    USE_GCS: bool = bool(GCS_BUCKET_NAME)
    
    # Vertex AI Configuration (for image-to-text)
    VERTEX_AI_PROJECT: str = os.getenv("VERTEX_AI_PROJECT", GCP_PROJECT_ID)
    VERTEX_AI_LOCATION: str = os.getenv("VERTEX_AI_LOCATION", "us-central1")
    GEMINI_MODEL: str = os.getenv("GEMINI_MODEL", "gemini-2.5-flash")
    
    # App Metadata
    APP_TITLE: str = "PPLX London 2025 API"
    APP_DESCRIPTION: str = "Backend API for image processing and AI-powered shopping assistance"
    APP_VERSION: str = "1.0.0"
    
    def __init__(self):
        """Initialize settings and create necessary directories"""
        if not self.USE_GCS:
            self.UPLOAD_DIR.mkdir(exist_ok=True)


# Global settings instance
settings = Settings()

