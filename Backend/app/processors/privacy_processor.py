"""
Privacy-compliant document processor.

This module provides a processor wrapper that ensures documents are processed
in compliance with privacy regulations (GDPR, CCPA, etc.) by identifying and
handling sensitive information.
"""
import logging
import re
from typing import Dict, Any, List, Optional, Set, Union

from app.processors.base import BaseProcessor

logger = logging.getLogger(__name__)

class PrivacyCompliantProcessor(BaseProcessor):
    """
    Privacy-compliant processor wrapper.
    
    This processor wraps another processor and ensures that sensitive information
    is properly identified, redacted, or encrypted according to privacy requirements.
    """
    
    # Common patterns for sensitive data
    PII_PATTERNS = {
        "email": r'\b[A-Za-z0-9._%+-]+@[A-Za-z0-9.-]+\.[A-Z|a-z]{2,}\b',
        "phone": r'\b(\+\d{1,2}\s?)?\(?\d{3}\)?[\s.-]?\d{3}[\s.-]?\d{4}\b',
        "ssn": r'\b\d{3}-\d{2}-\d{4}\b',
        "credit_card": r'\b(?:\d{4}[- ]?){3}\d{4}\b',
        "ip_address": r'\b\d{1,3}\.\d{1,3}\.\d{1,3}\.\d{1,3}\b',
    }
    
    def __init__(self, 
                 base_processor: BaseProcessor,
                 redact_pii: bool = True,
                 pii_types: Optional[List[str]] = None,
                 custom_patterns: Optional[Dict[str, str]] = None,
                 **kwargs):
        """
        Initialize the privacy processor.
        
        Args:
            base_processor: The underlying processor to wrap
            redact_pii: Whether to redact personally identifiable information
            pii_types: List of PII types to redact (default: all)
            custom_patterns: Custom regex patterns for additional PII types
            **kwargs: Additional options passed to the base processor
        """
        super().__init__(**kwargs)
        self.base_processor = base_processor
        self.redact_pii = redact_pii
        self.pii_types = set(pii_types) if pii_types else set(self.PII_PATTERNS.keys())
        
        # Compile regex patterns
        self.patterns = {}
        for pii_type, pattern in self.PII_PATTERNS.items():
            if pii_type in self.pii_types:
                self.patterns[pii_type] = re.compile(pattern)
        
        # Add custom patterns
        if custom_patterns:
            for pii_type, pattern in custom_patterns.items():
                self.patterns[pii_type] = re.compile(pattern)
    
    def process(self, content: Any, metadata: Dict[str, Any] = None, **kwargs) -> Dict[str, Any]:
        """
        Process the document with privacy compliance.
        
        Args:
            content: Document content
            metadata: Document metadata
            **kwargs: Additional processing options
            
        Returns:
            Processing results with sensitive data handled appropriately
        """
        # First, let the base processor handle the content
        result = self.base_processor.process(content, metadata, **kwargs)
        
        # Then apply privacy compliance
        if self.redact_pii:
            # Track what was redacted for logging/auditing
            redacted_items = {}
            
            # Process text chunks
            if 'chunks' in result:
                for i, chunk in enumerate(result['chunks']):
                    if 'text' in chunk:
                        chunk['text'], chunk_redacted = self._redact_text(chunk['text'])
                        for pii_type, count in chunk_redacted.items():
                            redacted_items[pii_type] = redacted_items.get(pii_type, 0) + count
            
            # Process any extracted text
            if 'extracted_text' in result:
                result['extracted_text'], text_redacted = self._redact_text(result['extracted_text'])
                for pii_type, count in text_redacted.items():
                    redacted_items[pii_type] = redacted_items.get(pii_type, 0) + count
            
            # Add redaction metadata
            if redacted_items:
                if 'metadata' not in result:
                    result['metadata'] = {}
                result['metadata']['privacy'] = {
                    'redacted': True,
                    'redacted_items': redacted_items
                }
                
                logger.info(f"Redacted PII: {redacted_items}")
        
        return result
    
    def _redact_text(self, text: str) -> tuple[str, Dict[str, int]]:
        """
        Redact PII from text.
        
        Args:
            text: Text to redact
            
        Returns:
            Tuple of (redacted text, dict of redaction counts by type)
        """
        redacted_counts = {}
        
        for pii_type, pattern in self.patterns.items():
            matches = list(pattern.finditer(text))
            if matches:
                redacted_counts[pii_type] = len(matches)
                
                # Replace each match with a redaction marker
                for match in reversed(matches):  # Process in reverse to maintain indices
                    start, end = match.span()
                    replacement = f"[REDACTED:{pii_type}]"
                    text = text[:start] + replacement + text[end:]
        
        return text, redacted_counts
    
    def get_embeddings(self, text: str, **kwargs) -> List[float]:
        """
        Get embeddings for text, ensuring privacy compliance.
        
        Args:
            text: Text to embed
            **kwargs: Additional embedding options
            
        Returns:
            Text embeddings
        """
        # Redact before embedding if needed
        if self.redact_pii:
            text, _ = self._redact_text(text)
        
        return self.base_processor.get_embeddings(text, **kwargs)
    
    def create_chunks(self, text: str, **kwargs) -> List[Dict[str, Any]]:
        """
        Create chunks from text, ensuring privacy compliance.
        
        Args:
            text: Text to chunk
            **kwargs: Additional chunking options
            
        Returns:
            List of text chunks
        """
        # Let the base processor create chunks
        chunks = self.base_processor.create_chunks(text, **kwargs)
        
        # Apply redaction to each chunk if needed
        if self.redact_pii:
            for chunk in chunks:
                if 'text' in chunk:
                    chunk['text'], _ = self._redact_text(chunk['text'])
        
        return chunks
    
    def store_in_graph(self, document_id: str, metadata: Dict[str, Any], 
                      chunks: List[Dict[str, Any]], **kwargs) -> None:
        """
        Store document in graph database with privacy compliance.
        
        Args:
            document_id: Document ID
            metadata: Document metadata
            chunks: Document chunks
            **kwargs: Additional storage options
        """
        # Add privacy metadata
        if 'privacy' not in metadata:
            metadata['privacy'] = {
                'redacted': self.redact_pii,
                'pii_types_checked': list(self.pii_types)
            }
        
        # Let the base processor handle storage
        self.base_processor.store_in_graph(document_id, metadata, chunks, **kwargs)
    
    def store_in_vector_db(self, document_id: str, metadata: Dict[str, Any],
                          chunks: List[Dict[str, Any]], **kwargs) -> None:
        """
        Store document in vector database with privacy compliance.
        
        Args:
            document_id: Document ID
            metadata: Document metadata
            chunks: Document chunks
            **kwargs: Additional storage options
        """
        # Add privacy metadata
        if 'privacy' not in metadata:
            metadata['privacy'] = {
                'redacted': self.redact_pii,
                'pii_types_checked': list(self.pii_types)
            }
        
        # Let the base processor handle storage
        self.base_processor.store_in_vector_db(document_id, metadata, chunks, **kwargs) 