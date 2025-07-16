"""
Pydantic models for context engineering operations.
"""
from typing import Dict, List, Optional, Any, Union
from pydantic import BaseModel, Field, HttpUrl

class Source(BaseModel):
    """A source of information for context building."""
    source_id: Optional[str] = None
    source_type: str = Field(..., description="Type of source (url, file, text, etc.)")
    content: Optional[str] = None
    url: Optional[HttpUrl] = None
    metadata: Optional[Dict[str, Any]] = None

class ContextRequest(BaseModel):
    """Request model for building engineered context."""
    sources: List[Source] = Field(..., description="List of sources to process")
    max_tokens: Optional[int] = Field(None, description="Maximum tokens for context window")
    compression_ratio: Optional[float] = Field(None, description="Target compression ratio")
    include_metadata: bool = Field(False, description="Include metadata in response")
    tool_type: Optional[str] = Field(None, description="Target tool type (cursor, windsurf, etc.)")

class ContextBlock(BaseModel):
    """A block of engineered context."""
    block_id: str
    block_type: str = Field(..., description="Type of context block (code, text, etc.)")
    content: str
    source_id: Optional[str] = None
    metadata: Optional[Dict[str, Any]] = None
    relevance_score: Optional[float] = None

class ContextResponse(BaseModel):
    """Response model for context building operations."""
    context_id: str
    blocks: List[ContextBlock]
    token_count: int
    compression_ratio: float
    metadata: Optional[Dict[str, Any]] = None

class SystemPromptRequest(BaseModel):
    """Request model for generating a system prompt."""
    context_id: str = Field(..., description="ID of the built context")
    tool_type: str = Field(..., description="Target tool type (cursor, windsurf, etc.)")
    parameters: Optional[Dict[str, Any]] = Field(None, description="Additional parameters") 