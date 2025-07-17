"""
CSV document processor.

This module provides a processor for CSV documents.
"""
import csv
import io
import logging
from typing import Dict, List, Any, Optional, Union

from app.processors.base import BaseProcessor

logger = logging.getLogger(__name__)

class CsvProcessor(BaseProcessor):
    """
    Processor for CSV documents.
    
    This class provides methods for processing CSV documents,
    extracting structured data, and storing it in the knowledge graph
    and vector database.
    """
    
    async def process(self, content: Union[str, io.TextIOBase], **kwargs) -> Dict[str, Any]:
        """
        Process a CSV document.
        
        Args:
            content: CSV content as string or file-like object
            **kwargs: Additional processing options
                - has_header: Whether the CSV has a header row (default: True)
                - delimiter: CSV delimiter (default: ',')
                - store_as_json: Whether to store as JSON (default: True)
                - max_rows: Maximum number of rows to process (default: None)
                - other options from BaseProcessor
        
        Returns:
            Processing result with document ID and metadata
        """
        # Extract options
        has_header = kwargs.get("has_header", True)
        delimiter = kwargs.get("delimiter", ",")
        store_as_json = kwargs.get("store_as_json", True)
        max_rows = kwargs.get("max_rows")
        document_id = kwargs.get("document_id")
        metadata = kwargs.get("metadata", {})
        
        # Update metadata
        metadata["content_type"] = "text/csv"
        metadata["delimiter"] = delimiter
        metadata["has_header"] = has_header
        
        # Parse CSV
        if isinstance(content, str):
            csv_data = self._parse_csv_string(content, delimiter, has_header, max_rows)
        else:
            csv_data = self._parse_csv_file(content, delimiter, has_header, max_rows)
        
        # Add CSV stats to metadata
        metadata["row_count"] = len(csv_data)
        if csv_data and isinstance(csv_data[0], dict):
            metadata["columns"] = list(csv_data[0].keys())
        elif csv_data:
            metadata["column_count"] = len(csv_data[0])
        
        # Store as JSON if requested
        if store_as_json:
            from app.processors.json_processor import JsonProcessor
            json_processor = JsonProcessor()
            json_processor.metadata = self.metadata
            
            # Process as JSON
            result = await json_processor.process(
                csv_data,
                document_id=document_id,
                metadata=metadata,
                **kwargs
            )
            
            # Add CSV-specific data
            result["csv_processed"] = True
            result["csv_row_count"] = len(csv_data)
            
            return result
        
        # Otherwise, create a text representation and process as text
        text_representation = self._csv_to_text(csv_data)
        
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
        
        # Add CSV-specific data
        result["csv_processed"] = True
        result["csv_row_count"] = len(csv_data)
        
        # Store additional relationships in Neo4j
        if result.get("document_id"):
            await self._store_csv_structure(result["document_id"], csv_data, has_header)
        
        return result
    
    def _parse_csv_string(self, content: str, delimiter: str, has_header: bool, 
                         max_rows: Optional[int] = None) -> List[Union[Dict[str, str], List[str]]]:
        """
        Parse CSV from string.
        
        Args:
            content: CSV content as string
            delimiter: CSV delimiter
            has_header: Whether the CSV has a header row
            max_rows: Maximum number of rows to process
            
        Returns:
            Parsed CSV data
        """
        # Use StringIO to create a file-like object
        with io.StringIO(content) as f:
            return self._parse_csv_file(f, delimiter, has_header, max_rows)
    
    def _parse_csv_file(self, file: io.TextIOBase, delimiter: str, has_header: bool,
                       max_rows: Optional[int] = None) -> List[Union[Dict[str, str], List[str]]]:
        """
        Parse CSV from file-like object.
        
        Args:
            file: File-like object containing CSV data
            delimiter: CSV delimiter
            has_header: Whether the CSV has a header row
            max_rows: Maximum number of rows to process
            
        Returns:
            Parsed CSV data
        """
        reader = csv.reader(file, delimiter=delimiter)
        rows = []
        
        # Read header if present
        header = next(reader) if has_header else None
        
        # Process rows
        row_count = 0
        for row in reader:
            if max_rows and row_count >= max_rows:
                break
                
            if header:
                # Create a dictionary using header as keys
                row_dict = {header[i]: value for i, value in enumerate(row) if i < len(header)}
                rows.append(row_dict)
            else:
                # Just store the row as a list
                rows.append(row)
                
            row_count += 1
        
        return rows
    
    def _csv_to_text(self, data: List[Union[Dict[str, str], List[str]]]) -> str:
        """
        Convert CSV data to a text representation for embedding.
        
        Args:
            data: Parsed CSV data
            
        Returns:
            Text representation
        """
        if not data:
            return ""
        
        lines = []
        
        # Handle dictionary rows (with header)
        if isinstance(data[0], dict):
            # Add header
            header = list(data[0].keys())
            lines.append(" | ".join(header))
            lines.append("-" * (sum(len(h) for h in header) + 3 * (len(header) - 1)))
            
            # Add rows
            for row in data:
                lines.append(" | ".join(str(row.get(h, "")) for h in header))
        else:
            # Handle list rows (without header)
            for row in data:
                lines.append(" | ".join(str(val) for val in row))
        
        return "\n".join(lines)
    
    async def _store_csv_structure(self, document_id: str, data: List[Union[Dict[str, str], List[str]]], 
                                  has_header: bool) -> None:
        """
        Store CSV structure in the knowledge graph.
        
        Args:
            document_id: Document ID
            data: Parsed CSV data
            has_header: Whether the CSV has a header row
        """
        if not data:
            return
        
        # Create a document node if it doesn't exist
        doc_query = """
        MERGE (d:Document {id: $id})
        ON CREATE SET d.content_type = 'text/csv'
        RETURN d.id as id
        """
        
        await self.neo4j_client.run_query(doc_query, {"id": document_id})
        
        # Create a CSV node
        csv_query = """
        MATCH (d:Document {id: $document_id})
        MERGE (c:CsvDocument {
            document_id: $document_id,
            row_count: $row_count,
            has_header: $has_header
        })
        MERGE (d)-[:HAS_CSV]->(c)
        RETURN c.document_id as id
        """
        
        await self.neo4j_client.run_query(csv_query, {
            "document_id": document_id,
            "row_count": len(data),
            "has_header": has_header
        })
        
        # Store header if present
        if has_header and isinstance(data[0], dict):
            header = list(data[0].keys())
            
            for i, column in enumerate(header):
                col_query = """
                MATCH (c:CsvDocument {document_id: $document_id})
                MERGE (col:CsvColumn {
                    document_id: $document_id,
                    name: $name,
                    index: $index
                })
                MERGE (c)-[:HAS_COLUMN]->(col)
                """
                
                await self.neo4j_client.run_query(col_query, {
                    "document_id": document_id,
                    "name": column,
                    "index": i
                })
        
        # Store sample rows (up to 5)
        for i, row in enumerate(data[:5]):
            row_query = """
            MATCH (c:CsvDocument {document_id: $document_id})
            CREATE (r:CsvRow {
                document_id: $document_id,
                index: $index,
                content: $content
            })
            CREATE (c)-[:HAS_ROW]->(r)
            """
            
            if isinstance(row, dict):
                content = ", ".join(f"{k}: {v}" for k, v in row.items())
            else:
                content = ", ".join(str(v) for v in row)
                
            await self.neo4j_client.run_query(row_query, {
                "document_id": document_id,
                "index": i,
                "content": content
            }) 