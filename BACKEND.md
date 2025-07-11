# Backend Documentation

## Project Role

The backend is the core engine of the **AI Context Builder**. It is a high-performance, asynchronous system responsible for ingesting, processing, and analyzing multi-modal data. It orchestrates complex AI workflows to transform raw information into a structured knowledge graph, which is then used to generate intelligent system prompts and configuration files for various AI agents.

## Core Responsibilities

1.  **API Development:** Implement and maintain a robust RESTful API using **FastAPI**. All endpoints must be asynchronous, fully documented via OpenAPI, and use Pydantic for strict data validation.
2.  **AI Workflow Orchestration:** Design and manage complex, stateful workflows using **LangGraph**. These graphs control the entire context-building pipeline, from data ingestion to final output generation.
3.  **Data Ingestion & Processing:** Develop and maintain modular processors for a wide range of sources:
    *   **Documents:** Handle `pdf`, `json`, `csv`, `xml`, `html`, and `md` files.
    *   **Conversations:** Process exports from platforms like ChatGPT, Claude, and Grok.
    *   **Media:** Transcribe audio from video files (`mp4`, `mkv`) and YouTube links using **Whisper**.
    *   **Web Content:** Scrape and process content from user-provided URLs.
4.  **Knowledge Representation:**
    *   **Knowledge Graph:** Use the `neo4j` library to build and populate a rich knowledge graph, turning ingested data into a network of interconnected entities and relationships.
    *   **Vector Storage:** Employ the `qdrant-client` to create and store vector embeddings for powerful semantic search and retrieval capabilities.
5.  **Database Integration:** Manage data persistence and caching across multiple specialized databases:
    *   **Neo4j:** For the core knowledge graph.
    *   **Qdrant:** For vector similarity search.
    *   **PostgreSQL:** For storing structured relational data (e.g., user info, project metadata, job statuses).
    *   **Redis:** For caching, real-time messaging (WebSockets), and task queuing.
6.  **Containerization:** Define and manage all backend services using **Docker** and `docker-compose.yml` to ensure a consistent, portable, and reproducible development and production environment.

## Tech Stack & Conventions

*   **Framework:** FastAPI
*   **Language:** Python 3.10+
*   **AI Libraries:** `langchain`, `langgraph`, `cognee`
*   **Databases:** `neo4j`, `qdrant-client`, `psycopg2` (or `asyncpg`), `redis`
*   **Data Handling:** Pydantic, Pandas, BeautifulSoup, `python-multipart`
*   **Audio Processing:** `openai-whisper`
*   **Asynchronicity:** Heavily utilize `async`/`await` for all I/O-bound operations to ensure high performance.
*   **Modularity:** Strictly adhere to the project structure. New logic must be placed in the appropriate directories (`/agents`, `/processors`, `/knowledge`).
*   **Configuration:** All credentials, API keys, and settings must be managed via environment variables (e.g., loaded from a `.env` file). Nothing should be hardcoded.

## Getting Started

1.  Navigate to the `Backend` directory:
    ```bash
    cd Backend
    ```
2.  Create and activate a virtual environment:
    ```bash
    python -m venv venv
    source venv/bin/activate
    ```
3.  Install the required dependencies:
    ```bash
    pip install -r requirements.txt
    ```
4.  Set up your environment variables by copying the example file:
    ```bash
    cp .env.example .env
    ```
5.  Fill in the necessary credentials in the `.env` file.
6.  Run the development server:
    ```bash
    uvicorn main:app --reload
    ```
7.  The API will be available at [http://localhost:8000](http://localhost:8000), with interactive documentation at [http://localhost:8000/docs](http://localhost:8000/docs).
