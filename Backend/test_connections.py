"""
Test script to verify database connections.

This script tests connections to Neo4j and Qdrant databases
to ensure the basic setup is working correctly.
"""
import asyncio
import logging
from dotenv import load_dotenv

from app.db.neo4j_client import Neo4jClient
from app.db.qdrant_client import QdrantClient
from app.config.settings import settings

# Configure logging
logging.basicConfig(
    level=logging.INFO,
    format="%(asctime)s - %(name)s - %(levelname)s - %(message)s",
)
logger = logging.getLogger(__name__)

# Load environment variables
load_dotenv()

async def test_neo4j_connection():
    """Test connection to Neo4j database."""
    logger.info(f"Testing Neo4j connection to {settings.NEO4J_URI}...")
    try:
        client = Neo4jClient()
        driver = await client.get_driver()
        
        # Run a simple query
        result = await client.run_query("RETURN 'Connected to Neo4j!' as message")
        logger.info("Neo4j test result: %s", result[0]["message"])
        
        # Close connection
        await client.close()
        logger.info("Neo4j connection test successful!")
        return True
    except Exception as e:
        logger.error("Neo4j connection test failed: %s", str(e))
        return False

async def test_qdrant_connection():
    """Test connection to Qdrant database."""
    logger.info(f"Testing Qdrant connection to {settings.QDRANT_HOST}:{settings.QDRANT_PORT}...")
    try:
        client = QdrantClient()
        qdrant = client.get_client()
        
        # Check if client is connected
        collections = qdrant.get_collections()
        logger.info("Qdrant collections: %s", [c.name for c in collections.collections])
        
        # Close connection
        client.close()
        logger.info("Qdrant connection test successful!")
        return True
    except Exception as e:
        logger.error("Qdrant connection test failed: %s", str(e))
        return False

async def main():
    """Run all tests."""
    logger.info("Starting connection tests...")
    logger.info(f"Environment configuration: NEO4J_HOST={settings.NEO4J_HOST}, QDRANT_HOST={settings.QDRANT_HOST}")
    
    neo4j_success = await test_neo4j_connection()
    qdrant_success = await test_qdrant_connection()
    
    if neo4j_success and qdrant_success:
        logger.info("All connection tests passed!")
    else:
        logger.warning("Some connection tests failed!")
        if not neo4j_success:
            logger.warning("Neo4j connection failed. Check if Neo4j is running and credentials are correct.")
        if not qdrant_success:
            logger.warning("Qdrant connection failed. Check if Qdrant is running.")

if __name__ == "__main__":
    asyncio.run(main()) 