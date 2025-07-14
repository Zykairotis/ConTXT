# AI Context Builder Backend

This is the backend component of the AI Context Builder project, which processes multi-modal data to generate intelligent system prompts and configurations.

## Features

- Process multiple data types:
  - Web URLs
  - PDF documents
  - Video content
  - Text conversations
- Generate context-aware configurations for:
  - Cursor
  - Windsurf
  - Other AI tools
- Utilize knowledge graph for semantic understanding
- Asynchronous processing for large files

## Tech Stack

- **FastAPI**: Modern, high-performance web framework
- **LangGraph**: Stateful AI workflow orchestration
- **Cognee**: RAG (Retrieval-Augmented Generation) capabilities
- **Neo4j**: Knowledge graph database
- **Qdrant**: Vector database for embeddings
- **PostgreSQL**: Relational data storage
- **Redis**: Caching and task queuing
- **Celery**: Background task processing

## Project Structure

```
backend/
├── api/          # FastAPI routes and endpoints
├── agents/       # AI agents and workflows
├── processors/   # Data processing components
├── knowledge/    # Knowledge graph and data storage
├── config/       # Configuration management
├── tests/        # Test suite
└── main.py       # Application entry point
```

## Getting Started

### Prerequisites

- Python 3.11+
- Neo4j database
- PostgreSQL database
- Redis server
- Qdrant server (optional, for vector search)

### Installation

1. Clone the repository:
   ```bash
   git clone https://github.com/yourusername/llm-context-builder.git
   cd llm-context-builder
   ```

2. Create and activate a virtual environment:
   ```bash
   uv venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. Install dependencies:
   ```bash
   uv pip install -e .
   ```

4. Create a `.env` file based on `.env.example` and fill in your configuration.

### Running the Application

1. Start the FastAPI server:
   ```bash
   uvicorn Backend.main:app --reload
   ```

2. Start Celery worker (in a separate terminal):
   ```bash
   celery -A Backend.config.celery worker --loglevel=info
   ```

3. (Optional) Start Flower for monitoring Celery tasks:
   ```bash
   celery -A Backend.config.celery flower
   ```

## API Documentation

Once the application is running, you can access the API documentation at:
- Swagger UI: http://localhost:8000/docs
- ReDoc: http://localhost:8000/redoc

## Testing

Run the test suite:
```bash
pytest Backend/tests/
```

## License

This project is licensed under the MIT License - see the LICENSE file for details. 