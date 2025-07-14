"""
Main application entry point for the AI Context Builder backend.
"""
import uvicorn
from fastapi import FastAPI
from fastapi.middleware.cors import CORSMiddleware

from Backend.api.routes import router as api_router
from Backend.config.settings import settings

app = FastAPI(
    title="AI Context Builder API",
    description="API for building AI context and generating system prompts",
    version="0.1.0",
)

# Configure CORS
app.add_middleware(
    CORSMiddleware,
    allow_origins=settings.CORS_ORIGINS,
    allow_credentials=True,
    allow_methods=["*"],
    allow_headers=["*"],
)

# Include API routes
app.include_router(api_router, prefix="/api/v1")

@app.get("/")
async def root():
    """Root endpoint for health check."""
    return {"status": "ok", "message": "AI Context Builder API is running"}

if __name__ == "__main__":
    uvicorn.run(
        "Backend.main:app",
        host=settings.API_HOST,
        port=settings.API_PORT,
        reload=settings.DEBUG,
    ) 