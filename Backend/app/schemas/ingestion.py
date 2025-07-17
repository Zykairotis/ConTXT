"""
Pydantic models for data ingestion operations.
Includes support for AI enhancements and database integration options.
"""
from typing import Dict, List, Optional, Any, Union, Literal
from pydantic import BaseModel, Field, HttpUrl

class EnhancementOptions(BaseModel):
    """Enhancement options for document processing."""
    use_cognee: bool = Field(False, description="Whether to use Cognee for database operations")
    enable_ai: bool = Field(False, description="Whether to enable AI enhancements")
    enhancement_type: Optional[str] = Field(None, description="Type of enhancement to apply (analysis, summary, etc.)")
    dataset_name: Optional[str] = Field(None, description="Name of the dataset for Cognee integration")

class UrlIngestionRequest(BaseModel):
    """Request model for ingesting content from a URL."""
    url: HttpUrl = Field(..., description="URL to ingest content from")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    options: Optional[Dict[str, Any]] = Field(None, description="Ingestion options including AI enhancements")

class FileIngestionRequest(BaseModel):
    """Request model for ingesting content from a file."""
    file_name: str = Field(..., description="Name of the file")
    file_type: str = Field(..., description="Type of the file (pdf, txt, etc.)")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    options: Optional[Dict[str, Any]] = Field(None, description="Ingestion options including AI enhancements")

class TextIngestionRequest(BaseModel):
    """Request model for ingesting raw text content."""
    text: str = Field(..., description="Text content to ingest")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    options: Optional[Dict[str, Any]] = Field(None, description="Ingestion options including AI enhancements")

class PrivacyIngestionRequest(BaseModel):
    """Request model for ingesting content with privacy compliance."""
    content: Any = Field(..., description="Content to ingest (text, URL, or file content)")
    content_type: str = Field(..., description="Type of content (text/plain, application/json, etc.)")
    redact_pii: bool = Field(True, description="Whether to redact personally identifiable information")
    pii_types: Optional[List[str]] = Field(None, description="Types of PII to redact (email, phone, etc.)")
    metadata: Optional[Dict[str, Any]] = Field(None, description="Additional metadata")
    options: Optional[Dict[str, Any]] = Field(None, description="Ingestion options including AI enhancements")

class EnhancementResult(BaseModel):
    """Result of document enhancement."""
    has_enhancements: bool = Field(..., description="Whether enhancements were applied")
    enhancement_type: Optional[str] = Field(None, description="Type of enhancement applied")
    insights: Optional[List[str]] = Field(None, description="Generated insights")

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

class EnhancementOptionsResponse(BaseModel):
    """Response model for available enhancement options."""
    cognee_available: bool = Field(..., description="Whether Cognee is available")
    ai_models: Dict[str, bool] = Field(..., description="Available AI models")
    enhancement_types: List[str] = Field(..., description="Available enhancement types") 