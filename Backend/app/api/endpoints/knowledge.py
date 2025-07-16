"""
API endpoints for knowledge graph operations.
"""
from fastapi import APIRouter, Depends, HTTPException
from typing import Dict, List, Optional, Any

from app.core.knowledge_graph import KnowledgeGraph
from app.schemas.knowledge import (
    GraphQueryRequest,
    GraphQueryResponse,
    EntityRequest,
    RelationshipRequest
)

router = APIRouter()

@router.post("/query", response_model=GraphQueryResponse)
async def query_knowledge_graph(request: GraphQueryRequest):
    """
    Query the knowledge graph for information.
    
    This endpoint allows querying the Neo4j knowledge graph using
    natural language or Cypher queries.
    """
    try:
        kg = KnowledgeGraph()
        results = await kg.query(
            query_text=request.query,
            query_type=request.query_type,
            limit=request.limit or 10
        )
        return GraphQueryResponse(results=results)
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Knowledge graph query failed: {str(e)}")

@router.post("/entity", response_model=Dict[str, str])
async def add_entity(request: EntityRequest):
    """
    Add an entity to the knowledge graph.
    
    This endpoint adds a new entity node to the Neo4j knowledge graph.
    """
    try:
        kg = KnowledgeGraph()
        entity_id = await kg.add_entity(
            entity_type=request.entity_type,
            properties=request.properties
        )
        return {"entity_id": entity_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add entity: {str(e)}")

@router.post("/relationship", response_model=Dict[str, str])
async def add_relationship(request: RelationshipRequest):
    """
    Add a relationship between entities in the knowledge graph.
    
    This endpoint creates a relationship between two entities in the Neo4j graph.
    """
    try:
        kg = KnowledgeGraph()
        relationship_id = await kg.add_relationship(
            source_id=request.source_id,
            target_id=request.target_id,
            relationship_type=request.relationship_type,
            properties=request.properties
        )
        return {"relationship_id": relationship_id}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to add relationship: {str(e)}")

@router.get("/stats", response_model=Dict[str, Any])
async def get_knowledge_graph_stats():
    """Get statistics about the knowledge graph."""
    try:
        kg = KnowledgeGraph()
        stats = await kg.get_stats()
        return stats
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Failed to get graph statistics: {str(e)}") 