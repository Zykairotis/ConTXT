"""
API endpoints for data ingestion operations.

These endpoints support processing various types of content with
optional AI enhancements and Cognee integration for advanced analysis.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Dict, List, Optional, Any

from app.core.ingestion import IngestionManager
from app.schemas.ingestion import (
    UrlIngestionRequest,
    FileIngestionRequest,
    TextIngestionRequest,
    PrivacyIngestionRequest,
    IngestionResponse,
    IngestionStatus
)

router = APIRouter()

@router.post("/url", response_model=IngestionResponse)
async def ingest_url(request: UrlIngestionRequest):
    """
    Ingest content from a URL.
    
    This endpoint processes content from a URL, extracts relevant information,
    and stores it in the knowledge graph and vector database.
    
    Optional AI enhancements can be enabled via the options field.
    """
    try:
        # Extract enhancement options
        options = request.options or {}
        use_cognee = options.get("use_cognee", False)
        enable_ai = options.get("enable_ai", False)
        
        # Initialize ingestion manager with options
        ingestion_manager = IngestionManager(use_cognee=use_cognee, enable_ai=enable_ai)
        
        job_id = await ingestion_manager.ingest_url(
            url=request.url,
            metadata=request.metadata,
            options=options
        )
        return IngestionResponse(job_id=job_id, status="processing")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"URL ingestion failed: {str(e)}")

@router.post("/file", response_model=IngestionResponse)
async def ingest_file(
    file: UploadFile = File(...),
    metadata: Optional[str] = Form(None),
    use_cognee: bool = Form(False),
    enable_ai: bool = Form(False),
    dataset_name: Optional[str] = Form(None)
):
    """
    Ingest content from an uploaded file.
    
    This endpoint processes uploaded files (PDF, text, etc.), extracts relevant
    information, and stores it in the knowledge graph and vector database.
    
    Optional parameters:
    - use_cognee: Whether to use Cognee for database operations
    - enable_ai: Whether to enable AI enhancements
    - dataset_name: Name of the dataset for Cognee integration
    """
    try:
        # Create options dictionary from form parameters
        options = {
            "use_cognee": use_cognee,
            "enable_ai": enable_ai
        }
        
        if dataset_name:
            options["dataset_name"] = dataset_name
        
        # Initialize ingestion manager with options
        ingestion_manager = IngestionManager(use_cognee=use_cognee, enable_ai=enable_ai)
        
        job_id = await ingestion_manager.ingest_file(
            file=file,
            metadata=metadata,
            options=options
        )
        return IngestionResponse(job_id=job_id, status="processing")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File ingestion failed: {str(e)}")

@router.post("/text", response_model=IngestionResponse)
async def ingest_text(
    text: str = Form(...),
    metadata: Optional[str] = Form(None),
    use_cognee: bool = Form(False),
    enable_ai: bool = Form(False),
    dataset_name: Optional[str] = Form(None)
):
    """
    Ingest raw text content.
    
    This endpoint processes raw text, extracts relevant information,
    and stores it in the knowledge graph and vector database.
    
    Optional parameters:
    - use_cognee: Whether to use Cognee for database operations
    - enable_ai: Whether to enable AI enhancements
    - dataset_name: Name of the dataset for Cognee integration
    """
    try:
        # Create options dictionary from form parameters
        options = {
            "use_cognee": use_cognee,
            "enable_ai": enable_ai
        }
        
        if dataset_name:
            options["dataset_name"] = dataset_name
        
        # Initialize ingestion manager with options
        ingestion_manager = IngestionManager(use_cognee=use_cognee, enable_ai=enable_ai)
        
        job_id = await ingestion_manager.ingest_text(
            text=text,
            metadata=metadata,
            options=options
        )
        return IngestionResponse(job_id=job_id, status="processing")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text ingestion failed: {str(e)}")

@router.post("/privacy", response_model=IngestionResponse)
async def ingest_with_privacy(request: PrivacyIngestionRequest):
    """
    Ingest content with privacy compliance.
    
    This endpoint processes content with privacy compliance, redacting
    personally identifiable information (PII) as specified.
    
    Optional AI enhancements can be enabled via the options field.
    """
    try:
        # Extract enhancement options
        options = request.options or {}
        use_cognee = options.get("use_cognee", False)
        enable_ai = options.get("enable_ai", False)
        
        # Initialize ingestion manager with options
        ingestion_manager = IngestionManager(use_cognee=use_cognee, enable_ai=enable_ai)
        
        job_id = await ingestion_manager.ingest_with_privacy(
            content=request.content,
            content_type=request.content_type,
            redact_pii=request.redact_pii,
            pii_types=request.pii_types,
            metadata=request.metadata,
            options=options
        )
        return IngestionResponse(job_id=job_id, status="processing")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Privacy-compliant ingestion failed: {str(e)}")

@router.get("/status/{job_id}", response_model=IngestionStatus)
async def get_ingestion_status(job_id: str):
    """Get the status of an ingestion job."""
    try:
        ingestion_manager = IngestionManager()
        status = await ingestion_manager.get_status(job_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Ingestion job not found: {str(e)}")

@router.get("/enhancement-options", response_model=Dict[str, Any])
async def get_enhancement_options():
    """
    Get available enhancement options for document processing.
    
    Returns information about available AI models, database integrations,
    and other enhancement options.
    """
    try:
        # Try to import optional dependencies to check availability
        cognee_available = False
        xai_available = False
        openai_available = False
        
        try:
            import cognee
            cognee_available = True
        except ImportError:
            pass
            
        try:
            from langchain_xai import ChatXAI
            xai_available = True
        except ImportError:
            pass
            
        try:
            from langchain_openai import ChatOpenAI
            openai_available = True
        except ImportError:
            pass
        
        # Return available options
        return {
            "cognee_available": cognee_available,
            "ai_models": {
                "xai_available": xai_available,
                "openai_available": openai_available
            },
            "enhancement_types": [
                "analysis",
                "summary",
                "entity_extraction",
                "insight_generation"
            ]
        }
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Error retrieving enhancement options: {str(e)}") 