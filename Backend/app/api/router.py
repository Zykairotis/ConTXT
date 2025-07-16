"""
Main API router that includes all endpoint routers.
"""
from fastapi import APIRouter

from app.api.endpoints import context, knowledge, ingestion

api_router = APIRouter()

# Include all endpoint routers
api_router.include_router(ingestion.router, prefix="/ingestion", tags=["ingestion"])
api_router.include_router(context.router, prefix="/context", tags=["context"])
api_router.include_router(knowledge.router, prefix="/knowledge", tags=["knowledge"]) 