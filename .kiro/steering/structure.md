# Project Structure & Organization

## Repository Layout
```
├── Backend/                 # FastAPI backend application
├── Frontend/               # Next.js frontend application  
├── Extension/              # Browser extension (planned)
├── .kiro/                  # Kiro AI assistant configuration
├── .taskmaster/            # Task management and workflow
└── logs/                   # Application logs
```

## Backend Structure (`Backend/`)
```
Backend/
├── app/
│   ├── api/
│   │   ├── endpoints/      # API route handlers
│   │   └── router.py       # Main API router
│   ├── config/
│   │   └── settings.py     # Application configuration
│   ├── core/               # Core business logic
│   │   ├── context_engine.py
│   │   ├── ingestion.py
│   │   └── knowledge_graph.py
│   ├── db/                 # Database clients
│   │   ├── neo4j_client.py
│   │   └── qdrant_client.py
│   ├── schemas/            # Pydantic models
│   ├── models/             # Database models
│   ├── processors/         # Data processing modules
│   └── utils/              # Utility functions
├── docker-compose.yml      # Development services
├── requirements.txt        # Python dependencies
└── Dockerfile             # Container definition
```

## Frontend Structure (`Frontend/`)
```
Frontend/
├── app/                    # Next.js App Router
│   ├── api/               # API routes
│   ├── globals.css        # Global styles
│   ├── layout.tsx         # Root layout
│   └── page.tsx           # Home page
├── components/            # React components
│   ├── ui/               # Reusable UI components (Radix)
│   └── *.tsx             # Feature components
├── hooks/                # Custom React hooks
├── lib/                  # Utility libraries
├── utils/                # Helper functions
├── public/               # Static assets
└── styles/               # Additional stylesheets
```

## Configuration Files
- **Environment**: `.env` files for local configuration
- **Python**: `pyproject.toml` for dependency management
- **Node.js**: `package.json` with pnpm lockfile
- **Docker**: `docker-compose.yml` for service orchestration
- **TypeScript**: `tsconfig.json` for frontend type checking
- **Tailwind**: `tailwind.config.ts` for styling configuration

## Key Conventions

### File Naming
- **Python**: snake_case for modules and functions
- **TypeScript**: kebab-case for files, PascalCase for components
- **API Routes**: RESTful naming (`/api/v1/resource`)

### Code Organization
- **Separation of Concerns**: Clear boundaries between API, business logic, and data layers
- **Async Patterns**: Use async/await throughout FastAPI backend
- **Type Safety**: Pydantic models for Python, TypeScript for frontend
- **Component Structure**: Atomic design principles for UI components

### Database Patterns
- **Neo4j**: Graph relationships for knowledge connections
- **Qdrant**: Vector embeddings for semantic search
- **Configuration**: Environment-based connection strings
- **Migrations**: Version-controlled schema changes

### API Design
- **RESTful**: Standard HTTP methods and status codes
- **Validation**: Pydantic schemas for request/response
- **Error Handling**: Consistent error response format
- **Documentation**: Auto-generated OpenAPI/Swagger docs