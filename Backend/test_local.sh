#!/bin/bash

# Set environment variables for local testing
export NEO4J_HOST=localhost
export QDRANT_HOST=localhost
export NEO4J_PORT=7687
export QDRANT_PORT=6333

# Display configuration
echo "Testing with configuration:"
echo "- NEO4J_HOST: $NEO4J_HOST"
echo "- QDRANT_HOST: $QDRANT_HOST"
echo "- NEO4J_PORT: $NEO4J_PORT"
echo "- QDRANT_PORT: $QDRANT_PORT"
echo ""

# Run the connection test
echo "Running connection tests with localhost configuration..."
python test_connections.py 