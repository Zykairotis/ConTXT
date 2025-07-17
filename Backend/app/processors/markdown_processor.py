"""
Markdown document processor.

This module provides a processor for Markdown documents.
"""
import logging
import re
from typing import Dict, List, Any, Optional, Tuple

from app.processors.text_processor import TextProcessor

logger = logging.getLogger(__name__)

class MarkdownProcessor(TextProcessor):
    """
    Processor for Markdown documents.
    
    This class extends the text processor with Markdown-specific
    processing capabilities, including header extraction and structure awareness.
    """
    
    async def process(self, content: str, **kwargs) -> Dict[str, Any]:
        """
        Process a Markdown document.
        
        Args:
            content: Markdown content to process
            **kwargs: Additional processing options
                - extract_headers: Whether to extract headers (default: True)
                - structure_aware: Whether to use structure-aware chunking (default: True)
                - other options from TextProcessor
        
        Returns:
            Processing result with document ID and metadata
        """
        # Extract options
        extract_headers = kwargs.get("extract_headers", True)
        structure_aware = kwargs.get("structure_aware", True)
        
        # Update metadata
        metadata = kwargs.get("metadata", {})
        metadata["content_type"] = "text/markdown"
        kwargs["metadata"] = metadata
        
        # Extract headers if requested
        if extract_headers:
            headers = self._extract_headers(content)
            metadata["headers"] = headers
            
            # Try to determine title from headers
            if headers and not metadata.get("title"):
                metadata["title"] = headers[0][1]
        
        # Use structure-aware chunking if requested
        if structure_aware:
            # Override the default chunking with structure-aware chunking
            original_split_text = self._split_text
            self._split_text = self._structure_aware_split
            
            # Process the document
            result = await super().process(content, **kwargs)
            
            # Restore the original chunking method
            self._split_text = original_split_text
            
            return result
        
        # Use default text processing
        return await super().process(content, **kwargs)
    
    def _extract_headers(self, markdown: str) -> List[Tuple[int, str]]:
        """
        Extract headers from Markdown content.
        
        Args:
            markdown: Markdown content
            
        Returns:
            List of (level, header) tuples
        """
        # Regular expression to match Markdown headers
        header_pattern = re.compile(r'^(#{1,6})\s+(.+)$', re.MULTILINE)
        
        # Find all headers
        headers = []
        for match in header_pattern.finditer(markdown):
            level = len(match.group(1))
            header = match.group(2).strip()
            headers.append((level, header))
        
        return headers
    
    def _structure_aware_split(self, text: str, chunk_size: int, chunk_overlap: int) -> List[str]:
        """
        Split Markdown text into chunks, respecting structural elements.
        
        Args:
            text: Markdown text to split
            chunk_size: Maximum chunk size
            chunk_overlap: Overlap between chunks
            
        Returns:
            List of text chunks
        """
        if len(text) <= chunk_size:
            return [text]
        
        # Define Markdown structural separators in order of precedence
        separators = [
            r'(?=^#{1,6}\s+.+$)',  # Headers
            r'(?=^---+$)',         # Horizontal rules
            r'(?=^```)',           # Code blocks
            r'(?=^\s*\n\s*$)',     # Blank lines
            r'(?=^[*-]\s+)',       # List items
            r'(?=^\d+\.\s+)'       # Numbered list items
        ]
        
        # Compile the regex pattern
        pattern = '|'.join(separators)
        regex = re.compile(pattern, re.MULTILINE)
        
        # Split the text into sections based on structural elements
        sections = regex.split(text)
        
        # Now combine sections into chunks respecting the chunk size
        chunks = []
        current_chunk = ""
        
        for section in sections:
            # If adding this section would exceed the chunk size and we already have content
            if len(current_chunk) + len(section) > chunk_size and current_chunk:
                chunks.append(current_chunk)
                # Start a new chunk with overlap
                overlap_start = max(0, len(current_chunk) - chunk_overlap)
                current_chunk = current_chunk[overlap_start:] + section
            else:
                current_chunk += section
        
        # Add the last chunk if it has content
        if current_chunk:
            chunks.append(current_chunk)
        
        return chunks
    
    async def _create_chunk_relationship(self, prev_chunk_id: str, next_chunk_id: str) -> None:
        """
        Create a relationship between consecutive chunks in the knowledge graph.
        
        Args:
            prev_chunk_id: ID of the previous chunk
            next_chunk_id: ID of the next chunk
        """
        # Call the parent method
        await super()._create_chunk_relationship(prev_chunk_id, next_chunk_id)
        
        # Add Markdown-specific relationship
        query = """
        MATCH (prev:Chunk {id: $prev_id})
        MATCH (next:Chunk {id: $next_id})
        CREATE (prev)-[:MARKDOWN_NEXT]->(next)
        """
        
        params = {
            "prev_id": prev_chunk_id,
            "next_id": next_chunk_id
        }
        
        await self.neo4j_client.run_query(query, params) 