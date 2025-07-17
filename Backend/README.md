# ConTXT - AI Context Engineering Agent Backend

The backend component of the ConTXT application, providing APIs for document processing, knowledge extraction, and context engineering.

## Docker Setup

This project is fully containerized using Docker for easy deployment and development. The Docker configuration includes:

- FastAPI application container
- Neo4j graph database
- Qdrant vector database
- PostgreSQL relational database
- Redis cache
- Celery worker for background processing (optional)
- Flower for monitoring Celery tasks (optional)

### Prerequisites

- Docker and Docker Compose installed
- API keys for LLM services (xAI, OpenAI, etc.)

### Getting Started

1. Create a `.env` file in the Backend directory with your configuration (see `.env.example` for reference):

```bash
# Minimal example .env file
XAI_API_KEY=your-xai-api-key-here
OPENAI_API_KEY=your-openai-api-key-here
```

2. Start the Docker containers:

```bash
# Navigate to the Backend directory
cd Backend

# Start with helper script
./scripts/docker_start.sh

# Or manually with docker-compose
docker-compose up -d
```

3. The following services will be available:

- **API Documentation**: http://localhost:8000/docs
- **Neo4j Browser**: http://localhost:7474 (neo4j/password)
- **Qdrant Dashboard**: http://localhost:6333/dashboard
- **Celery Flower** (if enabled): http://localhost:5555

### Testing the System

A comprehensive test script is provided to verify your setup:

```bash
# Install requests library if not present
pip install requests

# Run the test script
cd Backend
./scripts/test_docker_system.py
```

The test script will:
1. Check if the API is responding
2. Test database connections
3. Create test files
4. Upload files to the system
5. Wait for processing
6. Query the processed data

### Development Workflow

For development with hot-reloading:

```bash
# Start only databases
docker-compose up neo4j qdrant postgres redis

# Run the app locally
uvicorn app.main:app --reload --host 0.0.0.0 --port 8000
```

### Stopping the System

To stop the system:

```bash
# Use the helper script
./scripts/docker_stop.sh

# Or manually
docker-compose down
```

To stop and remove all data volumes:

```bash
docker-compose down -v
```

## API Endpoints

### Ingestion API

- `POST /api/ingestion/upload`: Upload a document
- `POST /api/ingestion/url`: Process a URL
- `GET /api/ingestion/{job_id}`: Get status of ingestion job

### Context API

- `POST /api/context/build`: Build context from sources
- `GET /api/context/{context_id}`: Get context by ID
- `DELETE /api/context/{context_id}`: Delete context

### Knowledge API

- `POST /api/knowledge/search`: Search knowledge graph
- `POST /api/knowledge/query`: Execute knowledge graph query

## Development

### Project Structure

```
Backend/
├── app/
│   ├── api/              # API endpoints
│   ├── config/           # Configuration
│   ├── core/             # Core business logic
│   ├── db/               # Database clients
│   ├── models/           # Data models
│   ├── processors/       # Document processors
│   ├── schemas/          # Pydantic schemas
│   └── utils/            # Utilities
├── scripts/              # Helper scripts
├── docker-compose.yml    # Docker Compose configuration
├── Dockerfile            # Docker configuration
└── requirements.txt      # Python dependencies
```

### Running Tests

```bash
# Run all tests
pytest

# Run specific test
pytest tests/test_ingestion.py
```

## Troubleshooting

### Common Issues

1. **Services not starting**: Check Docker logs and ensure all environment variables are set
   ```bash
   docker-compose logs app
   ```

2. **Database connection errors**: Verify database containers are running and accessible
   ```bash
   docker-compose ps
   python -m Backend.test_connections
   ```

3. **File upload failures**: Check file permissions and upload directory exists
   ```bash
   docker-compose exec app ls -la /app/uploads
   ```

4. **Memory issues**: Increase Docker memory limits or adjust database configurations in docker-compose.yml 