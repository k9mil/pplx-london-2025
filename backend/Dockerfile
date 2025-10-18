FROM python:3.12-slim

WORKDIR /app

# Install dependencies
COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

# Copy application
COPY . .

# Expose port (Cloud Run uses PORT env var)
ENV PORT=8080

# Run with uvicorn
CMD uvicorn main:app --host 0.0.0.0 --port ${PORT}

