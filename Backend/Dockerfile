FROM python:3.11-slim

WORKDIR /app

# Install system dependencies including those needed for document processing
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libpq-dev \
    libmagic1 \
    libmagic-dev \
    poppler-utils \
    tesseract-ocr \
    libreoffice \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Copy requirements files
COPY requirements.txt .
COPY app/processors/requirements.txt ./processor_requirements.txt

# Install Python dependencies
RUN pip install --no-cache-dir -r requirements.txt
RUN pip install --no-cache-dir -r processor_requirements.txt

# Install additional dependencies for integration
RUN pip install --no-cache-dir \
    langchain-xai \
    pandas \
    pillow \
    python-multipart \
    aiofiles

# Copy the application code
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Create directories for file uploads and processing
RUN mkdir -p /app/uploads /app/processed /app/logs

# Expose the port
EXPOSE 8000

# Health check
HEALTHCHECK --interval=30s --timeout=10s --start-period=5s --retries=3 \
    CMD curl -f http://localhost:8000/ || exit 1

# Default command
CMD ["uvicorn", "app.main:app", "--host", "0.0.0.0", "--port", "8000", "--reload"] 