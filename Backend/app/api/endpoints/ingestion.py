"""
API endpoints for data ingestion operations.
"""
from fastapi import APIRouter, Depends, HTTPException, UploadFile, File, Form
from typing import Dict, List, Optional, Any

from app.core.ingestion import IngestionManager
from app.schemas.ingestion import (
    UrlIngestionRequest,
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
    """
    try:
        ingestion_manager = IngestionManager()
        job_id = await ingestion_manager.ingest_url(
            url=request.url,
            metadata=request.metadata,
            options=request.options
        )
        return IngestionResponse(job_id=job_id, status="processing")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"URL ingestion failed: {str(e)}")

@router.post("/file", response_model=IngestionResponse)
async def ingest_file(
    file: UploadFile = File(...),
    metadata: Optional[str] = Form(None)
):
    """
    Ingest content from an uploaded file.
    
    This endpoint processes uploaded files (PDF, text, etc.), extracts relevant
    information, and stores it in the knowledge graph and vector database.
    """
    try:
        ingestion_manager = IngestionManager()
        job_id = await ingestion_manager.ingest_file(
            file=file,
            metadata=metadata
        )
        return IngestionResponse(job_id=job_id, status="processing")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"File ingestion failed: {str(e)}")

@router.post("/text", response_model=IngestionResponse)
async def ingest_text(
    text: str = Form(...),
    metadata: Optional[str] = Form(None)
):
    """
    Ingest raw text content.
    
    This endpoint processes raw text, extracts relevant information,
    and stores it in the knowledge graph and vector database.
    """
    try:
        ingestion_manager = IngestionManager()
        job_id = await ingestion_manager.ingest_text(
            text=text,
            metadata=metadata
        )
        return IngestionResponse(job_id=job_id, status="processing")
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Text ingestion failed: {str(e)}")

@router.get("/status/{job_id}", response_model=IngestionStatus)
async def get_ingestion_status(job_id: str):
    """Get the status of an ingestion job."""
    try:
        ingestion_manager = IngestionManager()
        status = await ingestion_manager.get_status(job_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Ingestion job not found: {str(e)}") 