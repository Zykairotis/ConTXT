"""
Qdrant vector database client.
"""
import logging
from typing import Dict, List, Any, Optional, Union

from qdrant_client import QdrantClient as QClient
from qdrant_client.http import models as qdrant_models

from app.config.settings import settings

logger = logging.getLogger(__name__)

class QdrantClient:
    """Client for interacting with Qdrant vector database."""
    
    def __init__(self):
        """Initialize the Qdrant client."""
        self.host = settings.QDRANT_HOST
        self.port = settings.QDRANT_PORT
        self.collection = settings.QDRANT_COLLECTION
        self._client = None
    
    def get_client(self):
        """Get or create the Qdrant client."""
        if self._client is None:
            try:
                self._client = QClient(host=self.host, port=self.port)
                logger.info("Connected to Qdrant at %s:%s", self.host, self.port)
            except Exception as e:
                logger.error("Failed to connect to Qdrant: %s", str(e))
                raise
        return self._client
    
    def close(self):
        """Close the Qdrant client."""
        if self._client is not None:
            self._client = None
            logger.info("Qdrant connection closed")
    
    async def ensure_collection(self, vector_size: int = 1536):
        """
        Ensure the collection exists, creating it if necessary.
        
        Args:
            vector_size: Size of vectors to store (default: 1536 for OpenAI embeddings)
        """
        client = self.get_client()
        collections = client.get_collections().collections
        collection_names = [c.name for c in collections]
        
        if self.collection not in collection_names:
            logger.info("Creating Qdrant collection: %s", self.collection)
            client.create_collection(
                collection_name=self.collection,
                vectors_config=qdrant_models.VectorParams(
                    size=vector_size,
                    distance=qdrant_models.Distance.COSINE
                )
            )
    
    async def store_vectors(
        self,
        vectors: List[List[float]],
        metadata: List[Dict[str, Any]],
        ids: Optional[List[str]] = None
    ) -> List[str]:
        """
        Store vectors in the collection.
        
        Args:
            vectors: List of vector embeddings
            metadata: List of metadata dictionaries
            ids: Optional list of IDs
            
        Returns:
            List of stored vector IDs
        """
        client = self.get_client()
        
        # Ensure collection exists
        await self.ensure_collection(len(vectors[0]))
        
        # Prepare points
        points = []
        result_ids = []
        
        for i, (vector, meta) in enumerate(zip(vectors, metadata)):
            point_id = ids[i] if ids and i < len(ids) else str(i)
            result_ids.append(point_id)
            
            points.append(
                qdrant_models.PointStruct(
                    id=point_id,
                    vector=vector,
                    payload=meta
                )
            )
        
        # Upsert points
        client.upsert(
            collection_name=self.collection,
            points=points
        )
        
        return result_ids
    
    async def search_vectors(
        self,
        query_vector: List[float],
        limit: int = 10,
        filter_dict: Optional[Dict[str, Any]] = None
    ) -> List[Dict[str, Any]]:
        """
        Search for similar vectors.
        
        Args:
            query_vector: Query vector embedding
            limit: Maximum number of results
            filter_dict: Optional filter dictionary
            
        Returns:
            List of search results with metadata
        """
        client = self.get_client()
        
        # Convert filter dict to Qdrant filter if provided
        filter_obj = None
        if filter_dict:
            filter_obj = qdrant_models.Filter(
                must=[
                    qdrant_models.FieldCondition(
                        key=key,
                        match=qdrant_models.MatchValue(value=value)
                    )
                    for key, value in filter_dict.items()
                ]
            )
        
        # Search
        search_result = client.search(
            collection_name=self.collection,
            query_vector=query_vector,
            limit=limit,
            query_filter=filter_obj
        )
        
        # Format results
        results = []
        for hit in search_result:
            result = {
                "id": hit.id,
                "score": hit.score,
                "payload": hit.payload
            }
            results.append(result)
        
        return results 