"""
Configuration module for document processing with Neo4j, Qdrant, and AI integration.

This module provides configuration for the document processing system,
supporting both direct database access and the Cognee abstraction layer.
"""
import os
import logging
from typing import Dict, Any, Optional, List

logger = logging.getLogger(__name__)

# Import optional dependencies with graceful fallbacks
try:
    import cognee
    COGNEE_AVAILABLE = True
except ImportError:
    COGNEE_AVAILABLE = False
    logger.warning("Cognee is not available. Install with 'pip install cognee[neo4j,qdrant]>=0.1.40'")

try:
    from langchain_xai import ChatXAI
    XAI_AVAILABLE = True
except ImportError:
    XAI_AVAILABLE = False
    logger.warning("LangChain XAI is not available. Install with 'pip install langchain-xai'")

try:
    from langchain_openai import ChatOpenAI
    OPENAI_AVAILABLE = True
except ImportError:
    OPENAI_AVAILABLE = False
    logger.warning("LangChain OpenAI is not available. Install with 'pip install langchain-openai'")

try:
    from pydantic import BaseModel, Field, model_validator
    PYDANTIC_AVAILABLE = True
except ImportError:
    PYDANTIC_AVAILABLE = False
    logger.warning("Pydantic is not available. Install with 'pip install pydantic>=2.0.0'")


# Define models if Pydantic is available
if PYDANTIC_AVAILABLE:
    class DatabaseConfig(BaseModel):
        """Database configuration model."""
        provider: str = Field(..., description="Database provider name")
        host: str = Field(..., description="Database host address")
        port: int = Field(..., description="Database port")
        username: str = Field(..., description="Database username")
        password: str = Field(..., description="Database password")
        name: Optional[str] = Field(None, description="Database name")
        url: Optional[str] = Field(None, description="Database URL")
        key: Optional[str] = Field(None, description="Database API key")

    class AIModelConfig(BaseModel):
        """AI model configuration."""
        provider: str = Field(..., description="AI model provider")
        model_name: str = Field(..., description="Model name/version")
        api_key: str = Field(..., description="API key for the model")
        temperature: float = Field(0.1, description="Temperature parameter")
        max_tokens: Optional[int] = Field(None, description="Maximum tokens to generate")
        endpoint: Optional[str] = Field(None, description="Custom endpoint URL")

    class ProcessorConfig(BaseModel):
        """Main processor configuration model."""
        use_cognee: bool = Field(False, description="Whether to use Cognee")
        enable_ai: bool = Field(False, description="Whether to enable AI enhancements")
        databases: Dict[str, DatabaseConfig] = Field({}, description="Database configurations")
        ai_models: Dict[str, AIModelConfig] = Field({}, description="AI model configurations")
        chunk_size: int = Field(1024, description="Document chunk size")
        chunk_overlap: int = Field(128, description="Chunk overlap size")
        default_model: str = Field("openai", description="Default AI model to use")
        
        @model_validator(mode='after')
        def validate_config(self):
            """Validate configuration."""
            if self.enable_ai and not self.ai_models:
                logger.warning("AI is enabled but no AI models are configured")
            
            if self.use_cognee and not COGNEE_AVAILABLE:
                logger.warning("Cognee is not available but use_cognee is True")
            
            return self


