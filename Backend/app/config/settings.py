"""
Configuration settings for the AI Context Engineering Agent.
"""
import os
import json
from typing import List, Optional, Union, Any

from pydantic import AnyHttpUrl, Field, validator
from pydantic_settings import BaseSettings


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    API_V1_STR: str = "/api/v1"
    PROJECT_NAME: str = "AI Context Engineering Agent"
    
    # CORS Configuration
    CORS_ORIGINS: List[Union[str, AnyHttpUrl]] = ["http://localhost:3000", "http://localhost:8000"]
    
    # Environment
    ENV: str = Field(default="dev", env="ENV")
    ENVIRONMENT: str = Field(default="development", env="ENVIRONMENT")
    DEBUG: bool = Field(default=True, env="DEBUG")
    LOG_LEVEL: str = Field(default="info", env="LOG_LEVEL")
    LOG_FORMAT: str = Field(default="json", env="LOG_FORMAT")
    LOG_FILE: str = Field(default="/app/logs/app.log", env="LOG_FILE")
    
    # Neo4j Configuration
    NEO4J_HOST: str = Field(default="neo4j", env="NEO4J_HOST")
    NEO4J_PORT: int = Field(default=7687, env="NEO4J_PORT")
    NEO4J_USER: str = Field(default="neo4j", env="NEO4J_USER")
    NEO4J_USERNAME: str = Field(default="neo4j", env="NEO4J_USERNAME")
    NEO4J_PASSWORD: str = Field(default="password", env="NEO4J_PASSWORD")
    NEO4J_URI: str = Field(default="bolt://neo4j:7687", env="NEO4J_URI")
    GRAPH_DATABASE_PROVIDER: str = Field(default="neo4j", env="GRAPH_DATABASE_PROVIDER")
    
    # Qdrant Configuration
    QDRANT_HOST: str = Field(default="qdrant", env="QDRANT_HOST")
    QDRANT_PORT: int = Field(default=6333, env="QDRANT_PORT")
    QDRANT_COLLECTION: str = Field(default="context_vectors", env="QDRANT_COLLECTION")
    VECTOR_DB_PROVIDER: str = Field(default="qdrant", env="VECTOR_DB_PROVIDER")
    VECTOR_DB_URL: str = Field(default="http://qdrant:6333", env="VECTOR_DB_URL")
    
    # Database Configuration
    DB_PROVIDER: str = Field(default="postgres", env="DB_PROVIDER")
    DB_HOST: str = Field(default="postgres", env="DB_HOST")
    DB_PORT: str = Field(default="5432", env="DB_PORT")
    DB_USERNAME: str = Field(default="postgres", env="DB_USERNAME")
    DB_PASSWORD: str = Field(default="postgres", env="DB_PASSWORD")
    DB_NAME: str = Field(default="document_processor", env="DB_NAME")
    DB_SSL_MODE: str = Field(default="disable", env="DB_SSL_MODE")
    
    # Redis Configuration
    REDIS_URL: str = Field(default="redis://redis:6379/0", env="REDIS_URL")
    
    # Celery Configuration
    CELERY_BROKER_URL: str = Field(default="redis://redis:6379/0", env="CELERY_BROKER_URL")
    CELERY_RESULT_BACKEND: str = Field(default="redis://redis:6379/0", env="CELERY_RESULT_BACKEND")
    CELERY_TASK_SERIALIZER: str = Field(default="json", env="CELERY_TASK_SERIALIZER")
    CELERY_RESULT_SERIALIZER: str = Field(default="json", env="CELERY_RESULT_SERIALIZER")
    CELERY_ACCEPT_CONTENT: List[str] = Field(default=["json"], env="CELERY_ACCEPT_CONTENT")
    CELERY_TIMEZONE: str = Field(default="UTC", env="CELERY_TIMEZONE")
    CELERY_ENABLE_UTC: bool = Field(default=True, env="CELERY_ENABLE_UTC")
    
    # LLM Configuration
    OPENAI_API_KEY: Optional[str] = Field(None, env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    PERPLEXITY_API_KEY: Optional[str] = Field(None, env="PERPLEXITY_API_KEY")
    GOOGLE_API_KEY: Optional[str] = Field(None, env="GOOGLE_API_KEY")
    MISTRAL_API_KEY: Optional[str] = Field(None, env="MISTRAL_API_KEY")
    XAI_API_KEY: Optional[str] = Field(None, env="XAI_API_KEY")
    AZURE_OPENAI_API_KEY: Optional[str] = Field(None, env="AZURE_OPENAI_API_KEY")
    OLLAMA_API_KEY: Optional[str] = Field(None, env="OLLAMA_API_KEY")
    GITHUB_API_KEY: Optional[str] = Field(None, env="GITHUB_API_KEY")
    LLM_API_KEY: Optional[str] = Field(None, env="LLM_API_KEY")
    LLM_PROVIDER: str = Field(default="openai", env="LLM_PROVIDER")
    LLM_MODEL: str = Field(default="gpt-4o", env="LLM_MODEL")
    LLM_ENDPOINT: Optional[str] = Field(None, env="LLM_ENDPOINT")
    DEFAULT_LLM_MODEL: str = Field(default="gpt-4o", env="DEFAULT_LLM_MODEL")
    EMBEDDING_MODEL: str = Field(default="text-embedding-3-large", env="EMBEDDING_MODEL")
    
    # Context Engineering Configuration
    MAX_CONTEXT_WINDOW: int = Field(default=128000, env="MAX_CONTEXT_WINDOW")
    COMPRESSION_RATIO: float = Field(default=0.5, env="COMPRESSION_RATIO")
    CHUNK_SIZE: int = Field(default=1024, env="CHUNK_SIZE")
    CHUNK_OVERLAP: int = Field(default=128, env="CHUNK_OVERLAP")
    
    # File Processing
    MAX_FILE_SIZE: int = Field(default=104857600, env="MAX_FILE_SIZE")  # 100 MB
    UPLOAD_PATH: str = Field(default="/app/uploads", env="UPLOAD_PATH")
    PROCESSED_PATH: str = Field(default="/app/processed", env="PROCESSED_PATH")
    MAX_CONCURRENT_UPLOADS: int = Field(default=10, env="MAX_CONCURRENT_UPLOADS")
    SUPPORTED_FILE_TYPES: List[str] = Field(
        default=["json", "csv", "txt", "md", "pdf", "png", "jpg", "jpeg"], 
        env="SUPPORTED_FILE_TYPES"
    )
    
    # Security
    SECRET_KEY: str = Field(default="UC38hxSfHk81WSvF0HGtkM2GY02lz6qeQN4wvtATJI8", env="SECRET_KEY")
    ACCESS_TOKEN_EXPIRE_MINUTES: int = Field(default=30, env="ACCESS_TOKEN_EXPIRE_MINUTES")
    ALGORITHM: str = Field(default="HS256", env="ALGORITHM")
    
    # Metrics
    ENABLE_METRICS: bool = Field(default=True, env="ENABLE_METRICS")
    METRICS_PORT: int = Field(default=9090, env="METRICS_PORT")
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str):
            if not v.startswith("["):
                return [i.strip() for i in v.split(",")]
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [i.strip() for i in v.split(",")]
        return v

    @validator("SUPPORTED_FILE_TYPES", pre=True)
    def assemble_supported_file_types(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse supported file types from string or list."""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [i.strip() for i in v.split(",")]
        return v

    @validator("CELERY_ACCEPT_CONTENT", pre=True)
    def assemble_celery_accept_content(cls, v: Union[str, List[str]]) -> List[str]:
        """Parse Celery accept content from string or list."""
        if isinstance(v, str):
            try:
                return json.loads(v)
            except json.JSONDecodeError:
                return [i.strip() for i in v.split(",")]
        return v

    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = True
        extra = "ignore"  # Allow extra fields


# Create settings instance
settings = Settings() 