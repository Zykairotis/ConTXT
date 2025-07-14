"""
Knowledge Graph Manager for Neo4j integration.
"""
from typing import Any, Dict, List, Optional, Union

from neo4j import AsyncGraphDatabase, AsyncSession

from Backend.config.settings import settings


class KnowledgeGraphManager:
    """Manager for Neo4j knowledge graph operations."""
    
    def __init__(self):
        """Initialize the Knowledge Graph Manager."""
        self.driver = AsyncGraphDatabase.driver(
            settings.NEO4J_URI,
            auth=(settings.NEO4J_USER, settings.NEO4J_PASSWORD),
        )
    
    async def close(self):
        """Close the Neo4j driver."""
        await self.driver.close()
    
    async def get_session(self) -> AsyncSession:
        """
        Get a Neo4j session.
        
        Returns:
            AsyncSession: A Neo4j session.
        """
        return self.driver.session(database=settings.NEO4J_DATABASE)
    
    async def create_entity(
        self, entity_type: str, properties: Dict[str, Any]
    ) -> Dict[str, Any]:
        """
        Create an entity in the knowledge graph.
        
        Args:
            entity_type: The type of entity to create.
            properties: The properties of the entity.
            
        Returns:
            Dict[str, Any]: The created entity.
        """
        async with await self.get_session() as session:
            result = await session.run(
                f"CREATE (e:{entity_type} $properties) RETURN e",
                properties=properties,
            )
            record = await result.single()
            return record["e"]
    
    async def create_relationship(
        self,
        from_entity_id: str,
        to_entity_id: str,
        relationship_type: str,
        properties: Optional[Dict[str, Any]] = None,
    ) -> Dict[str, Any]:
        """
        Create a relationship between two entities.
        
        Args:
            from_entity_id: The ID of the source entity.
            to_entity_id: The ID of the target entity.
            relationship_type: The type of relationship.
            properties: Optional properties for the relationship.
            
        Returns:
            Dict[str, Any]: The created relationship.
        """
        properties = properties or {}
        async with await self.get_session() as session:
            result = await session.run(
                f"""
                MATCH (a), (b)
                WHERE id(a) = $from_id AND id(b) = $to_id
                CREATE (a)-[r:{relationship_type} $properties]->(b)
                RETURN r
                """,
                from_id=from_entity_id,
                to_id=to_entity_id,
                properties=properties,
            )
            record = await result.single()
            return record["r"]
    
    async def query(self, cypher_query: str, parameters: Optional[Dict[str, Any]] = None) -> List[Dict[str, Any]]:
        """
        Execute a Cypher query.
        
        Args:
            cypher_query: The Cypher query to execute.
            parameters: Optional parameters for the query.
            
        Returns:
            List[Dict[str, Any]]: The query results.
        """
        parameters = parameters or {}
        async with await self.get_session() as session:
            result = await session.run(cypher_query, parameters)
            return [record.data() for record in await result.fetch_all()] 