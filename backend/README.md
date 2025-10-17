# Backend API

FastAPI backend with image upload to GCS and auto-deploy to Cloud Run.

## Quick Start for New Developers

```bash
# 1. Navigate to backend
cd backend

# 2. Create virtual environment
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate

# 3. Install dependencies
pip install -r requirements.txt

# 4. Set up environment (optional)
cp .env.example .env
# Edit .env if needed (works without it - uses local storage)

# 5. Run the server
python main.py
```

**API**: http://localhost:8000  
**Docs**: http://localhost:8000/docs (interactive API documentation)

### What You Need

**Required**:
- Python 3.12+
- pip

**Optional** (for GCS):
- Google Cloud account
- GCS bucket
- Service account key (see GCS Setup below)

**Default behavior**: Without `.env` or GCS config, uploads go to `backend/uploads/` folder (works fine for local dev!)

## Deploy to Cloud Run

```bash
./deploy.sh
```

First time? Run these commands first:
```bash
# Enable APIs and grant permissions
gcloud services enable cloudbuild.googleapis.com run.googleapis.com

PROJECT_NUMBER=$(gcloud projects describe my-test-project-475121 --format="value(projectNumber)")

gcloud projects add-iam-policy-binding my-test-project-475121 \
  --member="serviceAccount:${PROJECT_NUMBER}@cloudbuild.gserviceaccount.com" \
  --role="roles/run.admin" --quiet

gcloud projects add-iam-policy-binding my-test-project-475121 \
  --member="serviceAccount:${PROJECT_NUMBER}-compute@developer.gserviceaccount.com" \
  --role="roles/storage.objectAdmin" --quiet
```

## Auto Deploy (GitHub Actions)

Pushes to `main` auto-deploy. Setup:

1. Create service account:
```bash
gcloud iam service-accounts create github-actions \
  --display-name="GitHub Actions" \
  --project=my-test-project-475121

gcloud projects add-iam-policy-binding my-test-project-475121 \
  --member="serviceAccount:github-actions@my-test-project-475121.iam.gserviceaccount.com" \
  --role="roles/run.admin" --quiet

gcloud iam service-accounts keys create key.json \
  --iam-account=github-actions@my-test-project-475121.iam.gserviceaccount.com
```

2. Add to GitHub: Settings → Secrets → New secret
   - Name: `GCP_SA_KEY`
   - Value: Contents of `key.json`

3. Delete local key: `rm key.json`

## GCS Setup (Optional for Local Dev)

To test with real GCS locally:

1. **Get service account key** from team lead or create one:
```bash
gcloud iam service-accounts keys create service-account-key.json \
  --iam-account=pplx-storage@my-test-project-475121.iam.gserviceaccount.com
```

2. **Update `.env`**:
```env
GCS_BUCKET_NAME=pplx-london-space-uploads
GCP_PROJECT_ID=my-test-project-475121
GCS_CREDENTIALS_PATH=service-account-key.json
```

3. **Never commit** `service-account-key.json` or `.env` (already in `.gitignore`)

## API Endpoints

### Image Upload Endpoints

- **POST** `/api/upload` - Upload a single image
- **POST** `/api/upload/multiple` - Upload multiple images
- **GET** `/api/uploads` - List uploaded files
- **DELETE** `/api/uploads/{blob_name}` - Delete a file
- **POST** `/api/process` - Process image (placeholder for future AI processing)

### Image-to-Text Endpoint

**POST** `/api/image-to-text` - Convert image to detailed text description

This endpoint converts images from your GCS bucket into detailed text descriptions using **Google's Gemini Vision model** (via Vertex AI). It's designed for integration with ElevenLabs agent and other services that need text descriptions instead of direct image URLs.

**Benefits of using Gemini:**
- ✅ Stays within Google Cloud ecosystem (same credentials as GCS)
- ✅ Direct GCS URI support for faster processing
- ✅ No need for separate API keys
- ✅ High-quality vision capabilities with Gemini 1.5

**Request body:**
```json
{
  "blob_name": "uploads/20241017_123456_image.jpg",  // Recommended: GCS blob path
  "image_url": "https://...",  // Alternative: public image URL
  "prompt": "Describe this bedroom in detail",  // Optional custom prompt
  "detail_level": "high"  // Options: "low", "medium", "high" (default: "high")
}
```

**Response:**
```json
{
  "success": true,
  "message": "Image successfully converted to text using Gemini Vision",
  "description": "This is a modern bedroom featuring...",
  "image_info": {
    "blob_name": "uploads/20241017_123456_image.jpg",
    "bucket": "pplx-london-space-uploads",
    "size": 245678,
    "content_type": "image/jpeg",
    "created": "2024-10-17T12:34:56.789Z"
  }
}
```

**Example usage with ElevenLabs:**
```python
# 1. Upload image and get blob_name
response = requests.post("https://api.example.com/api/upload", files={"file": image})
blob_name = response.json()["data"]["blob_name"]

# 2. Convert to text description using Gemini
text_response = requests.post(
    "https://api.example.com/api/image-to-text",
    json={"blob_name": blob_name, "detail_level": "high"}
)
description = text_response.json()["description"]

# 3. Send to ElevenLabs agent
# Use the text description instead of image URL
```

## Environment Variables

See `.env.example` for all options. Key variables:

- `ALLOWED_ORIGINS` - Frontend URLs for CORS
- `MAX_FILE_SIZE_MB` - Max upload size (default: 10MB)
- `GCS_BUCKET_NAME` - Enable GCS (leave empty for local storage)
- `GCP_PROJECT_ID` - Your GCP project (also used for Vertex AI)
- `GCS_CREDENTIALS_PATH` - Path to service account JSON
- `VERTEX_AI_PROJECT` - Vertex AI project (defaults to GCP_PROJECT_ID)
- `VERTEX_AI_LOCATION` - Vertex AI region (default: us-central1)
- `GEMINI_MODEL` - Gemini model to use (default: gemini-1.5-flash)

**Note**: Cloud Run sets these automatically via deployment script. The same service account credentials used for GCS also work for Vertex AI!
