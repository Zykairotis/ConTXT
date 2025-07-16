# AI Context Engineering Agent Backend

This is the backend service for the AI Context Engineering Agent, which provides context engineering capabilities for AI-assisted software development.

## Overview

The AI Context Engineering Agent backend is built with:

- **FastAPI**: High-performance API framework
- **LangGraph**: Workflow orchestration for context engineering
- **Neo4j**: Graph database for knowledge representation
- **Qdrant**: Vector database for embeddings and semantic search

## Quick Start

### Prerequisites

- Python 3.11+
- Docker and Docker Compose

### Setup

1. Clone the repository:
   ```bash
   git clone <repository-url>
   cd ConTXT
   ```

2. Create a virtual environment (using uv):
   ```bash
   uv venv
   source .venv/bin/activate
   ```

3. Install dependencies:
   ```bash
   cd Backend
   pip install -r requirements.txt
   ```

4. Create a `.env` file in the `Backend` directory:
   ```
   # API Configuration
   API_V1_STR=/api/v1
   PROJECT_NAME=AI Context Engineering Agent
   CORS_ORIGINS=http://localhost:3000,http://localhost:8000

   # Neo4j Configuration
   NEO4J_HOST=localhost  # Use 'neo4j' when running inside Docker
   NEO4J_PORT=7687
   NEO4J_USER=neo4j
   NEO4J_PASSWORD=password

   # Qdrant Configuration
   QDRANT_HOST=localhost  # Use 'qdrant' when running inside Docker
   QDRANT_PORT=6333
   QDRANT_COLLECTION=context_vectors

   # LLM Configuration
   OPENAI_API_KEY=your_openai_api_key_here
   ANTHROPIC_API_KEY=your_anthropic_api_key_here
   DEFAULT_LLM_MODEL=gpt-4o
   ```

5. Start the database services:
   ```bash
   ./start_services.sh
   ```
   or manually:
   ```bash
   docker compose up -d
   ```

6. Test database connections:
   ```bash
   ./test_local.sh
   ```
   or manually:
   ```bash
   export NEO4J_HOST=localhost
   export QDRANT_HOST=localhost
   python test_connections.py
   ```

7. Run the application:
   ```bash
   python run.py
   ```

8. Access the API documentation at http://localhost:8000/docs

## Environment Configuration

The application supports two environments:

### Local Development (Default)

When running the application locally but using Docker for databases:
- Set `NEO4J_HOST=localhost` and `QDRANT_HOST=localhost` in your `.env` file
- Use `./test_local.sh` to run tests

### Docker Environment

When running the application inside Docker:
- Set `NEO4J_HOST=neo4j` and `QDRANT_HOST=qdrant` in your `.env` file
- Use Docker networking to connect to services

## Services

### Neo4j

- **Purpose**: Graph database for knowledge representation
- **Access**: http://localhost:7474 (Browser interface)
- **Credentials**: neo4j / password

### Qdrant

- **Purpose**: Vector database for embeddings
- **Access**: http://localhost:6333/dashboard (Web dashboard)
- **API**: http://localhost:6333 (REST API)

## API Endpoints

### Context Engineering

- `POST /api/context/build`: Build engineered context from sources
- `POST /api/context/generate-system-prompt`: Generate system prompts

### Knowledge Graph

- `POST /api/knowledge/query`: Query the knowledge graph
- `POST /api/knowledge/entity`: Add an entity to the graph
- `POST /api/knowledge/relationship`: Add a relationship to the graph

### Ingestion

- `POST /api/ingestion/url`: Ingest content from a URL
- `POST /api/ingestion/file`: Ingest content from a file
- `POST /api/ingestion/text`: Ingest raw text content

## Development

### Project Structure

```
Backend/
├── app/
│   ├── api/              # API routes and endpoints
│   ├── core/             # Core business logic
│   ├── db/               # Database clients
│   ├── models/           # Data models
│   ├── processors/       # Data processors
│   ├── schemas/          # Pydantic schemas
│   └── utils/            # Utility functions
├── docker-compose.yml    # Docker services configuration
├── Dockerfile            # Docker build configuration
├── requirements.txt      # Python dependencies
├── run.py                # Entry point
├── test_connections.py   # Database connection test
├── test_local.sh         # Script for testing local connections
└── start_services.sh     # Script to start Docker services
```

### Adding New Features

1. Define schemas in `app/schemas/`
2. Implement core logic in `app/core/`
3. Create API endpoints in `app/api/endpoints/`
4. Register routes in `app/api/router.py` 