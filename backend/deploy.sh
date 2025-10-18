#!/bin/bash
# Quick deploy script for Cloud Run

# Colors for output
GREEN='\033[0;32m'
BLUE='\033[0;34m'
NC='\033[0m' # No Color

echo -e "${BLUE}🚀 Deploying to Google Cloud Run...${NC}"

# Check if gcloud is installed
if ! command -v gcloud &> /dev/null; then
    echo "❌ gcloud CLI not found. Install it from: https://cloud.google.com/sdk/docs/install"
    exit 1
fi

# Get project ID
PROJECT_ID=$(gcloud config get-value project 2>/dev/null)
if [ -z "$PROJECT_ID" ]; then
    echo "❌ No GCP project set. Run: gcloud config set project YOUR_PROJECT_ID"
    exit 1
fi

echo -e "${GREEN}✓ Project: $PROJECT_ID${NC}"

# Deploy
echo -e "${BLUE}📦 Building and deploying...${NC}"

gcloud run deploy pplx-london-api \
  --source . \
  --region europe-west2 \
  --allow-unauthenticated \
  --set-env-vars "GCS_BUCKET_NAME=pplx-london-space-uploads,GCP_PROJECT_ID=$PROJECT_ID"

if [ $? -eq 0 ]; then
    echo -e "${GREEN}✅ Deployment successful!${NC}"
    
    # Get and display URL
    URL=$(gcloud run services describe pplx-london-api --region europe-west2 --format 'value(status.url)')
    echo -e "${GREEN}🌐 Your API is live at: $URL${NC}"
    echo -e "${BLUE}📚 Docs: $URL/docs${NC}"
    echo -e "${BLUE}❤️  Health: $URL/health${NC}"
else
    echo -e "❌ Deployment failed"
    exit 1
fi

