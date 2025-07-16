"""
Neo4j database client.
"""
import logging
from typing import Dict, List, Any, Optional

from neo4j import AsyncGraphDatabase
from neo4j.exceptions import ServiceUnavailable

from app.config.settings import settings

logger = logging.getLogger(__name__)

class Neo4jClient:
    """Client for interacting with Neo4j database."""
    
    def __init__(self):
        """Initialize the Neo4j client."""
        self.uri = settings.NEO4J_URI
        self.user = settings.NEO4J_USER
        self.password = settings.NEO4J_PASSWORD
        self._driver = None
    
    async def get_driver(self):
        """Get or create the Neo4j driver."""
        if self._driver is None:
            try:
                self._driver = AsyncGraphDatabase.driver(
                    self.uri, 
                    auth=(self.user, self.password)
                )
                # Test connection
                await self._driver.verify_connectivity()
                logger.info("Connected to Neo4j at %s", self.uri)
            except ServiceUnavailable as e:
                logger.error("Failed to connect to Neo4j: %s", str(e))
                raise
        return self._driver
    
    async def close(self):
        """Close the Neo4j driver."""
        if self._driver is not None:
            await self._driver.close()
            self._driver = None
            logger.info("Neo4j connection closed")
    
    async def run_query(self, query: str, params: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Run a Cypher query against Neo4j.
        
        Args:
            query: Cypher query string
            params: Query parameters
            
        Returns:
            List of results as dictionaries
        """
        driver = await self.get_driver()
        params = params or {}
        
        try:
            async with driver.session() as session:
                result = await session.run(query, params)
                records = await result.values()
                return [dict(zip(result.keys(), record)) for record in records]
        except Exception as e:
            logger.error("Neo4j query failed: %s", str(e))
            raise 