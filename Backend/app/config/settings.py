"""
Configuration settings for the AI Context Engineering Agent.
"""
import os
from typing import List, Optional, Union

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
    
    # Neo4j Configuration
    NEO4J_HOST: str = Field(default="localhost", env="NEO4J_HOST")
    NEO4J_PORT: int = Field(default=7687, env="NEO4J_PORT")
    NEO4J_USER: str = Field(default="neo4j", env="NEO4J_USER")
    NEO4J_PASSWORD: str = Field(default="password", env="NEO4J_PASSWORD")
    
    @property
    def NEO4J_URI(self) -> str:
        """Get the Neo4j URI based on environment."""
        return f"bolt://{self.NEO4J_HOST}:{self.NEO4J_PORT}"
    
    # Qdrant Configuration
    QDRANT_HOST: str = Field(default="localhost", env="QDRANT_HOST")
    QDRANT_PORT: int = Field(default=6333, env="QDRANT_PORT")
    QDRANT_COLLECTION: str = Field(default="context_vectors", env="QDRANT_COLLECTION")
    
    # LLM Configuration
    OPENAI_API_KEY: Optional[str] = Field(None, env="OPENAI_API_KEY")
    ANTHROPIC_API_KEY: Optional[str] = Field(None, env="ANTHROPIC_API_KEY")
    DEFAULT_LLM_MODEL: str = Field(default="gpt-4o", env="DEFAULT_LLM_MODEL")
    
    # Context Engineering Configuration
    MAX_CONTEXT_WINDOW: int = Field(default=128000, env="MAX_CONTEXT_WINDOW")
    COMPRESSION_RATIO: float = Field(default=0.5, env="COMPRESSION_RATIO")
    
    @validator("CORS_ORIGINS", pre=True)
    def assemble_cors_origins(cls, v: Union[str, List[str]]) -> Union[List[str], str]:
        """Parse CORS origins from string or list."""
        if isinstance(v, str) and not v.startswith("["):
            return [i.strip() for i in v.split(",")]
        elif isinstance(v, (list, str)):
            return v
        raise ValueError(v)

    class Config:
        """Pydantic config."""
        env_file = ".env"
        case_sensitive = True


# Create settings instance
settings = Settings() 