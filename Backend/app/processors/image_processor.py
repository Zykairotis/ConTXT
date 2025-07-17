"""
Image processor.

This module provides a processor for image files.
"""
import base64
import io
import logging
import os
from typing import Dict, List, Any, Optional, Union
from pathlib import Path

from app.processors.base import BaseProcessor

logger = logging.getLogger(__name__)

class ImageProcessor(BaseProcessor):
    """
    Processor for image files.
    
    This class provides methods for processing image files,
    extracting content, and storing it in the knowledge graph and vector database.
    """
    
    async def process(self, content: Union[str, bytes, Path], **kwargs) -> Dict[str, Any]:
        """
        Process an image file.
        
        Args:
            content: Image content as file path, bytes, or base64 string
            **kwargs: Additional processing options
                - extract_text: Whether to extract text from the image (default: True)
                - extract_objects: Whether to extract objects from the image (default: True)
                - embedding_model: Model to use for image embeddings (default: clip-vit-large-patch14)
                - document_id: Optional document ID
                - metadata: Optional metadata dictionary
        
        Returns:
            Processing result with document ID and metadata
        """
        # Extract options
        extract_text = kwargs.get("extract_text", True)
        extract_objects = kwargs.get("extract_objects", True)
        embedding_model = kwargs.get("embedding_model", "clip-vit-large-patch14")
        document_id = kwargs.get("document_id")
        metadata = kwargs.get("metadata", {})
        
        # Update metadata
        metadata["content_type"] = "image"
        
        # Load image content
        image_bytes = await self._load_image_content(content)
        
        # Extract text if requested
        if extract_text:
            text = await self._extract_text_from_image(image_bytes)
            metadata["extracted_text"] = text
        else:
            text = ""
        
        # Extract objects if requested
        if extract_objects:
            objects = await self._extract_objects_from_image(image_bytes)
            metadata["detected_objects"] = objects
        
        # Generate image embedding
        image_embedding = await self._generate_image_embedding(image_bytes, model=embedding_model)
        
        # Store in vector database
        vector_id = await self.store_in_vector_db(image_embedding, metadata)
        
        # Store in knowledge graph
        kg_id = await self._store_image_in_knowledge_graph(document_id, metadata)
        
        # If text was extracted, process it as text
        text_result = None
        if extract_text and text:
            from app.processors.text_processor import TextProcessor
            text_processor = TextProcessor()
            
            # Process the extracted text
            text_result = await text_processor.process(
                text,
                document_id=f"{document_id}_text" if document_id else None,
                metadata={
                    "source_type": "image_text",
                    "source_image_id": document_id,
                    "content_type": "text/plain"
                }
            )
            
            # Create relationship between image and extracted text
            if document_id and text_result.get("document_id"):
                await self._create_image_text_relationship(document_id, text_result["document_id"])
        
        return {
            "document_id": document_id,
            "knowledge_graph_id": kg_id,
            "vector_id": vector_id,
            "metadata": metadata,
            "extracted_text": text if extract_text else None,
            "detected_objects": objects if extract_objects else None,
            "text_processing_result": text_result
        }
    
    async def _load_image_content(self, content: Union[str, bytes, Path]) -> bytes:
        """
        Load image content from various sources.
        
        Args:
            content: Image content as file path, bytes, or base64 string
            
        Returns:
            Image bytes
        """
        if isinstance(content, bytes):
            return content
        elif isinstance(content, (str, Path)):
            path = Path(content)
            if path.exists():
                # Load from file
                with open(path, "rb") as f:
                    return f.read()
            elif isinstance(content, str) and content.startswith(("data:image", "base64:")):
                # Base64 encoded image
                if content.startswith("data:image"):
                    # Extract the base64 part from data URL
                    _, base64_data = content.split(",", 1)
                else:
                    # Remove the "base64:" prefix
                    base64_data = content[7:]
                
                return base64.b64decode(base64_data)
        
        raise ValueError("Invalid image content format")
    
    async def _extract_text_from_image(self, image_bytes: bytes) -> str:
        """
        Extract text from an image using OCR.
        
        Args:
            image_bytes: Image content as bytes
            
        Returns:
            Extracted text
        """
        # Placeholder for actual OCR implementation
        # In a real implementation, this would use an OCR library or API
        logger.info("Extracting text from image (placeholder)")
        
        # Return a placeholder result
        return "Sample extracted text from image"
    
    async def _extract_objects_from_image(self, image_bytes: bytes) -> List[Dict[str, Any]]:
        """
        Extract objects from an image using object detection.
        
        Args:
            image_bytes: Image content as bytes
            
        Returns:
            List of detected objects with bounding boxes
        """
        # Placeholder for actual object detection implementation
        # In a real implementation, this would use a computer vision API
        logger.info("Extracting objects from image (placeholder)")
        
        # Return placeholder results
        return [
            {"label": "person", "confidence": 0.95, "box": [10, 10, 100, 200]},
            {"label": "car", "confidence": 0.85, "box": [150, 50, 300, 150]}
        ]
    
    async def _generate_image_embedding(self, image_bytes: bytes, model: str) -> List[float]:
        """
        Generate embedding for an image.
        
        Args:
            image_bytes: Image content as bytes
            model: Embedding model to use
            
        Returns:
            Vector embedding
        """
        # Placeholder for actual image embedding generation
        # In a real implementation, this would call an embedding API
        logger.info(f"Generating image embedding with model: {model}")
        
        # Return a mock embedding (would be replaced with actual API call)
        return [0.0] * 512  # CLIP embeddings are typically 512 dimensions
    
    async def _store_image_in_knowledge_graph(self, document_id: str, metadata: Dict[str, Any]) -> str:
        """
        Store image metadata in the knowledge graph.
        
        Args:
            document_id: Document ID
            metadata: Image metadata
            
        Returns:
            ID of the stored node
        """
        # Create an image node
        query = """
        CREATE (i:Image {
            id: $id,
            content_type: $content_type,
            width: $width,
            height: $height,
            format: $format,
            created_at: $created_at
        })
        RETURN i.id as id
        """
        
        params = {
            "id": document_id,
            "content_type": metadata.get("content_type", "image"),
            "width": metadata.get("width", 0),
            "height": metadata.get("height", 0),
            "format": metadata.get("format", "unknown"),
            "created_at": metadata.get("processed_at")
        }
        
        result = await self.neo4j_client.run_query(query, params)
        
        # Store detected objects if available
        if "detected_objects" in metadata:
            await self._store_image_objects(document_id, metadata["detected_objects"])
        
        return result[0]["id"] if result else None
    
    async def _store_image_objects(self, image_id: str, objects: List[Dict[str, Any]]) -> None:
        """
        Store detected objects in the knowledge graph.
        
        Args:
            image_id: Image ID
            objects: List of detected objects
        """
        for i, obj in enumerate(objects):
            # Create an object node
            query = """
            MATCH (i:Image {id: $image_id})
            CREATE (o:ImageObject {
                id: $id,
                image_id: $image_id,
                label: $label,
                confidence: $confidence,
                box_x: $box_x,
                box_y: $box_y,
                box_width: $box_width,
                box_height: $box_height
            })
            CREATE (i)-[:CONTAINS_OBJECT]->(o)
            """
            
            box = obj.get("box", [0, 0, 0, 0])
            
            params = {
                "id": f"{image_id}_object_{i}",
                "image_id": image_id,
                "label": obj.get("label", "unknown"),
                "confidence": obj.get("confidence", 0.0),
                "box_x": box[0] if len(box) > 0 else 0,
                "box_y": box[1] if len(box) > 1 else 0,
                "box_width": box[2] if len(box) > 2 else 0,
                "box_height": box[3] if len(box) > 3 else 0
            }
            
            await self.neo4j_client.run_query(query, params)
    
    async def _create_image_text_relationship(self, image_id: str, text_id: str) -> None:
        """
        Create a relationship between an image and extracted text.
        
        Args:
            image_id: Image ID
            text_id: Text document ID
        """
        query = """
        MATCH (i:Image {id: $image_id})
        MATCH (t:Document {id: $text_id})
        CREATE (i)-[:HAS_TEXT]->(t)
        """
        
        params = {
            "image_id": image_id,
            "text_id": text_id
        }
        
        await self.neo4j_client.run_query(query, params) 