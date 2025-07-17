"""
JSON document processor.

This module provides a processor for JSON documents.
"""
import json
import logging
from typing import Dict, List, Any, Optional, Union

from app.processors.base import BaseProcessor

logger = logging.getLogger(__name__)

class JsonProcessor(BaseProcessor):
    """
    Processor for JSON documents.
    
    This class provides methods for processing JSON documents,
    extracting structured data, and storing it in the knowledge graph
    and vector database.
    """
    
    async def process(self, content: Union[str, Dict, List], **kwargs) -> Dict[str, Any]:
        """
        Process a JSON document.
        
        Args:
            content: JSON content as string or parsed object
            **kwargs: Additional processing options
                - flatten: Whether to flatten nested JSON (default: True)
                - max_depth: Maximum depth for flattening (default: 5)
                - store_schema: Whether to store JSON schema (default: True)
                - other options from BaseProcessor
        
        Returns:
            Processing result with document ID and metadata
        """
        # Extract options
        flatten = kwargs.get("flatten", True)
        max_depth = kwargs.get("max_depth", 5)
        store_schema = kwargs.get("store_schema", True)
        document_id = kwargs.get("document_id")
        metadata = kwargs.get("metadata", {})
        
        # Update metadata
        metadata["content_type"] = "application/json"
        
        # Parse JSON if needed
        if isinstance(content, str):
            try:
                parsed_json = json.loads(content)
            except json.JSONDecodeError as e:
                logger.error(f"Invalid JSON: {e}")
                raise ValueError(f"Invalid JSON: {e}")
        else:
            parsed_json = content
        
        # Extract schema if requested
        if store_schema:
            schema = self._extract_schema(parsed_json)
            metadata["schema"] = schema
        
        # Flatten JSON if requested
        if flatten:
            flattened = self._flatten_json(parsed_json, max_depth=max_depth)
            
            # Store flattened version in metadata
            metadata["flattened"] = flattened
            
            # Create text representation for embedding
            text_representation = self._json_to_text(flattened)
        else:
            # Create text representation directly
            text_representation = self._json_to_text(parsed_json)
        
        # Use the text processor to handle the text representation
        from app.processors.text_processor import TextProcessor
        text_processor = TextProcessor()
        text_processor.metadata = self.metadata
        
        # Process the text representation
        result = await text_processor.process(
            text_representation,
            document_id=document_id,
            metadata=metadata,
            **kwargs
        )
        
        # Add JSON-specific data to the result
        result["json_keys"] = self._extract_keys(parsed_json)
        
        # Store additional relationships in Neo4j
        if result.get("document_id"):
            await self._store_json_structure(result["document_id"], parsed_json)
        
        return result
    
    def _extract_schema(self, data: Union[Dict, List]) -> Dict[str, Any]:
        """
        Extract a simple schema from JSON data.
        
        Args:
            data: JSON data
            
        Returns:
            Schema description
        """
        if isinstance(data, dict):
            schema = {}
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    schema[key] = self._extract_schema(value)
                else:
                    schema[key] = type(value).__name__
            return schema
        elif isinstance(data, list):
            if not data:
                return {"type": "array", "items": {}}
            
            # Check if all items have the same type
            item_types = set(type(item).__name__ for item in data)
            
            if len(item_types) == 1:
                item_type = next(iter(item_types))
                if item_type in ("dict", "list"):
                    # Sample the first item for nested structures
                    return {"type": "array", "items": self._extract_schema(data[0])}
                else:
                    return {"type": "array", "items": {"type": item_type}}
            else:
                return {"type": "array", "items": {"type": list(item_types)}}
        else:
            return {"type": type(data).__name__}
    
    def _flatten_json(self, data: Union[Dict, List], prefix: str = "", max_depth: int = 5, 
                     current_depth: int = 0) -> Dict[str, Any]:
        """
        Flatten nested JSON into a flat dictionary.
        
        Args:
            data: JSON data
            prefix: Key prefix for nested items
            max_depth: Maximum depth to flatten
            current_depth: Current depth in recursion
            
        Returns:
            Flattened dictionary
        """
        result = {}
        
        # Stop recursion if max depth reached
        if current_depth >= max_depth:
            return {prefix: str(data)}
        
        if isinstance(data, dict):
            for key, value in data.items():
                new_key = f"{prefix}.{key}" if prefix else key
                
                if isinstance(value, (dict, list)):
                    result.update(self._flatten_json(value, new_key, max_depth, current_depth + 1))
                else:
                    result[new_key] = value
        elif isinstance(data, list):
            for i, item in enumerate(data):
                new_key = f"{prefix}[{i}]"
                
                if isinstance(item, (dict, list)):
                    result.update(self._flatten_json(item, new_key, max_depth, current_depth + 1))
                else:
                    result[new_key] = item
        else:
            result[prefix] = data
        
        return result
    
    def _json_to_text(self, data: Union[Dict, List]) -> str:
        """
        Convert JSON to a text representation for embedding.
        
        Args:
            data: JSON data
            
        Returns:
            Text representation
        """
        if isinstance(data, dict):
            lines = []
            for key, value in data.items():
                if isinstance(value, (dict, list)):
                    lines.append(f"{key}: {json.dumps(value, indent=2)}")
                else:
                    lines.append(f"{key}: {value}")
            return "\n".join(lines)
        else:
            return json.dumps(data, indent=2)
    
    def _extract_keys(self, data: Union[Dict, List], prefix: str = "") -> List[str]:
        """
        Extract all keys from JSON data.
        
        Args:
            data: JSON data
            prefix: Key prefix for nested items
            
        Returns:
            List of keys
        """
        keys = []
        
        if isinstance(data, dict):
            for key, value in data.items():
                full_key = f"{prefix}.{key}" if prefix else key
                keys.append(full_key)
                
                if isinstance(value, (dict, list)):
                    keys.extend(self._extract_keys(value, full_key))
        elif isinstance(data, list):
            for i, item in enumerate(data):
                if isinstance(item, (dict, list)):
                    keys.extend(self._extract_keys(item, f"{prefix}[{i}]"))
        
        return keys
    
    async def _store_json_structure(self, document_id: str, data: Union[Dict, List]) -> None:
        """
        Store JSON structure in the knowledge graph.
        
        Args:
            document_id: Document ID
            data: JSON data
        """
        # Create a document node if it doesn't exist
        doc_query = """
        MERGE (d:Document {id: $id})
        ON CREATE SET d.content_type = 'application/json'
        RETURN d.id as id
        """
        
        await self.neo4j_client.run_query(doc_query, {"id": document_id})
        
        # Store the structure
        if isinstance(data, dict):
            await self._store_json_object(document_id, data, "root")
        elif isinstance(data, list):
            await self._store_json_array(document_id, data, "root")
    
    async def _store_json_object(self, document_id: str, data: Dict, path: str) -> None:
        """
        Store JSON object in the knowledge graph.
        
        Args:
            document_id: Document ID
            data: JSON object
            path: Path to the object
        """
        # Create an object node
        obj_query = """
        MATCH (d:Document {id: $document_id})
        MERGE (o:JsonObject {document_id: $document_id, path: $path})
        MERGE (d)-[:HAS_OBJECT]->(o)
        RETURN o.path as path
        """
        
        await self.neo4j_client.run_query(obj_query, {
            "document_id": document_id,
            "path": path
        })
        
        # Store each property
        for key, value in data.items():
            prop_path = f"{path}.{key}"
            
            if isinstance(value, dict):
                # Nested object
                await self._store_json_object(document_id, value, prop_path)
                
                # Create relationship
                rel_query = """
                MATCH (p:JsonObject {document_id: $document_id, path: $parent_path})
                MATCH (c:JsonObject {document_id: $document_id, path: $child_path})
                MERGE (p)-[:HAS_PROPERTY {key: $key}]->(c)
                """
                
                await self.neo4j_client.run_query(rel_query, {
                    "document_id": document_id,
                    "parent_path": path,
                    "child_path": prop_path,
                    "key": key
                })
            elif isinstance(value, list):
                # Array
                await self._store_json_array(document_id, value, prop_path)
                
                # Create relationship
                rel_query = """
                MATCH (o:JsonObject {document_id: $document_id, path: $path})
                MATCH (a:JsonArray {document_id: $document_id, path: $array_path})
                MERGE (o)-[:HAS_PROPERTY {key: $key}]->(a)
                """
                
                await self.neo4j_client.run_query(rel_query, {
                    "document_id": document_id,
                    "path": path,
                    "array_path": prop_path,
                    "key": key
                })
            else:
                # Simple value
                val_query = """
                MATCH (o:JsonObject {document_id: $document_id, path: $path})
                MERGE (v:JsonValue {
                    document_id: $document_id, 
                    path: $value_path,
                    type: $type,
                    value: $value
                })
                MERGE (o)-[:HAS_PROPERTY {key: $key}]->(v)
                """
                
                await self.neo4j_client.run_query(val_query, {
                    "document_id": document_id,
                    "path": path,
                    "value_path": prop_path,
                    "type": type(value).__name__,
                    "value": str(value),
                    "key": key
                })
    
    async def _store_json_array(self, document_id: str, data: List, path: str) -> None:
        """
        Store JSON array in the knowledge graph.
        
        Args:
            document_id: Document ID
            data: JSON array
            path: Path to the array
        """
        # Create an array node
        arr_query = """
        MATCH (d:Document {id: $document_id})
        MERGE (a:JsonArray {
            document_id: $document_id, 
            path: $path,
            length: $length
        })
        MERGE (d)-[:HAS_ARRAY]->(a)
        RETURN a.path as path
        """
        
        await self.neo4j_client.run_query(arr_query, {
            "document_id": document_id,
            "path": path,
            "length": len(data)
        })
        
        # Store each item
        for i, item in enumerate(data):
            item_path = f"{path}[{i}]"
            
            if isinstance(item, dict):
                # Object
                await self._store_json_object(document_id, item, item_path)
                
                # Create relationship
                rel_query = """
                MATCH (a:JsonArray {document_id: $document_id, path: $path})
                MATCH (o:JsonObject {document_id: $document_id, path: $item_path})
                MERGE (a)-[:HAS_ITEM {index: $index}]->(o)
                """
                
                await self.neo4j_client.run_query(rel_query, {
                    "document_id": document_id,
                    "path": path,
                    "item_path": item_path,
                    "index": i
                })
            elif isinstance(item, list):
                # Nested array
                await self._store_json_array(document_id, item, item_path)
                
                # Create relationship
                rel_query = """
                MATCH (a:JsonArray {document_id: $document_id, path: $path})
                MATCH (na:JsonArray {document_id: $document_id, path: $item_path})
                MERGE (a)-[:HAS_ITEM {index: $index}]->(na)
                """
                
                await self.neo4j_client.run_query(rel_query, {
                    "document_id": document_id,
                    "path": path,
                    "item_path": item_path,
                    "index": i
                })
            else:
                # Simple value
                val_query = """
                MATCH (a:JsonArray {document_id: $document_id, path: $path})
                MERGE (v:JsonValue {
                    document_id: $document_id, 
                    path: $item_path,
                    type: $type,
                    value: $value
                })
                MERGE (a)-[:HAS_ITEM {index: $index}]->(v)
                """
                
                await self.neo4j_client.run_query(val_query, {
                    "document_id": document_id,
                    "path": path,
                    "item_path": item_path,
                    "type": type(item).__name__,
                    "value": str(item),
                    "index": i
                }) 