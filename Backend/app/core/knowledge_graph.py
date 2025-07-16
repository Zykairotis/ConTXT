"""
Knowledge Graph Manager.

This module provides an interface to the Neo4j knowledge graph,
implementing operations for storing, retrieving, and querying
knowledge representations.
"""
import uuid
from typing import Dict, List, Optional, Any, Union

from app.db.neo4j_client import Neo4jClient

class KnowledgeGraph:
    """
    Manager for knowledge graph operations.
    
    This class provides methods for interacting with the Neo4j
    knowledge graph, including querying, adding entities and relationships,
    and retrieving statistics.
    """
    
    def __init__(self):
        """Initialize the knowledge graph manager."""
        self.neo4j_client = Neo4jClient()
    
    async def query(
        self,
        query_text: str,
        query_type: str = "natural",
        limit: int = 10
    ) -> List[Dict[str, Any]]:
        """
        Query the knowledge graph.
        
        Args:
            query_text: Natural language query or Cypher query
            query_type: Type of query ('natural' or 'cypher')
            limit: Maximum number of results to return
            
        Returns:
            List of query results
        """
        if query_type == "cypher":
            # Execute Cypher query directly
            return await self.neo4j_client.run_query(query_text, {"limit": limit})
        else:
            # Convert natural language to Cypher using LLM
            cypher_query = await self._natural_to_cypher(query_text, limit)
            return await self.neo4j_client.run_query(cypher_query, {})
    
    async def _natural_to_cypher(self, natural_query: str, limit: int) -> str:
        """
        Convert natural language query to Cypher.
        
        Args:
            natural_query: Natural language query
            limit: Maximum number of results
            
        Returns:
            Cypher query string
        """
        # In a real implementation, this would use an LLM to convert
        # natural language to Cypher. This is a placeholder.
        return f"MATCH (n) RETURN n LIMIT {limit}"
    
    async def add_entity(
        self,
        entity_type: str,
        properties: Dict[str, Any]
    ) -> str:
        """
        Add an entity to the knowledge graph.
        
        Args:
            entity_type: Type of entity (e.g., 'Person', 'Document')
            properties: Entity properties
            
        Returns:
            ID of the created entity
        """
        # Generate a unique ID if not provided
        if "id" not in properties:
            properties["id"] = str(uuid.uuid4())
        
        # Create Cypher query for entity creation
        query = f"""
        CREATE (n:{entity_type} $properties)
        RETURN n.id as id
        """
        
        # Execute query
        result = await self.neo4j_client.run_query(query, {"properties": properties})
        return result[0]["id"] if result else properties["id"]
    
    async def add_relationship(
        self,
        source_id: str,
        target_id: str,
        relationship_type: str,
        properties: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Add a relationship between entities.
        
        Args:
            source_id: ID of the source entity
            target_id: ID of the target entity
            relationship_type: Type of relationship
            properties: Relationship properties
            
        Returns:
            ID of the created relationship
        """
        properties = properties or {}
        
        # Generate a unique ID if not provided
        if "id" not in properties:
            properties["id"] = str(uuid.uuid4())
        
        # Create Cypher query for relationship creation
        query = f"""
        MATCH (source), (target)
        WHERE source.id = $source_id AND target.id = $target_id
        CREATE (source)-[r:{relationship_type} $properties]->(target)
        RETURN r.id as id
        """
        
        # Execute query
        params = {
            "source_id": source_id,
            "target_id": target_id,
            "properties": properties
        }
        result = await self.neo4j_client.run_query(query, params)
        return result[0]["id"] if result else properties["id"]
    
    async def get_stats(self) -> Dict[str, Any]:
        """
        Get statistics about the knowledge graph.
        
        Returns:
            Dictionary with graph statistics
        """
        # Query for node count
        node_query = "MATCH (n) RETURN count(n) as node_count"
        node_result = await self.neo4j_client.run_query(node_query, {})
        node_count = node_result[0]["node_count"] if node_result else 0
        
        # Query for relationship count
        rel_query = "MATCH ()-[r]->() RETURN count(r) as rel_count"
        rel_result = await self.neo4j_client.run_query(rel_query, {})
        rel_count = rel_result[0]["rel_count"] if rel_result else 0
        
        # Query for node type distribution
        type_query = """
        MATCH (n)
        WITH labels(n) as labels, count(*) as count
        RETURN labels, count
        ORDER BY count DESC
        LIMIT 10
        """
        type_result = await self.neo4j_client.run_query(type_query, {})
        type_distribution = {str(r["labels"]): r["count"] for r in type_result}
        
        return {
            "node_count": node_count,
            "relationship_count": rel_count,
            "node_types": type_distribution,
            "database_name": "neo4j"
        } 