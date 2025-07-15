"""
Configuration settings for the AI Context Builder backend.
"""
from typing import Dict, List, Optional, Any

from pydantic import AnyHttpUrl, Field, PostgresDsn, RedisDsn
from pydantic_settings import BaseSettings, SettingsConfigDict


class Settings(BaseSettings):
    """Application settings."""
    
    # API Configuration
    API_HOST: str = "0.0.0.0"
    API_PORT: int = 8000
    DEBUG: bool = False
    ENVIRONMENT: str = "production"
    
    # CORS
    CORS_ORIGINS: List[AnyHttpUrl] = Field(
        default=["http://localhost:3000", "http://localhost:8000"],
        description="List of allowed CORS origins"
    )
    
    # Database Connections
    # PostgreSQL
    POSTGRES_USER: str
    POSTGRES_PASSWORD: str
    POSTGRES_HOST: str
    POSTGRES_PORT: int = 5432
    POSTGRES_DB: str
    
    @property
    def POSTGRES_DSN(self) -> PostgresDsn:
        """Get PostgreSQL DSN."""
        return f"postgresql://{self.POSTGRES_USER}:{self.POSTGRES_PASSWORD}@{self.POSTGRES_HOST}:{self.POSTGRES_PORT}/{self.POSTGRES_DB}"
    
    # Neo4j
    NEO4J_URI: str
    NEO4J_USER: str
    NEO4J_PASSWORD: str
    NEO4J_DATABASE: str
    
    # Redis
    REDIS_HOST: str
    REDIS_PORT: int = 6379
    REDIS_DB: int = 0
    REDIS_PASSWORD: Optional[str] = None
    
    @property
    def REDIS_DSN(self) -> RedisDsn:
        """Get Redis DSN."""
        if self.REDIS_PASSWORD:
            return f"redis://:{self.REDIS_PASSWORD}@{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
        return f"redis://{self.REDIS_HOST}:{self.REDIS_PORT}/{self.REDIS_DB}"
    
    # Qdrant Vector DB
    QDRANT_HOST: str
    QDRANT_PORT: int = 6333
    QDRANT_COLLECTION: str
    
    # LLM API Keys
    OPENAI_API_KEY: str
    ANTHROPIC_API_KEY: Optional[str] = None
    
    # LLM Providers (for LiteLLM)
    LITELLM_PROVIDERS: Dict[str, Dict[str, Any]] = Field(
        default_factory=lambda: {
            "openai": {
                "api_key": None,  # Will be set from OPENAI_API_KEY
                "chat_model": "gpt-4o",
                "embedding_model": "text-embedding-3-large",
            },
            "anthropic": {
                "api_key": None,  # Will be set from ANTHROPIC_API_KEY
                "chat_model": "claude-3-5-sonnet-20241022",
            },
        },
        description="Configurations for LiteLLM providers."
    )
    DEFAULT_CHAT_PROVIDER: str = "openai"
    DEFAULT_EMBEDDING_PROVIDER: str = "openai"
    DEFAULT_VOICE_PROVIDER: str = "openai"
    
    # Celery Configuration
    CELERY_BROKER_URL: str
    CELERY_RESULT_BACKEND: str
    
    # Cognee Configuration
    COGNEE_EMBEDDINGS_MODEL: str = "text-embedding-ada-002"
    COGNEE_LLM_MODEL: str = "gpt-4-turbo"
    COGNEE_CHUNK_SIZE: int = 1000
    COGNEE_CHUNK_OVERLAP: int = 200
    
    model_config = SettingsConfigDict(
        env_file=".env",
        env_file_encoding="utf-8",
        case_sensitive=True,
    )

    def __init__(self, **kwargs):
        super().__init__(**kwargs)
        # Set API keys from environment variables
        if self.OPENAI_API_KEY:
            self.LITELLM_PROVIDERS["openai"]["api_key"] = self.OPENAI_API_KEY
        if self.ANTHROPIC_API_KEY:
            self.LITELLM_PROVIDERS["anthropic"]["api_key"] = self.ANTHROPIC_API_KEY
    
    @property
    def cors_origins_list(self) -> List[str]:
        """Get CORS origins as a list."""
        return [str(origin) for origin in self.CORS_ORIGINS]


# Create settings instance
settings = Settings()
