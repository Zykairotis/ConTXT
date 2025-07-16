"""
Pydantic models for data ingestion operations.
"""
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, HttpUrl

class UrlIngestionRequest(BaseModel):
    """Request model for ingesting content from a URL."""
    url: HttpUrl = Field(..., description="URL to ingest content from")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    options: Optional[Dict[str, Any]] = Field(None, description="Ingestion options")

class FileIngestionRequest(BaseModel):
    """Request model for ingesting content from a file."""
    file_name: str = Field(..., description="Name of the file")
    file_type: str = Field(..., description="Type of the file (pdf, txt, etc.)")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    options: Optional[Dict[str, Any]] = Field(None, description="Ingestion options")

class TextIngestionRequest(BaseModel):
    """Request model for ingesting raw text content."""
    text: str = Field(..., description="Text content to ingest")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    options: Optional[Dict[str, Any]] = Field(None, description="Ingestion options")

class IngestionResponse(BaseModel):
    """Response model for ingestion operations."""
    job_id: str = Field(..., description="ID of the ingestion job")
    status: str = Field(..., description="Status of the ingestion job")
    message: Optional[str] = None

class IngestionStatus(BaseModel):
    """Status model for ingestion jobs."""
    job_id: str
    status: str = Field(..., description="Status of the job (processing, completed, failed)")
    progress: Optional[float] = Field(None, description="Progress percentage (0-100)")
    message: Optional[str] = None
    result: Optional[Dict[str, Any]] = None
    created_at: str
    updated_at: str 