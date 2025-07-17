"""
Document processor factory.

This module provides a factory for creating document processors
based on content type, file type, and processing requirements.
It integrates standard processors with enhanced AI capabilities.
"""
import logging
import os
from typing import Dict, Any, Optional, Type, Union, List
from pathlib import Path

# Import base processor
from app.processors.base import BaseProcessor

# Import standard processors
from app.processors.text_processor import TextProcessor
from app.processors.markdown_processor import MarkdownProcessor
from app.processors.json_processor import JsonProcessor
from app.processors.csv_processor import CsvProcessor
from app.processors.image_processor import ImageProcessor
from app.processors.pdf_processor import PDFProcessor
from app.processors.html_processor import HTMLProcessor
from app.processors.code_processor import CodeProcessor
from app.processors.privacy_processor import PrivacyCompliantProcessor

logger = logging.getLogger(__name__)

class ProcessorFactory:
    """
    Factory for creating document processors.
    
    This class provides methods for creating the appropriate processor
    based on content type, file extension, or specific processing needs.
    Support standard and AI-enhanced document processing modes.
    """
    
    # Mapping of file extensions to processor classes
    EXTENSION_MAPPING = {
        # Text and documents
        ".txt": TextProcessor,
        ".md": MarkdownProcessor,
        ".json": JsonProcessor,
        ".csv": CsvProcessor,
        ".pdf": PDFProcessor,
        ".html": HTMLProcessor,
        ".htm": HTMLProcessor,
        
        # Images
        ".png": ImageProcessor,
        ".jpg": ImageProcessor,
        ".jpeg": ImageProcessor,
        ".gif": ImageProcessor,
        ".bmp": ImageProcessor,
        ".webp": ImageProcessor,
        
        # Code files
        ".py": CodeProcessor,
        ".js": CodeProcessor,
        ".ts": CodeProcessor,
        ".jsx": CodeProcessor,
        ".tsx": CodeProcessor,
        ".java": CodeProcessor,
        ".c": CodeProcessor,
        ".cpp": CodeProcessor,
        ".h": CodeProcessor,
        ".hpp": CodeProcessor,
        ".go": CodeProcessor,
        ".rs": CodeProcessor,
        ".rb": CodeProcessor,
        ".php": CodeProcessor,
        ".swift": CodeProcessor,
        ".kt": CodeProcessor,
        ".cs": CodeProcessor,
    }
    
    # Mapping of content types to processor classes
    CONTENT_TYPE_MAPPING = {
        # Text and documents
        "text/plain": TextProcessor,
        "text/markdown": MarkdownProcessor,
        "application/json": JsonProcessor,
        "text/csv": CsvProcessor,
        "application/pdf": PDFProcessor,
        "text/html": HTMLProcessor,
        
        # Images
        "image/png": ImageProcessor,
        "image/jpeg": ImageProcessor,
        "image/gif": ImageProcessor,
        "image/bmp": ImageProcessor,
        "image/webp": ImageProcessor,
        
        # Code files
        "text/x-python": CodeProcessor,
        "application/javascript": CodeProcessor,
        "text/javascript": CodeProcessor,
        "application/typescript": CodeProcessor,
        "text/x-java": CodeProcessor,
        "text/x-c": CodeProcessor,
        "text/x-c++": CodeProcessor,
        "text/x-go": CodeProcessor,
        "text/x-rust": CodeProcessor,
        "text/x-ruby": CodeProcessor,
        "application/x-php": CodeProcessor,
        "text/x-swift": CodeProcessor,
        "text/x-kotlin": CodeProcessor,
        "text/x-csharp": CodeProcessor,
    }
    
    # Mapping of special processor types
    SPECIAL_PROCESSORS = {
        "privacy": PrivacyCompliantProcessor,
    }
    
    @classmethod
    def get_processor_for_file(
        cls, 
        file_path: Union[str, Path], 
        use_cognee: bool = False,
        enable_ai: bool = False,
        dataset_name: Optional[str] = None,
        **kwargs
    ) -> BaseProcessor:
        """
        Get processor for a file based on its extension.
        
        Args:
            file_path: Path to the file
            use_cognee: Whether to use Cognee for database operations
            enable_ai: Whether to enable AI enhancements
            dataset_name: Name of the dataset (for Cognee integration)
            **kwargs: Additional options for the processor
            
        Returns:
            Appropriate processor instance
            
        Raises:
            ValueError: If no processor is available for the file type
        """
        file_path = Path(file_path) if isinstance(file_path, str) else file_path
        extension = file_path.suffix.lower()
        
        processor_class = cls.EXTENSION_MAPPING.get(extension)
        if not processor_class:
            raise ValueError(f"No processor available for file type: {extension}")
        
        # Add file path to kwargs for processors that need it
        kwargs['file_path'] = str(file_path)
        
        # Create processor with enhanced options
        return processor_class(
            use_cognee=use_cognee,
            enable_ai=enable_ai,
            dataset_name=dataset_name or f"{extension[1:]}_dataset",
            **kwargs
        )
    
    @classmethod
    def get_processor_for_content_type(
        cls, 
        content_type: str, 
        use_cognee: bool = False,
        enable_ai: bool = False,
        dataset_name: Optional[str] = None,
        **kwargs
    ) -> BaseProcessor:
        """
        Get processor for a content type.
        
        Args:
            content_type: MIME content type
            use_cognee: Whether to use Cognee for database operations
            enable_ai: Whether to enable AI enhancements
            dataset_name: Name of the dataset (for Cognee integration)
            **kwargs: Additional options for the processor
            
        Returns:
            Appropriate processor instance
            
        Raises:
            ValueError: If no processor is available for the content type
        """
        processor_class = cls.CONTENT_TYPE_MAPPING.get(content_type)
        if not processor_class:
            raise ValueError(f"No processor available for content type: {content_type}")
        
        # Create processor with enhanced options
        return processor_class(
            use_cognee=use_cognee,
            enable_ai=enable_ai,
            dataset_name=dataset_name or f"{content_type.split('/')[-1]}_dataset",
            **kwargs
        )
    
    @classmethod
    def get_special_processor(
        cls, 
        processor_type: str,
        use_cognee: bool = False,
        enable_ai: bool = False,
        **kwargs
    ) -> BaseProcessor:
        """
        Get a special processor by type.
        
        Args:
            processor_type: Type of special processor
            use_cognee: Whether to use Cognee for database operations
            enable_ai: Whether to enable AI enhancements
            **kwargs: Additional options for the processor
            
        Returns:
            Special processor instance
            
        Raises:
            ValueError: If the requested processor type is not available
        """
        processor_class = cls.SPECIAL_PROCESSORS.get(processor_type)
        if not processor_class:
            raise ValueError(f"Special processor not available: {processor_type}")
        
        # Create processor with enhanced options
        return processor_class(
            use_cognee=use_cognee,
            enable_ai=enable_ai,
            **kwargs
        )
    
    @classmethod
    def get_optimal_processor(
        cls, 
        content: Any, 
        file_size: Optional[int] = None, 
        content_type: Optional[str] = None,
        use_cognee: bool = False,
        enable_ai: bool = False,
        dataset_name: Optional[str] = None,
        **kwargs
    ) -> BaseProcessor:
        """
        Get the optimal processor based on content analysis.
        
        Args:
            content: Content to process
            file_size: Size of the file in bytes
            content_type: MIME content type if known
            use_cognee: Whether to use Cognee for database operations
            enable_ai: Whether to enable AI enhancements
            dataset_name: Name of the dataset (for Cognee integration)
            **kwargs: Additional options for the processor
            
        Returns:
            Optimal processor instance
        """
        # If content type is provided, use it
        if content_type and content_type in cls.CONTENT_TYPE_MAPPING:
            return cls.get_processor_for_content_type(
                content_type, 
                use_cognee=use_cognee,
                enable_ai=enable_ai,
                dataset_name=dataset_name,
                **kwargs
            )
        
        # Try to infer from content
        if isinstance(content, str):
            # Check if it looks like HTML
            if content.strip().startswith(('<html', '<!DOCTYPE html')):
                processor_class = HTMLProcessor
            # Check if it looks like JSON
            elif content.strip().startswith('{') and content.strip().endswith('}'):
                processor_class = JsonProcessor
            # Check if it looks like CSV
            elif ',' in content and '\n' in content:
                processor_class = CsvProcessor
            # Check if it looks like Markdown
            elif '# ' in content or '## ' in content:
                processor_class = MarkdownProcessor
            # Check if it looks like code
            elif any(keyword in content for keyword in ['def ', 'class ', 'function ', 'import ', '#include']):
                processor_class = CodeProcessor
            # Default to text
            else:
                processor_class = TextProcessor
        elif isinstance(content, bytes):
            # Check for PDF signature
            if content.startswith(b'%PDF'):
                processor_class = PDFProcessor
            # Check for image signatures
            elif content.startswith((b'\x89PNG', b'\xFF\xD8\xFF', b'GIF', b'BM', b'RIFF')):
                processor_class = ImageProcessor
            # Try to decode as text
            else:
                try:
                    text_content = content.decode('utf-8')
                    return cls.get_optimal_processor(
                        text_content, 
                        file_size, 
                        content_type, 
                        use_cognee=use_cognee,
                        enable_ai=enable_ai,
                        dataset_name=dataset_name,
                        **kwargs
                    )
                except UnicodeDecodeError:
                    # Binary content we don't recognize, default to text
                    processor_class = TextProcessor
        else:
            # Default to text processor
            processor_class = TextProcessor
        
        # Create processor with enhanced options
        inferred_type = processor_class.__name__.replace("Processor", "").lower()
        return processor_class(
            use_cognee=use_cognee,
            enable_ai=enable_ai,
            dataset_name=dataset_name or f"{inferred_type}_dataset",
            **kwargs
        )
    
    @classmethod
    def get_enhanced_processor(
        cls, 
        file_path: Optional[Union[str, Path]] = None, 
        content_type: Optional[str] = None, 
        content: Optional[Any] = None,
        dataset_name: Optional[str] = None,
        **kwargs
    ) -> BaseProcessor:
        """
        Get a processor with enhanced AI capabilities.
        
        This is a convenience method that enables AI enhancements
        and Cognee integration by default.
        
        Args:
            file_path: Path to the file (if processing a file)
            content_type: MIME content type (if known)
            content: Content to process (if not processing a file)
            dataset_name: Name of the dataset (for Cognee integration)
            **kwargs: Additional options for the processor
            
        Returns:
            Enhanced processor instance
        """
        # Set enhanced options
        kwargs.update({
            "use_cognee": kwargs.get("use_cognee", True),
            "enable_ai": kwargs.get("enable_ai", True),
            "dataset_name": dataset_name
        })
        
        # Determine the appropriate method to call
        if file_path:
            return cls.get_processor_for_file(file_path, **kwargs)
        elif content_type:
            return cls.get_processor_for_content_type(content_type, **kwargs)
        elif content:
            return cls.get_optimal_processor(content, **kwargs)
        else:
            raise ValueError("At least one of file_path, content_type, or content must be provided")
    
    @classmethod
    def available_processor_types(cls) -> List[str]:
        """
        Get a list of available processor types.
        
        Returns:
            List of available processor types
        """
        # Collect extensions and content types
        extensions = sorted(cls.EXTENSION_MAPPING.keys())
        content_types = sorted(cls.CONTENT_TYPE_MAPPING.keys())
        special = sorted(cls.SPECIAL_PROCESSORS.keys())
        
        return {
            "extensions": extensions,
            "content_types": content_types,
            "special": special
        } 