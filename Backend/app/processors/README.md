# Document Processors

This directory contains document processors for the ConTXT system. Each processor is specialized for handling a specific type of document or content.

## Available Processors

- **BaseProcessor**: Enhanced base class for all processors with common functionality
- **TextProcessor**: Handles plain text documents
- **MarkdownProcessor**: Processes Markdown documents with structure-aware chunking
- **JsonProcessor**: Processes JSON documents with schema extraction
- **CsvProcessor**: Processes CSV documents with header detection
- **ImageProcessor**: Processes images with OCR and object detection
- **PDFProcessor**: Processes PDF documents with text and structure extraction
- **HTMLProcessor**: Processes HTML documents with structure and link extraction
- **CodeProcessor**: Processes source code files with language-specific handling
- **PrivacyCompliantProcessor**: Wrapper processor for privacy compliance (PII redaction)

## Enhanced Capabilities

The document processors now support optional AI enhancements and Cognee integration:

- **AI Enhancements**: Use models like Grok-4 and GPT-4o to analyze and enrich document content
- **Cognee Integration**: Integrate with Cognee for advanced graph and vector database operations
- **Feature Flags**: Enable/disable AI enhancements and Cognee integration as needed
- **Database Adapters**: Support both direct database access and Cognee abstraction

## Factory

The `ProcessorFactory` class provides methods for creating the appropriate processor based on content type or file extension.

### Enhanced Factory Methods

- **get_processor_for_file**: Get a processor for a file based on extension
- **get_processor_for_content_type**: Get a processor for a content type
- **get_optimal_processor**: Get the optimal processor based on content analysis
- **get_special_processor**: Get a special processor (e.g., privacy)
- **get_enhanced_processor**: Get a processor with AI enhancements enabled

## Configuration

The `ProcessingConfig` class provides configuration for the document processors, supporting:

- Database connections (Neo4j, Qdrant)
- AI model configuration (xAI, OpenAI)
- Feature flags (enable_ai, use_cognee)
- Document processing options (chunk_size, chunk_overlap)

## Environment Variables

Set these environment variables to configure the system:

```
# Database Configuration
NEO4J_URI=bolt://localhost:7687
NEO4J_USERNAME=neo4j
NEO4J_PASSWORD=your-neo4j-password
VECTOR_DB_URL=https://your-qdrant.cloud.io
VECTOR_DB_KEY=your-qdrant-key

# AI Configuration
XAI_API_KEY=your-xai-api-key
OPENAI_API_KEY=your-openai-api-key
DEFAULT_AI_MODEL=openai

# Feature Flags
USE_COGNEE=false
ENABLE_AI=false
```

## Usage

### Standard Processing

```python
from app.processors import ProcessorFactory

# Create a processor based on file extension
processor = ProcessorFactory.get_processor_for_file("document.md")

# Process a document
with open("document.md", "r") as f:
    content = f.read()
result = await processor.process(content, {"file_name": "document.md"})

# Access the processed data
chunks = result["chunks"]
metadata = result["metadata"]
```

### Enhanced Processing

```python
from app.processors import ProcessorFactory

# Create an enhanced processor with AI capabilities
processor = ProcessorFactory.get_enhanced_processor(
    file_path="document.md",
    dataset_name="my_documents"
)

# Process with AI enhancements
with open("document.md", "r") as f:
    content = f.read()
result = await processor.process_with_enhancements(content, {
    "file_name": "document.md",
    "enhancement_type": "analysis"
})

# Access the processed and enhanced data
chunks = result["chunks"]
metadata = result["metadata"]
enhanced_content = result["enhanced_content"]
```

### Direct Factory Integration

```python
from app.processors.factory import ProcessorFactory

# Process a document with enhancements
result = await ProcessorFactory.get_enhanced_processor(
    file_path="document.json"
).process_with_enhancements(content)
```

## Testing

See the `test_processors.py` script in the root directory for examples of how to use each processor.

## Documentation

For more detailed documentation:

- See `DOCUMENT_PROCESSING.md` for detailed documentation on document processing
- See `PROCESSORS_SUMMARY.md` for a summary of available processors and their capabilities 