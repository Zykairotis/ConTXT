#!/bin/bash
# Environment setup script for ConTXT Document Processing System

# Color outputs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
BLUE='\033[0;34m'
BOLD='\033[1m'
NC='\033[0m' # No Color

echo -e "${BLUE}${BOLD}=== ConTXT Document Processing System - Environment Setup ===${NC}"
echo -e "This script will help you set up the environment configuration for the ConTXT Document Processing System.\n"

# Check if .env already exists
if [ -f ".env" ]; then
    echo -e "${YELLOW}A .env file already exists.${NC}"
    read -p "Do you want to overwrite it? (y/N): " overwrite
    if [ "$overwrite" != "y" ] && [ "$overwrite" != "Y" ]; then
        echo -e "${GREEN}Setup aborted. Your .env file remains unchanged.${NC}"
        exit 0
    fi
fi

echo -e "\n${YELLOW}Setting up .env file with default values...${NC}"

# Create .env file
cat > .env << EOL
# =============================================================================
# API Keys (Required to enable respective provider)
# =============================================================================
ANTHROPIC_API_KEY="your_anthropic_api_key_here"
PERPLEXITY_API_KEY="your_perplexity_api_key_here"
OPENAI_API_KEY="your_openai_api_key_here"
GOOGLE_API_KEY="your_google_api_key_here"
MISTRAL_API_KEY="your_mistral_key_here"
XAI_API_KEY="your_xai_api_key_here"
AZURE_OPENAI_API_KEY="your_azure_key_here"
OLLAMA_API_KEY="your_ollama_api_key_here"
GITHUB_API_KEY="your_github_api_key_here"

# =============================================================================
# Cognee Configuration
# =============================================================================
LLM_API_KEY=\${XAI_API_KEY}  # Default to XAI key
LLM_PROVIDER="openai"  # xAI uses OpenAI-compatible API
LLM_MODEL="grok-beta"  # or "grok-4" based on your preference
LLM_ENDPOINT="https://api.x.ai/v1"

# Processing Configuration
CHUNK_SIZE=1024
CHUNK_OVERLAP=128
EMBEDDING_MODEL="text-embedding-3-large"

# =============================================================================
# Graph Database Configuration (Neo4j)
# =============================================================================
GRAPH_DATABASE_PROVIDER=neo4j
# For Docker: use service name, for local: use localhost
NEO4J_URI=bolt://neo4j:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=password

# Local development override (uncomment for local development)
# NEO4J_URI=bolt://localhost:7687

# =============================================================================
# Vector Database Configuration (Qdrant)
# =============================================================================
VECTOR_DB_PROVIDER=qdrant
# For Docker: use service name, for local: use localhost
VECTOR_DB_URL=http://qdrant:6333
VECTOR_DB_KEY=""  # Empty for local development

# Local development override (uncomment for local development)
# VECTOR_DB_URL=http://localhost:6333

# =============================================================================
# Relational Database Configuration (PostgreSQL)
# =============================================================================
DB_PROVIDER=postgres
# For Docker: use service name, for local: use localhost
DB_HOST=postgres
DB_PORT=5432
DB_USERNAME=postgres
DB_PASSWORD=postgres
DB_NAME=document_processor
DB_SSL_MODE=disable

# Local development override (uncomment for local development)
# DB_HOST=localhost
# DB_USERNAME=cognee
# DB_PASSWORD=cognee
# DB_NAME=cognee_db

# =============================================================================
# Redis Configuration
# =============================================================================
REDIS_URL=redis://redis:6379/0
REDIS_PASSWORD=""

# Local development override (uncomment for local development)
# REDIS_URL=redis://localhost:6379/0

# =============================================================================
# FastAPI Application Configuration
# =============================================================================
DEBUG=true
LOG_LEVEL=info
ENVIRONMENT=development

# CORS Configuration
CORS_ORIGINS=["http://localhost:3000", "http://localhost:8000", "http://localhost:5173"]

# =============================================================================
# File Processing Configuration
# =============================================================================
MAX_FILE_SIZE=104857600  # 100MB in bytes
UPLOAD_PATH=/app/uploads
PROCESSED_PATH=/app/processed
MAX_CONCURRENT_UPLOADS=10
SUPPORTED_FILE_TYPES=["json", "csv", "txt", "md", "pdf", "png", "jpg", "jpeg"]

# =============================================================================
# Celery Configuration
# =============================================================================
CELERY_BROKER_URL=redis://redis:6379/0
CELERY_RESULT_BACKEND=redis://redis:6379/0
CELERY_TASK_SERIALIZER=json
CELERY_RESULT_SERIALIZER=json
CELERY_ACCEPT_CONTENT=["json"]
CELERY_TIMEZONE=UTC
CELERY_ENABLE_UTC=true

# =============================================================================
# Security Configuration
# =============================================================================
SECRET_KEY=your-secret-key-here-make-it-long-and-random
ACCESS_TOKEN_EXPIRE_MINUTES=30
ALGORITHM=HS256

