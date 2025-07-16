"""
API endpoints for context engineering operations.
"""
from fastapi import APIRouter, Depends, HTTPException
from pydantic import BaseModel
from typing import Dict, List, Optional, Any

from app.core.context_engine import ContextEngine
from app.schemas.context import ContextRequest, ContextResponse, SystemPromptRequest

router = APIRouter()

@router.post("/build", response_model=ContextResponse)
async def build_context(request: ContextRequest):
    """
    Build engineered context from provided sources.
    
    This endpoint processes the input sources, analyzes their content,
    and curates an optimized context for AI agents.
    
    Context engineering steps:
    1. Select relevant knowledge from sources
    2. Compress content to fit within context window
    3. Order content by relevance and importance
    4. Structure output for optimal consumption
    """
    try:
        context_engine = ContextEngine()
        result = await context_engine.build_context(
            sources=request.sources,
            max_tokens=request.max_tokens or 128000,
            compression_ratio=request.compression_ratio or 0.5
        )
        return result
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"Context building failed: {str(e)}")

@router.post("/generate-system-prompt", response_model=Dict[str, str])
async def generate_system_prompt(request: SystemPromptRequest):
    """
    Generate a system prompt based on engineered context.
    
    This endpoint takes context information and generates a tailored 
    system prompt for specific AI tools like Cursor, Windsurf, etc.
    """
    try:
        context_engine = ContextEngine()
        system_prompt = await context_engine.generate_system_prompt(
            context_id=request.context_id,
            tool_type=request.tool_type,
            parameters=request.parameters
        )
        return {"system_prompt": system_prompt}
    except Exception as e:
        raise HTTPException(status_code=500, detail=f"System prompt generation failed: {str(e)}")

@router.get("/status/{context_id}", response_model=Dict[str, Any])
async def get_context_status(context_id: str):
    """Get the status and metadata of a context building operation."""
    try:
        context_engine = ContextEngine()
        status = await context_engine.get_context_status(context_id)
        return status
    except Exception as e:
        raise HTTPException(status_code=404, detail=f"Context not found: {str(e)}") 