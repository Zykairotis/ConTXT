# AI Context Builder Containers

This document provides an overview of all containers in the AI Context Builder Docker environment, explaining their purpose, configuration, and how they interact with each other.

## Architecture Diagram

```mermaid
graph TD
    Client[Client] --> API[API Container<br>backend-api:8000]
    
    subgraph "Processing Layer"
        API --> Worker[Worker Container<br>backend-worker]
        API --> Flower[Flower Container<br>backend-flower:5555]
        Worker --> Flower
    end
    
    subgraph "Data Layer"
        API --> PostgreSQL[PostgreSQL<br>postgres:15:5432]
        API --> Redis[Redis<br>redis:7:6379]
        API --> Neo4j[Neo4j<br>neo4j:5:7474/7687]
        API --> Qdrant[Qdrant<br>qdrant:latest:6333/6334]
        
        Worker --> PostgreSQL
        Worker --> Redis
        Worker --> Neo4j
        Worker --> Qdrant
        
        Flower --> Redis
    end
    
    Redis --> Worker
    
    classDef primary fill:#4CAF50,stroke:#388E3C,color:white;
    classDef secondary fill:#2196F3,stroke:#1976D2,color:white;
    classDef database fill:#FF9800,stroke:#F57C00,color:white;
    
    class API,Worker primary;
    class Flower secondary;
    class PostgreSQL,Redis,Neo4j,Qdrant database;
```

## Container Overview

The AI Context Builder backend consists of 7 containers that work together to provide a complete environment for building AI context and generating system prompts:

| Container | Image | Purpose | Ports |
|-----------|-------|---------|-------|
| api-1 | backend-api | FastAPI backend serving REST API endpoints | 8000 |
| worker-1 | backend-worker | Celery worker for processing background tasks | - |
| flower-1 | backend-flower | Celery monitoring interface | 5555 |
| postgres-1 | postgres:15 | Relational database for structured data | 5432 |
| redis-1 | redis:7 | Cache and message broker | 6379 |
| neo4j-1 | neo4j:5 | Graph database for knowledge representation | 7474, 7687 |
| qdrant-1 | qdrant/qdrant:latest | Vector database for embeddings | 6333, 6334 |

## Detailed Container Descriptions

### API Container (backend-api)

**Purpose**: Serves as the main entry point for the application, providing REST API endpoints for client interactions.

**Key Features**:
- Built with FastAPI for high-performance async API endpoints
- Provides endpoints for file upload, context building, and configuration generation
- Integrates with all other services (databases, worker, etc.)
- Implements CORS for frontend integration

**Configuration**:
- Built from custom Dockerfile in the project
- Uses uvicorn as the ASGI server
- Hot-reloading enabled for development
- Environment variables loaded from .env file

**Access**:
- API documentation: http://localhost:8000/docs
- Health check: http://localhost:8000/

### Worker Container (backend-worker)

**Purpose**: Processes background tasks asynchronously to prevent blocking the API.

**Key Features**:
- Runs Celery for task queue processing
- Handles long-running tasks like document processing, embedding generation, etc.
- Communicates with Redis for task queue management
- Accesses all databases for data processing and storage

**Configuration**:
- Built from the same Dockerfile as the API
- Configured to use Redis as broker and result backend
- Shares the same codebase as the API container

### Flower Container (backend-flower)

**Purpose**: Provides a web interface for monitoring and managing Celery tasks.

**Key Features**:
- Real-time monitoring of task execution
- Task history and statistics
- Ability to inspect and manage tasks

**Configuration**:
- Built from the same Dockerfile as the API
- Connects to Redis to monitor Celery tasks
- Provides a web interface on port 5555

**Access**:
- Web interface: http://localhost:5555

### PostgreSQL Container (postgres-1)

**Purpose**: Stores structured relational data for the application.

**Key Features**:
- Reliable relational database
- Stores user data, job metadata, and other structured information
- Persistent storage through Docker volumes

**Configuration**:
- Uses official PostgreSQL 15 image
- Database name: context_builder
- Credentials configured in .env file
- Data persisted in postgres_data volume

**Access**:
- Connection string: postgresql://postgres:postgres@localhost:5432/context_builder

### Redis Container (redis-1)

**Purpose**: Serves as both a cache and message broker for Celery.

**Key Features**:
- High-performance in-memory data store
- Used as Celery's message broker for task queue
- Also used for caching frequently accessed data
- Supports pub/sub for real-time updates

**Configuration**:
- Uses official Redis 7 image
- No authentication in development setup
- Data persisted in redis_data volume

**Access**:
- Connection string: redis://localhost:6379/0

### Neo4j Container (neo4j-1)

**Purpose**: Stores and queries graph-based knowledge representations.

**Key Features**:
- Graph database for semantic context
- Stores entities, relationships, and properties extracted from documents
- Enables complex graph queries for knowledge retrieval
- Provides a browser interface for visualization

**Configuration**:
- Uses official Neo4j 5 image
- Authentication: neo4j/password
- Memory configuration optimized for development
- Anonymous usage reporting disabled
- Data persisted in neo4j_data volume

**Access**:
- Browser interface: http://localhost:7474
- Bolt connection: bolt://localhost:7687
- Credentials: neo4j/password

### Qdrant Container (qdrant-1)

**Purpose**: Vector database for storing and querying embeddings.

**Key Features**:
- High-performance vector similarity search
- Stores embeddings generated from text and other content
- Enables semantic search capabilities
- Provides REST API and gRPC interfaces

**Configuration**:
- Uses official Qdrant latest image
- No authentication in development setup
- Data persisted in qdrant_data volume

**Access**:
- REST API: http://localhost:6333
- Web dashboard: http://localhost:6333/dashboard
- gRPC interface: localhost:6334

## Container Interactions

The containers interact in the following ways:

1. **API Container**:
   - Receives requests from clients
   - Communicates with all databases for data operations
   - Sends tasks to Worker via Redis
   - Serves responses back to clients

2. **Worker Container**:
   - Receives tasks from Redis queue
   - Processes tasks asynchronously
   - Stores results in databases
   - Updates task status in Redis

3. **Flower Container**:
   - Monitors Redis for task information
   - Provides visualization of task execution

4. **Database Containers** (PostgreSQL, Neo4j, Qdrant):
   - Store different types of data based on their specialization
   - Respond to queries from API and Worker containers

5. **Redis Container**:
   - Acts as message broker between API and Worker
   - Stores task status and results
   - Provides caching for frequently accessed data

## Development Workflow

When developing with these containers:

1. Use `docker compose up` to start all services
2. Make changes to the code and the API container will automatically reload
3. Access API documentation at http://localhost:8000/docs
4. Monitor tasks with Flower at http://localhost:5555
5. Explore the knowledge graph with Neo4j Browser at http://localhost:7474
6. Visualize vector embeddings with Qdrant Dashboard at http://localhost:6333/dashboard

## Troubleshooting

Common issues and solutions:

- **API container fails to start**: Check .env file for proper configuration, especially CORS_ORIGINS format
- **Worker not processing tasks**: Verify Redis connection and Celery configuration
- **Database connection errors**: Ensure the database containers are running and credentials are correct
- **Permission issues with volumes**: Check Docker volume permissions on the host

## Production Considerations

For production deployment:

- Enable proper authentication for all services
- Configure SSL/TLS for secure communication
- Implement proper backup strategies for all databases
- Consider using managed services for databases in cloud environments
- Optimize container resources based on workload requirements
- Implement monitoring and alerting for all services 