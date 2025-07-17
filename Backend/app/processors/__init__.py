"""
Document processors package.

This package provides processors for various file types with optional
AI enhancements and Cognee integration for advanced capabilities.
"""
import os

# Set environment variables for Cognee before importing
# Ensure LOG_LEVEL is uppercase for Cognee
if 'LOG_LEVEL' in os.environ:
    log_level = os.environ['LOG_LEVEL']
    if log_level.lower() in ['info', 'debug', 'warning', 'error', 'critical']:
        os.environ['LOG_LEVEL'] = log_level.upper()

# Now import the processor components
try:
    from app.processors.base import BaseProcessor, DatabaseAdapter, AIEnhancementLayer
    from app.processors.factory import ProcessorFactory
    from app.processors.text_processor import TextProcessor
    from app.processors.pdf_processor import PDFProcessor
    from app.processors.image_processor import ImageProcessor
    from app.processors.html_processor import HTMLProcessor
    from app.processors.markdown_processor import MarkdownProcessor
    from app.processors.code_processor import CodeProcessor
    from app.processors.csv_processor import CSVProcessor
    from app.processors.json_processor import JSONProcessor
    from app.processors.privacy_processor import PrivacyProcessor
except ImportError as e:
    print(f"Warning: Some processor modules could not be imported: {e}")

__all__ = [
    'BaseProcessor',
    'DatabaseAdapter',
    'AIEnhancementLayer',
    'ProcessorFactory',
    'TextProcessor',
    'PDFProcessor',
    'ImageProcessor',
    'HTMLProcessor',
    'MarkdownProcessor',
    'CodeProcessor',
    'CSVProcessor',
    'JSONProcessor',
    'PrivacyProcessor',
]

# Create convenience functions for processor factory
def get_processor(file_path=None, content_type=None, content=None, **kwargs):
    """
    Get the appropriate processor for the given file path, content type, or content.
    
    Args:
        file_path: Path to the file (if processing a file)
        content_type: MIME content type (if known)
        content: Content to process (if not processing a file)
        **kwargs: Additional options for the processor
        
    Returns:
        Appropriate processor instance
        
    Raises:
        ValueError: If no processor is available for the file type or content type
    """
    if file_path:
        return ProcessorFactory.get_processor_for_file(file_path, **kwargs)
    elif content_type:
        return ProcessorFactory.get_processor_for_content_type(content_type, **kwargs)
    elif content:
        return ProcessorFactory.get_optimal_processor(content, **kwargs)
    else:
        raise ValueError("At least one of file_path, content_type, or content must be provided")

def get_enhanced_processor(file_path=None, content_type=None, content=None, **kwargs):
    """
    Get an enhanced processor with AI capabilities.
    
    This is a convenience method that enables AI enhancements
    and Cognee integration by default.
    
    Args:
        file_path: Path to the file (if processing a file)
        content_type: MIME content type (if known)
        content: Content to process (if not processing a file)
        **kwargs: Additional options for the processor
        
    Returns:
        Enhanced processor instance
    """
    return ProcessorFactory.get_enhanced_processor(
        file_path=file_path,
        content_type=content_type,
        content=content,
        **kwargs
    ) 