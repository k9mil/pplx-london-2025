# API Package Structure

Clean, organized API structure for the PPLX London 2025 backend.

## 📁 Structure

```
api/
├── __init__.py           # Package initialization
├── models.py            # Pydantic models (UserPreference, ProductResult, etc.)
├── routes/              # API endpoints
│   ├── __init__.py
│   ├── health.py        # Health check & info endpoints
│   ├── uploads.py       # Image upload & processing endpoints
│   └── search.py        # Furniture search endpoints
└── services/            # Business logic
    ├── __init__.py
    ├── image_merger.py  # Image merging service (Gemini API)
    └── search_service.py # Product search service (Perplexity API)
```

## 🔧 Components

### Models (`models.py`)

- `UserPreference`: User search preferences
- `ProductResult`: Product search results
- `ProductRating`: User ratings for products
- `NarrowSearchRequest`: Refined search request
- `RefinedProduct`: Refined product recommendations

### Routes

#### Health (`routes/health.py`)

- `GET /` - API information
- `GET /health` - Health check

#### Uploads (`routes/uploads.py`)

- `POST /api/upload` - Upload single image
- `POST /api/upload/multiple` - Upload multiple images
- `GET /api/uploads` - List uploads
- `DELETE /api/uploads/{blob_name}` - Delete upload
- `POST /api/process` - Process image
- `POST /api/image-to-text` - Convert image to text (Gemini Vision)
- `POST /api/merge-images` - Merge two images (Gemini)

#### Search (`routes/search.py`)

- `POST /search/general` - General furniture search
- `POST /search/narrow` - Refined search (TODO)
- `POST /search/debug/full-response` - Debug endpoint (TODO)

### Services

#### Image Merger (`services/image_merger.py`)

- `ImageMerger` class for merging images using Gemini API
- Methods:
  - `merge_images()` - Merge two images with prompt
  - `save_merged_image()` - Save merged result

#### Search Service (`services/search_service.py`)

- `general_search()` - Search products from IKEA & JYSK
- `fetch_and_parse_product()` - Fetch & parse individual product
- `parse_single_product()` - Parse product from text

## 🚀 Usage

```python
from fastapi import FastAPI
from api.routes import health, uploads, search

app = FastAPI()

app.include_router(health.router)
app.include_router(uploads.router)
app.include_router(search.router)
```

## ✅ Benefits

1. **Clean separation of concerns**

   - Routes handle HTTP
   - Services handle business logic
   - Models define data structures

2. **Easy to maintain**

   - Each file has a single responsibility
   - Clear import paths
   - Type hints everywhere

3. **Scalable**

   - Easy to add new routes
   - Services are reusable
   - No circular dependencies

4. **Type-safe**
   - All linter errors resolved
   - Proper type annotations
   - Pydantic validation
