FROM python:3.11-slim

WORKDIR /app

# Install system dependencies
RUN apt-get update && apt-get install -y --no-install-recommends \
    build-essential \
    curl \
    git \
    libpq-dev \
    && apt-get clean \
    && rm -rf /var/lib/apt/lists/*

# Install uv
RUN curl -sSf https://astral.sh/uv/install.sh | sh

# Copy requirements and install dependencies
COPY pyproject.toml .
COPY README.md .

# Install dependencies
RUN uv pip install -e .

# Copy the rest of the application
COPY . .

# Set environment variables
ENV PYTHONPATH=/app
ENV PYTHONUNBUFFERED=1

# Expose ports
EXPOSE 8000

# Default command
CMD ["uvicorn", "Backend.main:app", "--host", "0.0.0.0", "--port", "8000"] 