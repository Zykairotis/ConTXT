"""
Text document processor.

This module provides a processor for plain text documents.
"""
import logging
import uuid
from datetime import datetime
from typing import Dict, List, Any, Optional

from app.processors.base import BaseProcessor

logger = logging.getLogger(__name__)

class TextProcessor(BaseProcessor):
    """
    Processor for plain text documents.
    
    This class provides methods for processing plain text documents,
    extracting content, and storing it in the knowledge graph and vector database.
    """
    
    async def process(self, content: str, **kwargs) -> Dict[str, Any]:
        """
        Process a text document.
        
        Args:
            content: Text content to process
            **kwargs: Additional processing options
                - chunk_size: Size of text chunks (default: 1024)
                - chunk_overlap: Overlap between chunks (default: 128)
                - embedding_model: Model to use for embeddings (default: text-embedding-3-large)
                - document_id: Optional document ID
                - metadata: Optional metadata dictionary
        
        Returns:
            Processing result with document ID and metadata
        """
        # Extract options
        chunk_size = kwargs.get("chunk_size", 1024)
        chunk_overlap = kwargs.get("chunk_overlap", 128)
        embedding_model = kwargs.get("embedding_model", "text-embedding-3-large")
        document_id = kwargs.get("document_id", str(uuid.uuid4()))
        metadata = kwargs.get("metadata", {})
        
        # Merge with processor metadata
        metadata.update(self.metadata)
        metadata["content_type"] = "text/plain"
        metadata["processed_at"] = datetime.now().isoformat()
        metadata["id"] = document_id
        
        # Extract text if needed
        if not isinstance(content, str):
            content = await self.extract_text(content)
        
        # Split into chunks
        chunks = self._split_text(content, chunk_size, chunk_overlap)
        logger.info(f"Split text into {len(chunks)} chunks")
        
        # Process each chunk
        chunk_ids = []
        for i, chunk in enumerate(chunks):
            # Generate embedding
            embedding = await self.generate_embeddings(chunk, model=embedding_model)
            
            # Prepare chunk metadata
            chunk_metadata = metadata.copy()
            chunk_metadata["chunk_index"] = i
            chunk_metadata["chunk_total"] = len(chunks)
            chunk_metadata["chunk_id"] = f"{document_id}_chunk_{i}"
            chunk_metadata["text_snippet"] = chunk[:100] + "..." if len(chunk) > 100 else chunk
            
            # Store in vector database
            chunk_id = await self.store_in_vector_db(embedding, chunk_metadata)
            chunk_ids.append(chunk_id)
            
            # Store relationship in knowledge graph if it's not the first chunk
            if i > 0:
                await self._create_chunk_relationship(chunk_ids[i-1], chunk_id)
        
        # Store document in knowledge graph
        kg_id = await self.store_in_knowledge_graph({
            "id": document_id,
            "title": metadata.get("title", "Text Document"),
            "content_type": "text/plain",
            "chunk_count": len(chunks),
            "chunk_ids": chunk_ids
        })
        
        return {
            "document_id": document_id,
            "knowledge_graph_id": kg_id,
            "chunk_count": len(chunks),
            "chunk_ids": chunk_ids,
            "metadata": metadata
        }
    
    def _split_text(self, text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
        """
        Split text into overlapping chunks.
        
        Args:
            text: Text to split
            chunk_size: Maximum chunk size
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        if len(text) <= chunk_size:
            return [text]
        
        chunks = []
        start = 0
        
        while start < len(text):
            # Find the end of the chunk
            end = start + chunk_size
            
            # Adjust end to avoid splitting words
            if end < len(text):
                # Try to find a natural break point
                for separator in ["\n\n", "\n", ". ", " "]:
                    pos = text.rfind(separator, start, end)
                    if pos > start:
                        end = pos + len(separator)
                        break
            
            # Add the chunk
            chunks.append(text[start:end])
            
            # Move to next chunk with overlap
            start = end - chunk_overlap
        
        return chunks
    
    async def _create_chunk_relationship(self, prev_chunk_id: str, next_chunk_id: str) -> None:
        """
        Create a relationship between consecutive chunks in the knowledge graph.
        
        Args:
            prev_chunk_id: ID of the previous chunk
            next_chunk_id: ID of the next chunk
        """
        query = """
        MATCH (prev:Chunk {id: $prev_id})
        MATCH (next:Chunk {id: $next_id})
        CREATE (prev)-[:NEXT]->(next)
        """
        
        params = {
            "prev_id": prev_chunk_id,
            "next_id": next_chunk_id
        }
        
        await self.neo4j_client.run_query(query, params) 