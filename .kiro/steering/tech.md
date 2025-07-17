# Technology Stack & Build System

## Backend Stack
- **Framework**: FastAPI with async/await patterns
- **Workflow Engine**: LangGraph for context engineering workflows
- **LLM Integration**: LiteLLM for multi-provider LLM access
- **Databases**: 
  - Neo4j (knowledge graphs)
  - Qdrant (vector storage)
  - PostgreSQL (structured data)
  - Redis (caching/sessions)

## Frontend Stack
- **Framework**: Next.js 14+ with App Router
- **UI Library**: Radix UI components with Tailwind CSS
- **Styling**: Tailwind CSS with custom design system
- **Theme**: Dark/light mode support via next-themes
- **Forms**: React Hook Form with Zod validation

## Development Environment
- **Python**: 3.12+ (managed via uv/pyproject.toml)
- **Node.js**: 18+ with pnpm package manager
- **Containerization**: Docker Compose for local development

## Common Commands

### Backend Development
```bash
# Setup virtual environment
uv venv
source .venv/bin/activate

# Install dependencies
uv pip install -e .

# Start services
cd Backend && docker compose up -d

# Run development server
cd Backend && python -m uvicorn app.main:app --reload --host 0.0.0.0 --port 8000

# Run tests
cd Backend && pytest
```

### Frontend Development
```bash
# Install dependencies
cd Frontend && pnpm install

# Development server
cd Frontend && pnpm dev

# Build for production
cd Frontend && pnpm build

# Lint code
cd Frontend && pnpm lint
```

### Docker Operations
```bash
# Start all services
docker compose up -d

# View logs
docker compose logs -f

# Stop services
docker compose down

# Rebuild containers
docker compose build --no-cache
```

## Key Libraries & Dependencies
- **LangGraph**: Workflow orchestration for context engineering
- **LiteLLM**: Unified LLM API interface
- **Qdrant Client**: Vector database operations
- **Neo4j Driver**: Graph database connectivity
- **Pydantic**: Data validation and settings management
- **FastAPI**: Modern async web framework