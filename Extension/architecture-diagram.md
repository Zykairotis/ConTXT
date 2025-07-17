# ConTXT Browser Extension Architecture Diagram

```mermaid
flowchart TD
    subgraph "User Interaction"
        A[User] -->|Clicks Extension Icon| B[Popup UI]
        A -->|Right-click Context Menu| C[Context Menu]
    end

    subgraph "Extension Components"
        B -->|Send Request| D[Background Script]
        C -->|Send Request| D
        D -->|Execute on Page| E[Content Script]
        D -->|Process Content| F[Ingestion Service]
    end

    subgraph "Core Services"
        F -->|Capture Content| G[Content Capture Service]
        F -->|Send to Backend| H[API Service]
        F -->|Save Settings| I[Storage Service]
    end

    subgraph "Content Types"
        G -->|URL| J[URL Processing]
        G -->|Text| K[Text Processing]
        G -->|Screenshot| L[Screenshot Processing]
        G -->|HTML| M[HTML Processing]
        G -->|Chat| N[Chat Processing]
        G -->|File| O[File Processing]
    end

    subgraph "Backend Integration"
        H -->|API Request| P[ConTXT Backend]
        P -->|Response| H
        P -->|Store in Knowledge Graph| Q[Neo4j]
        P -->|Store Vectors| R[Qdrant]
    end
```

This diagram illustrates the architecture and data flow of the ConTXT Browser Extension, showing how user interactions trigger content capture and processing, which is then sent to the ConTXT backend for integration into the knowledge graph and vector database. 