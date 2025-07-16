#!/bin/bash

# Start Docker services
echo "Starting Neo4j and Qdrant services..."
docker compose up -d

# Wait for services to be ready
echo "Waiting for services to be ready..."
sleep 5

# Check if services are running
echo "Checking services status..."
docker compose ps

echo "Services should now be available at:"
echo "- Neo4j: http://localhost:7474 (Browser interface)"
echo "- Qdrant: http://localhost:6333/dashboard (Web dashboard)"

echo "You can now run the application with:"
echo "python run.py"

echo "To test database connections, run:"
echo "python test_connections.py" 