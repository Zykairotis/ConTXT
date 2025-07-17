#!/bin/bash
# Docker stop script for ConTXT document processing system

# Color outputs
GREEN='\033[0;32m'
YELLOW='\033[1;33m'
RED='\033[0;31m'
NC='\033[0m' # No Color

echo -e "${YELLOW}=== Stopping ConTXT Document Processing System ===${NC}"

# Check if Docker is running
docker info > /dev/null 2>&1
if [ $? -ne 0 ]; then
    echo -e "${RED}Error: Docker is not running.${NC}"
    exit 1
fi

# Check if test data directory exists and clean it up
if [ -d "test_data" ]; then
    echo -e "${YELLOW}Cleaning up test data...${NC}"
    rm -rf test_data
fi

# Ask if volumes should be removed
read -p "Do you want to remove all data volumes as well? (y/N): " remove_volumes

if [ "$remove_volumes" = "y" ] || [ "$remove_volumes" = "Y" ]; then
    echo -e "${YELLOW}Stopping containers and removing volumes...${NC}"
    docker compose down -v
    echo -e "${GREEN}Containers stopped and volumes removed.${NC}"
else
    echo -e "${YELLOW}Stopping containers...${NC}"
    docker compose down
    echo -e "${GREEN}Containers stopped. Data volumes preserved.${NC}"
fi

echo -e "\n${GREEN}System shutdown complete!${NC}" 