class ProcessingConfig:
    """
    Configuration for document processing system.
    
    This class provides configuration for the document processing system,
    supporting both direct database access and the Cognee abstraction layer,
    as well as AI enhancement capabilities.
    """
    
    def __init__(self, use_cognee: bool = False, enable_ai: bool = False):
        """
        Initialize the processing configuration.
        
        Args:
            use_cognee: Whether to use Cognee
            enable_ai: Whether to enable AI enhancements
        """
        # Set configuration from environment or arguments
        self.use_cognee = use_cognee or os.getenv("USE_COGNEE", "false").lower() == "true"
        self.enable_ai = enable_ai or os.getenv("ENABLE_AI", "false").lower() == "true"
        
        # Load configuration
        self._load_environment()
        self._configure_databases()
        self._configure_ai_models()
        
        # Create Pydantic model if available
        self.config_model = None
        if PYDANTIC_AVAILABLE:
            self._create_config_model()
    
    def _load_environment(self):
        """Load configuration from environment variables."""
        # Document processing configuration
        self.chunk_size = int(os.getenv("CHUNK_SIZE", "1024"))
        self.chunk_overlap = int(os.getenv("CHUNK_OVERLAP", "128"))
        
        # Database configuration
        self.neo4j_uri = os.getenv("NEO4J_URI", "bolt://localhost:7687")
        self.neo4j_username = os.getenv("NEO4J_USERNAME", "neo4j")
        self.neo4j_password = os.getenv("NEO4J_PASSWORD", "")
        
        self.vector_db_url = os.getenv("VECTOR_DB_URL", "")
        self.vector_db_key = os.getenv("VECTOR_DB_KEY", "")
        
        # AI configuration
        self.xai_api_key = os.getenv("XAI_API_KEY", "")
        self.openai_api_key = os.getenv("OPENAI_API_KEY", "")
        
        # Feature flags
        self.log_level = os.getenv("LOG_LEVEL", "INFO")
        logging.basicConfig(level=self.log_level)
    
    def _configure_databases(self):
        """Configure database connections."""
        self.databases = {}
        
        # Configure Neo4j
        self.databases["neo4j"] = {
            "provider": "neo4j",
            "host": self.neo4j_uri,
            "port": 7687,
            "username": self.neo4j_username,
            "password": self.neo4j_password
        }
        
        # Configure Qdrant
        self.databases["qdrant"] = {
            "provider": "qdrant",
            "url": self.vector_db_url,
            "key": self.vector_db_key
        }
        
        # Configure Cognee if available
        if COGNEE_AVAILABLE and self.use_cognee:
            try:
                cognee.config.set_graph_db_provider("neo4j")
                cognee.config.graph_db_url = self.neo4j_uri
                cognee.config.graph_db_username = self.neo4j_username
                cognee.config.graph_db_password = self.neo4j_password
                
                cognee.config.set_vector_db_provider("qdrant")
                cognee.config.vector_db_url = self.vector_db_url
                cognee.config.vector_db_key = self.vector_db_key
                
                cognee.config.chunk_size = self.chunk_size
                cognee.config.chunk_overlap = self.chunk_overlap
                
                self.cognee = cognee
                logger.info("Configured Cognee successfully")
            except Exception as e:
                logger.error(f"Failed to configure Cognee: {e}")
                self.use_cognee = False
    
    def _configure_ai_models(self):
        """Configure AI model integrations."""
        self.ai_models = {}
        self.available_models = []
        
        # Configure xAI if available
        if XAI_AVAILABLE and self.xai_api_key:
            try:
                self.ai_models["xai"] = {
                    "provider": "xai",
                    "model_name": "grok-4",
                    "api_key": self.xai_api_key,
                    "temperature": 0.1
                }
                self.available_models.append("xai")
                logger.info("Configured xAI model")
            except Exception as e:
                logger.error(f"Failed to configure xAI: {e}")
        
        # Configure OpenAI if available
        if OPENAI_AVAILABLE and self.openai_api_key:
            try:
                self.ai_models["openai"] = {
                    "provider": "openai",
                    "model_name": "gpt-4o",
                    "api_key": self.openai_api_key,
                    "temperature": 0.1
                }
                self.available_models.append("openai")
                logger.info("Configured OpenAI model")
            except Exception as e:
                logger.error(f"Failed to configure OpenAI: {e}")
        
        # Set default model
        self.default_model = os.getenv("DEFAULT_AI_MODEL", "openai")
        if self.default_model not in self.available_models and self.available_models:
            self.default_model = self.available_models[0]
            logger.warning(f"Default AI model not available, using {self.default_model} instead")
    
    def _create_config_model(self):
        """Create a Pydantic model from the configuration."""
        if not PYDANTIC_AVAILABLE:
            return
        
        try:
            # Create database configs
            db_configs = {}
            for db_name, db_info in self.databases.items():
                db_configs[db_name] = DatabaseConfig(**db_info)
            
            # Create AI model configs
            ai_configs = {}
            for model_name, model_info in self.ai_models.items():
                ai_configs[model_name] = AIModelConfig(**model_info)
            
            # Create main config
            self.config_model = ProcessorConfig(
                use_cognee=self.use_cognee,
                enable_ai=self.enable_ai,
                databases=db_configs,
                ai_models=ai_configs,
                chunk_size=self.chunk_size,
                chunk_overlap=self.chunk_overlap,
                default_model=self.default_model
            )
        except Exception as e:
            logger.error(f"Failed to create Pydantic model: {e}")
    
    def get_ai_model(self, model_name: Optional[str] = None):
        """
        Get an AI model client.
        
        Args:
            model_name: Name of the model to get (default: use default_model)
            
        Returns:
            AI model client or None if not available
        """
        if not self.enable_ai:
            logger.warning("AI is not enabled")
            return None
        
        # Use default model if not specified
        model_name = model_name or self.default_model
        
        # Check if model is available
        if model_name not in self.ai_models:
            logger.warning(f"Model {model_name} not available")
            return None
        
        # Get model configuration
        model_config = self.ai_models[model_name]
        
        # Initialize model client
        if model_name == "xai":
            if not XAI_AVAILABLE:
                logger.warning("XAI is not available")
                return None
            
            try:
                return ChatXAI(
                    xai_api_key=model_config["api_key"],
                    model=model_config["model_name"],
                    temperature=model_config["temperature"]
                )
            except Exception as e:
                logger.error(f"Failed to initialize XAI model: {e}")
                return None
        
        elif model_name == "openai":
            if not OPENAI_AVAILABLE:
                logger.warning("OpenAI is not available")
                return None
            
            try:
                return ChatOpenAI(
                    api_key=model_config["api_key"],
                    model=model_config["model_name"],
                    temperature=model_config["temperature"]
                )
            except Exception as e:
                logger.error(f"Failed to initialize OpenAI model: {e}")
                return None
        
        logger.warning(f"Unknown model provider: {model_name}")
        return None
    
    def to_dict(self) -> Dict[str, Any]:
        """
        Convert configuration to dictionary.
        
        Returns:
            Dictionary representation of the configuration
        """
        # Use Pydantic model if available
        if PYDANTIC_AVAILABLE and self.config_model:
            return self.config_model.model_dump()
        
        # Manual conversion
        return {
            "use_cognee": self.use_cognee,
            "enable_ai": self.enable_ai,
            "chunk_size": self.chunk_size,
            "chunk_overlap": self.chunk_overlap,
            "default_model": self.default_model,
            "available_models": self.available_models,
            "databases": self.databases,
            "ai_models": {k: {**v, "api_key": "****"} for k, v in self.ai_models.items()}  # Redact API keys
        }


# Create a default instance for convenience
default_config = ProcessingConfig() 