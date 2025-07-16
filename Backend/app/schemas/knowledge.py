"""
Pydantic models for knowledge graph operations.
"""
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field

class GraphQueryRequest(BaseModel):
    """Request model for querying the knowledge graph."""
    query: str = Field(..., description="Query text or Cypher query")
    query_type: str = Field("natural", description="Query type: 'natural' or 'cypher'")
    limit: Optional[int] = Field(10, description="Maximum number of results")
    include_metadata: bool = Field(False, description="Include metadata in response")

class GraphQueryResult(BaseModel):
    """A single result from a knowledge graph query."""
    node_id: str
    node_type: str
    properties: Dict[str, Any]
    relationships: Optional[List[Dict[str, Any]]] = None

class GraphQueryResponse(BaseModel):
    """Response model for knowledge graph queries."""
    results: List[GraphQueryResult]
    count: int = Field(..., description="Number of results returned")
    metadata: Optional[Dict[str, Any]] = None

class EntityRequest(BaseModel):
    """Request model for adding an entity to the knowledge graph."""
    entity_type: str = Field(..., description="Type of entity (e.g., 'Person', 'Document')")
    properties: Dict[str, Any] = Field(..., description="Entity properties")
    
class RelationshipRequest(BaseModel):
    """Request model for adding a relationship to the knowledge graph."""
    source_id: str = Field(..., description="ID of the source entity")
    target_id: str = Field(..., description="ID of the target entity")
    relationship_type: str = Field(..., description="Type of relationship (e.g., 'KNOWS', 'CONTAINS')")
    properties: Optional[Dict[str, Any]] = Field({}, description="Relationship properties") 