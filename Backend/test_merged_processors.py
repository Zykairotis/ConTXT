"""
Test file for demonstrating the merged document processors.

This file shows how to use both standard and enhanced processing capabilities.
Run with: python test_merged_processors.py
"""
import os
import asyncio
import json
from pathlib import Path

# Set environment variables for testing (optional)
os.environ["ENABLE_AI"] = "false"  # Set to "true" to enable AI enhancements
os.environ["USE_COGNEE"] = "false"  # Set to "true" to use Cognee abstraction

# Import processors
from app.processors import (
    get_processor,
    get_enhanced_processor,
    ProcessorFactory,
    ProcessingConfig
)

# Sample data
SAMPLE_TEXT = """
# Sample Document

This is a sample document for testing document processing capabilities.

## Features

- Standard processing
- Enhanced processing with AI
- Cognee integration for knowledge graphs
"""

SAMPLE_JSON = """
{
    "name": "Document Processors",
    "features": [
        "Standard processing",
        "Enhanced processing",
        "Cognee integration"
    ],
    "capabilities": {
        "ai": true,
        "graph": true,
        "vector": true
    }
}
"""

async def test_standard_processing():
    """Test standard document processing."""
    print("\n=== Testing Standard Processing ===")
    
    # Create a text processor
    text_processor = get_processor(content_type="text/markdown")
    
    # Process text
    print("Processing markdown text...")
    result = await text_processor.process(SAMPLE_TEXT, metadata={"source": "test"})
    
    # Print results
    print(f"Processed {len(result.get('chunks', []))} chunks")
    
    # Create a JSON processor
    json_processor = get_processor(content_type="application/json")
    
    # Process JSON
    print("Processing JSON data...")
    result = await json_processor.process(SAMPLE_JSON, metadata={"source": "test"})
    
    # Print results
    print(f"Processed {len(result.get('chunks', []))} chunks")
    print(f"Extracted {len(result.get('metadata', {}).get('entities', []))} entities")

async def test_enhanced_processing():
    """Test enhanced document processing with AI."""
    print("\n=== Testing Enhanced Processing ===")
    
    # Check if AI is enabled
    config = ProcessingConfig()
    if not config.enable_ai or not config.available_models:
        print("AI enhancements not available (set ENABLE_AI=true and configure an AI model)")
        return
    
    # Create an enhanced text processor
    enhanced_processor = get_enhanced_processor(
        content_type="text/markdown",
        enhancement_type="analysis"
    )
    
    # Process with enhancements
    print("Processing markdown text with AI enhancements...")
    result = await enhanced_processor.process_with_enhancements(
        SAMPLE_TEXT, 
        metadata={"source": "test"}
    )
    
    # Print results
    print(f"Processed {len(result.get('chunks', []))} chunks")
    if result.get("has_enhancements"):
        print("Enhanced content:")
        print("-" * 40)
        print(result.get("enhanced_content", "No enhanced content"))
        print("-" * 40)
    else:
        print("No enhancements applied")

async def test_file_processing():
    """Test file processing if sample files exist."""
    print("\n=== Testing File Processing ===")
    
    # Check for sample files
    samples_dir = Path("samples")
    if not samples_dir.exists():
        print("No sample directory found, creating it with sample files...")
        samples_dir.mkdir(exist_ok=True)
        
        # Create sample files
        with open(samples_dir / "sample.md", "w") as f:
            f.write(SAMPLE_TEXT)
        
        with open(samples_dir / "sample.json", "w") as f:
            f.write(SAMPLE_JSON)
    
    # Process markdown file
    if (samples_dir / "sample.md").exists():
        print("Processing sample markdown file...")
        md_processor = get_processor(file_path=str(samples_dir / "sample.md"))
        with open(samples_dir / "sample.md", "r") as f:
            result = await md_processor.process(f.read())
        print(f"Processed markdown file: {len(result.get('chunks', []))} chunks")
    
    # Process JSON file with enhancements
    if (samples_dir / "sample.json").exists():
        print("Processing sample JSON file with enhancements...")
        config = ProcessingConfig()
        if config.enable_ai and config.available_models:
            json_processor = get_enhanced_processor(file_path=str(samples_dir / "sample.json"))
            with open(samples_dir / "sample.json", "r") as f:
                result = await json_processor.process_with_enhancements(f.read())
            print(f"Processed JSON file: {len(result.get('chunks', []))} chunks")
            if result.get("has_enhancements"):
                print("AI enhancements applied")
        else:
            print("AI enhancements not available for JSON file processing")

async def test_configuration():
    """Test configuration options."""
    print("\n=== Testing Configuration ===")
    
    # Create configuration
    config = ProcessingConfig()
    
    # Print configuration
    print("Current configuration:")
    print(f"- AI enabled: {config.enable_ai}")
    print(f"- Cognee enabled: {config.use_cognee}")
    print(f"- Available AI models: {config.available_models}")
    print(f"- Default model: {config.default_model}")
    
    # Try to get AI model
    model = config.get_ai_model()
    if model:
        print(f"- AI model loaded: {model.__class__.__name__}")
    else:
        print("- No AI model available")
    
    # Print database configuration
    print("\nDatabase configuration:")
    for db_name, db_config in config.databases.items():
        print(f"- {db_name}: {db_config.get('provider')}")
    
    # Print to_dict output
    config_dict = config.to_dict()
    print("\nConfiguration as dict (excluding sensitive data):")
    print(json.dumps(config_dict, indent=2))

async def main():
    """Run tests."""
    # Print processor information
    print("=== Document Processors Test ===")
    print("This test demonstrates both standard and enhanced processing capabilities.")
    
    # Print available processors
    print("\nAvailable processors:")
    for ext in sorted(list(ProcessorFactory.EXTENSION_MAPPING.keys())):
        proc = ProcessorFactory.EXTENSION_MAPPING[ext].__name__
        print(f"- {ext}: {proc}")
    
    # Run tests
    await test_standard_processing()
    await test_enhanced_processing()
    await test_file_processing()
    await test_configuration()
    
    print("\n=== Testing Complete ===")

if __name__ == "__main__":
    asyncio.run(main()) 