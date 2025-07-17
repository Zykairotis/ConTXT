"""
Document processors package.

This package provides processors for various file types with optional
AI enhancements and Cognee integration for advanced capabilities.
"""
import os

# Set environment variables for Cognee before importing
if os.environ.get('LOG_LEVEL', '').lower() == 'info':
    os.environ['LOG_LEVEL'] = 'INFO'
elif os.environ.get('LOG_LEVEL', '').lower() == 'debug':
    os.environ['LOG_LEVEL'] = 'DEBUG'
elif os.environ.get('LOG_LEVEL', '').lower() == 'warning':
    os.environ['LOG_LEVEL'] = 'WARNING'
elif os.environ.get('LOG_LEVEL', '').lower() == 'error':
    os.environ['LOG_LEVEL'] = 'ERROR'
elif os.environ.get('LOG_LEVEL', '').lower() == 'critical':
    os.environ['LOG_LEVEL'] = 'CRITICAL'

from app.processors.base import BaseProcessor, DatabaseAdapter, AIEnhancementLayer
from app.processors.factory import ProcessorFactory
from app.processors.config import ProcessingConfig, default_config

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

__all__ = [
    # Main components
    'BaseProcessor',
    'DatabaseAdapter',
    'AIEnhancementLayer',
    'ProcessorFactory',
    'ProcessingConfig',
    'default_config',
    
    # Standard processors
    'TextProcessor',
    'MarkdownProcessor',
    'JsonProcessor',
    'CsvProcessor',
    'ImageProcessor',
    'PDFProcessor',
    'HTMLProcessor',
    'CodeProcessor',
    'PrivacyCompliantProcessor',
] 