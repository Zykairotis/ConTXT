#!/bin/bash

# Set environment variables for Docker testing
export NEO4J_HOST=neo4j
export QDRANT_HOST=qdrant
export NEO4J_PORT=7687
export QDRANT_PORT=6333

# Display configuration
echo "Testing with Docker configuration:"
echo "- NEO4J_HOST: $NEO4J_HOST"
echo "- QDRANT_HOST: $QDRANT_HOST"
echo "- NEO4J_PORT: $NEO4J_PORT"
echo "- QDRANT_PORT: $QDRANT_PORT"
echo ""

# Run the connection test
echo "Running connection tests with Docker configuration..."
echo "Note: This will only work when running inside Docker network!"
python test_connections.py 