# =============================================================================
# Monitoring and Logging
# =============================================================================
ENABLE_METRICS=true
METRICS_PORT=9090
LOG_FORMAT=json
LOG_FILE=/app/logs/app.log

# =============================================================================
# Production Overrides (uncomment for production)
# =============================================================================
# DEBUG=false
# ENVIRONMENT=production
# LOG_LEVEL=warning
# NEO4J_URI=neo4j+s://your-production-instance.databases.neo4j.io:7687
# VECTOR_DB_URL=https://your-cluster.cloud.qdrant.io:6333
# VECTOR_DB_KEY=your-production-qdrant-key
# DB_HOST=your-production-db-host
# DB_SSL_MODE=require
EOL

echo -e "${GREEN}Default .env file created.${NC}"
echo -e "${YELLOW}Now, let's customize your configuration...${NC}\n"

# Generate a secure secret key
GENERATED_SECRET_KEY=$(python3 -c "import secrets; print(secrets.token_urlsafe(32))" 2>/dev/null || echo "your-secret-key-here-make-it-long-and-random")
sed -i "s|SECRET_KEY=.*|SECRET_KEY=$GENERATED_SECRET_KEY|" .env

# Prompt for API keys
read -p "Enter your xAI API key (leave empty to keep default): " xai_key
if [ ! -z "$xai_key" ]; then
    sed -i "s/XAI_API_KEY=.*/XAI_API_KEY=$xai_key/" .env
fi

read -p "Enter your OpenAI API key (leave empty to keep default): " openai_key
if [ ! -z "$openai_key" ]; then
    sed -i "s/OPENAI_API_KEY=.*/OPENAI_API_KEY=$openai_key/" .env
fi

read -p "Enter your Anthropic API key (leave empty to keep default): " anthropic_key
if [ ! -z "$anthropic_key" ]; then
    sed -i "s/ANTHROPIC_API_KEY=.*/ANTHROPIC_API_KEY=$anthropic_key/" .env
fi

# Prompt for Neo4j password
read -p "Enter Neo4j password (default: password): " neo4j_pass
if [ ! -z "$neo4j_pass" ]; then
    sed -i "s/NEO4J_PASSWORD=.*/NEO4J_PASSWORD=$neo4j_pass/" .env
fi

# Prompt for PostgreSQL password
read -p "Enter PostgreSQL password (default: postgres): " pg_pass
if [ ! -z "$pg_pass" ]; then
    sed -i "s/DB_PASSWORD=.*/DB_PASSWORD=$pg_pass/" .env
fi

# Prompt for environment selection
echo -e "\n${YELLOW}Select environment:${NC}"
echo "1) Docker (default)"
echo "2) Local development"
read -p "Enter your choice (1-2): " env_choice

if [ "$env_choice" = "2" ]; then
    # Enable local development overrides
    sed -i "s|# NEO4J_URI=bolt://localhost:7687|NEO4J_URI=bolt://localhost:7687|" .env
    sed -i "s|# VECTOR_DB_URL=http://localhost:6333|VECTOR_DB_URL=http://localhost:6333|" .env
    sed -i "s|# REDIS_URL=redis://localhost:6379/0|REDIS_URL=redis://localhost:6379/0|" .env
    sed -i "s|# DB_HOST=localhost|DB_HOST=localhost|" .env
    
    # Comment out Docker-specific settings
    sed -i "s|NEO4J_URI=bolt://neo4j:7687|# NEO4J_URI=bolt://neo4j:7687|" .env
    sed -i "s|VECTOR_DB_URL=http://qdrant:6333|# VECTOR_DB_URL=http://qdrant:6333|" .env
    sed -i "s|REDIS_URL=redis://redis:6379/0|# REDIS_URL=redis://redis:6379/0|" .env
    sed -i "s|DB_HOST=postgres|# DB_HOST=postgres|" .env
    
    echo -e "${GREEN}Environment configured for local development.${NC}"
else
    echo -e "${GREEN}Environment configured for Docker deployment.${NC}"
fi

echo -e "\n${GREEN}Environment configuration completed!${NC}"
echo -e "Your .env file has been created with your custom settings."
echo -e "\n${YELLOW}Next steps:${NC}"
echo -e "1. Review your .env file to make any additional changes"
echo -e "2. Add your .env file to .gitignore if not already included"
echo -e "3. Start the system with: ./scripts/docker_start.sh"
echo -e "4. Test your setup with: ./scripts/test_docker_system.py"

# Add .env to .gitignore if not already included
if ! grep -q "^.env$" .gitignore 2>/dev/null; then
    echo -e "\n${YELLOW}Adding .env to .gitignore for security...${NC}"
    echo ".env" >> .gitignore
    echo -e "${GREEN}Added .env to .gitignore.${NC}"
fi 