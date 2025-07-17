#!/bin/bash
# Docker start script for ConTXT document processing system

# Color outputs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== ConTXT Document Processing System ===${NC}"

# Check if .env file exists
if [ ! -f .env ]; then
    echo -e "${RED}Error: .env file not found. Please create .env file with required configuration.${NC}"
    echo -e "You can use .env.example as a template."
    exit 1
fi

# Check if Docker is running
docker info > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Docker is not running. Please start Docker and try again.${NC}"
    exit 1
fi

echo -e "${GREEN}Starting Docker containers...${NC}"
docker compose up -d

# Wait for services to start
echo -e "${YELLOW}Waiting for services to start...${NC}"
sleep 5

# Check container status
echo -e "\n${YELLOW}Checking container status:${NC}"
docker compose ps

echo -e "\n${YELLOW}API will be available at:${NC} http://localhost:8000"
echo -e "${YELLOW}API Documentation:${NC} http://localhost:8000/docs"
echo -e "${YELLOW}Neo4j Browser:${NC} http://localhost:7474 (neo4j/password)"
echo -e "${YELLOW}Qdrant Dashboard:${NC} http://localhost:6333/dashboard"

if docker compose ps | grep -q "contxt_flower"; then
    echo -e "${YELLOW}Celery Flower:${NC} http://localhost:5555"
fi

echo -e "\n${GREEN}System started successfully!${NC}"
echo -e "Run the following command to view logs:"
echo -e "  docker compose logs -f"
echo -e "To stop the system:"
echo -e "  docker compose down"
echo -e "To run tests:"
echo -e "  ./scripts/test_docker_system.py" 