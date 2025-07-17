"""
Base document processor module.

This module defines the base class for document processors and common utilities.
It combines functionality from the original processors system and the advanced
doc_process system, providing enhanced capabilities with AI integration.
"""
import logging
import os
from abc import ABC, abstractmethod
from datetime import datetime
from typing import Dict, List, Any, Optional, Union

# Import database clients for direct database operations
from app.db.neo4j_client import Neo4jClient
from app.db.qdrant_client import QdrantClient

logger = logging.getLogger(__name__)

# Try to import optional dependencies with fallbacks
try:
    import cognee
    from cognee.api.v1.search import SearchType
    COGNEE_AVAILABLE = True
except ImportError:
    COGNEE_AVAILABLE = False
    logger.warning("Cognee not available. Some advanced features will be disabled.")

try:
    from langchain_xai import ChatXAI
    XAI_AVAILABLE = True
except ImportError:
    XAI_AVAILABLE = False
    logger.warning("LangChain XAI not available. AI enhancements will be disabled.")


class DatabaseAdapter:
    """
    Adapter for database operations that can use either direct database
    clients or the Cognee abstraction layer.
    """
    
    def __init__(self, use_cognee: bool = False):
        """
        Initialize the database adapter.
        
        Args:
            use_cognee: Whether to use Cognee for database operations
        """
        self.use_cognee = use_cognee and COGNEE_AVAILABLE
        
        if self.use_cognee:
            # Initialize Cognee
            try:
                cognee.config.set_vector_db_provider("qdrant")
                cognee.config.set_graph_db_provider("neo4j")
                cognee.config.vector_db_url = os.getenv("VECTOR_DB_URL", "")
                cognee.config.vector_db_key = os.getenv("VECTOR_DB_KEY", "")
                cognee.config.graph_db_url = os.getenv("NEO4J_URI", "")
                cognee.config.graph_db_username = os.getenv("NEO4J_USERNAME", "")
                cognee.config.graph_db_password = os.getenv("NEO4J_PASSWORD", "")
                cognee.config.chunk_size = 1024
                cognee.config.chunk_overlap = 128
                self.cognee = cognee
            except Exception as e:
                logger.error(f"Failed to initialize Cognee: {e}")
                self.use_cognee = False
        
        # Always initialize direct clients as fallback
        self.neo4j_client = Neo4jClient()
        self.qdrant_client = QdrantClient()
    
    async def store_in_knowledge_graph(self, data: Dict[str, Any]) -> Optional[str]:
        """
        Store data in the knowledge graph.
        
        Args:
            data: Data to store
            
        Returns:
            ID of the stored node
        """
        if self.use_cognee:
            try:
                # Use Cognee's graph functionality
                await self.cognee.add_to_graph(data)
                return data.get("id")
            except Exception as e:
                logger.error(f"Cognee graph storage failed: {e}, falling back to direct Neo4j")
        
        # Create a node in Neo4j
        query = """
        CREATE (d:Document {
            id: $id,
            title: $title,
            content_type: $content_type,
            created_at: $created_at,
            updated_at: $updated_at
        })
        RETURN d.id as id
        """
        
        params = {
            "id": data.get("id", str(datetime.now().timestamp())),
            "title": data.get("title", "Untitled Document"),
            "content_type": data.get("content_type", "text"),
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        result = await self.neo4j_client.run_query(query, params)
        return result[0]["id"] if result else None
    
    async def store_in_vector_db(self, embedding: List[float], metadata: Dict[str, Any]) -> Optional[str]:
        """
        Store embedding in vector database.
        
        Args:
            embedding: Vector embedding
            metadata: Metadata to store with the embedding
            
        Returns:
            ID of the stored vector
        """
        if self.use_cognee:
            try:
                # Use Cognee's vector database functionality
                await self.cognee.add_to_vector_db(embedding, metadata)
                return metadata.get("id")
            except Exception as e:
                logger.error(f"Cognee vector storage failed: {e}, falling back to direct Qdrant")
        
        # Store in Qdrant
        ids = await self.qdrant_client.store_vectors(
            vectors=[embedding],
            metadata=[metadata],
            ids=[metadata.get("id")]
        )
        return ids[0] if ids else None


class AIEnhancementLayer:
    """
    Optional AI enhancement layer for document processing.
    Provides advanced analysis capabilities when available.
    """
    
    def __init__(self):
        """Initialize the AI enhancement layer."""
        self.ai_model = None
        self.initialized = False
        
        # Try to initialize the AI model
        self._initialize_model()
    
    def _initialize_model(self):
        """Initialize the AI model based on available providers."""
        if not self.initialized:
            # Try XAI (Grok) first
            if XAI_AVAILABLE and os.getenv("XAI_API_KEY"):
                try:
                    self.ai_model = ChatXAI(
                        xai_api_key=os.getenv("XAI_API_KEY"),
                        model="grok-4",
                        temperature=0.1
                    )
                    self.initialized = True
                    logger.info("Initialized XAI enhancement layer with Grok-4")
                except Exception as e:
                    logger.error(f"Failed to initialize XAI: {e}")
            
            # Try OpenAI if XAI is not available
            if not self.initialized:
                try:
                    from langchain_openai import ChatOpenAI
                    if os.getenv("OPENAI_API_KEY"):
                        self.ai_model = ChatOpenAI(
                            api_key=os.getenv("OPENAI_API_KEY"),
                            model="gpt-4o",
                            temperature=0.1
                        )
                        self.initialized = True
                        logger.info("Initialized OpenAI enhancement layer with GPT-4o")
                except ImportError:
                    logger.warning("LangChain OpenAI not available")
    
    async def enhance_content(self, content: Any, content_type: str, enhancement_type: str = "analysis") -> Optional[str]:
        """
        Enhance content with AI analysis.
        
        Args:
            content: Content to enhance
            content_type: Type of content
            enhancement_type: Type of enhancement to perform
            
        Returns:
            Enhanced content or None if enhancement fails
        """
        if not self.initialized or not self.ai_model:
            logger.warning("AI enhancement requested but no AI model is available")
            return None
        
        # Create prompt based on content type and enhancement type
        prompt = self._create_enhancement_prompt(content, content_type, enhancement_type)
        
        try:
            # Invoke the AI model
            result = await self.ai_model.ainvoke(prompt)
            return result.content if hasattr(result, "content") else str(result)
        except Exception as e:
            logger.error(f"AI enhancement failed: {e}")
            return None
    
    def _create_enhancement_prompt(self, content: Any, content_type: str, enhancement_type: str) -> str:
        """
        Create a prompt for AI enhancement.
        
        Args:
            content: Content to enhance
            content_type: Type of content
            enhancement_type: Type of enhancement
            
        Returns:
            Prompt for the AI model
        """
        # Base prompt template
        if enhancement_type == "analysis":
            return f"""
            Analyze the following {content_type} content and provide insights:
            
            {content}
            
            Extract:
            1. Key topics and themes
            2. Important entities and relationships
            3. Main insights and findings
            4. Structure and organization
            """
        elif enhancement_type == "summary":
            return f"""
            Summarize the following {content_type} content:
            
            {content}
            
            Provide a concise summary highlighting the most important information.
            """
        else:
            return f"""
            Process the following {content_type} content for {enhancement_type}:
            
            {content}
            """


class BaseProcessor(ABC):
    """
    Enhanced base class for document processors.
    
    This abstract class defines the interface and common functionality
    for all document processors in the system, combining features from
    the original processors and the advanced doc_process system.
    """
    
    def __init__(
        self,
        dataset_name: str = None,
        use_cognee: bool = False,
        enable_ai: bool = False
    ):
        """
        Initialize the base processor.
        
        Args:
            dataset_name: Name of the dataset (for Cognee integration)
            use_cognee: Whether to use Cognee for database operations
            enable_ai: Whether to enable AI enhancements
        """
        # Set up database adapter
        self.db_adapter = DatabaseAdapter(use_cognee=use_cognee)
        
        # Set up AI enhancement layer if enabled
        self.enable_ai = enable_ai
        if enable_ai:
            self.ai_layer = AIEnhancementLayer()
        
        # Set dataset name for Cognee
        self.dataset_name = dataset_name or self.__class__.__name__.lower()
        
        # Initialize metadata
        self.metadata = {}
    
    @abstractmethod
    async def process(self, content: Any, **kwargs) -> Dict[str, Any]:
        """
        Process the document content.
        
        Args:
            content: Document content to process
            **kwargs: Additional processing options
            
        Returns:
            Processing result
        """
        pass
    
    async def process_with_enhancements(self, content: Any, **kwargs) -> Dict[str, Any]:
        """
        Process the document content with AI enhancements if enabled.
        
        Args:
            content: Document content to process
            **kwargs: Additional processing options
            
        Returns:
            Enhanced processing result
        """
        # Standard processing first
        result = await self.process(content, **kwargs)
        
        # Apply AI enhancements if enabled
        if self.enable_ai and hasattr(self, "ai_layer"):
            content_type = kwargs.get("content_type") or self._detect_content_type(content)
            enhancement_type = kwargs.get("enhancement_type", "analysis")
            
            enhanced_content = await self.ai_layer.enhance_content(
                content=result.get("processed_content", content),
                content_type=content_type,
                enhancement_type=enhancement_type
            )
            
            if enhanced_content:
                result["enhanced_content"] = enhanced_content
                result["has_enhancements"] = True
        
        return result
    
    def _detect_content_type(self, content: Any) -> str:
        """
        Detect the content type based on the content itself.
        
        Args:
            content: Content to detect type for
            
        Returns:
            Detected content type
        """
        # Simple detection based on content
        if isinstance(content, str):
            if content.strip().startswith(("{", "[")):
                return "application/json"
            elif content.strip().startswith("#"):
                return "text/markdown"
            else:
                return "text/plain"
        elif isinstance(content, bytes):
            if content.startswith(b"%PDF"):
                return "application/pdf"
            elif content.startswith((b"\x89PNG", b"\xFF\xD8\xFF")):
                return "image"
            else:
                return "application/octet-stream"
        else:
            return "unknown"
    
    async def extract_text(self, content: Any) -> str:
        """
        Extract text from content.
        
        Args:
            content: Content to extract text from
            
        Returns:
            Extracted text
        """
        # Default implementation returns content as string if possible
        if isinstance(content, str):
            return content
        elif hasattr(content, "read"):
            return await content.read()
        else:
            return str(content)
    
    async def generate_embeddings(self, text: str, model: str = "text-embedding-3-large") -> List[float]:
        """
        Generate embeddings for text.
        
        Args:
            text: Text to generate embeddings for
            model: Embedding model to use
            
        Returns:
            Vector embedding
        """
        # If Cognee is available, try to use it for embeddings
        if self.db_adapter.use_cognee:
            try:
                embedding = await self.db_adapter.cognee.generate_embedding(text)
                return embedding
            except Exception as e:
                logger.error(f"Cognee embedding generation failed: {e}, falling back to mock")
        
        # Placeholder for actual embedding generation
        # In a real implementation, this would call an embedding API
        logger.info(f"Using mock embeddings with model: {model}")
        
        # Return a mock embedding (would be replaced with actual API call)
        return [0.0] * 1536  # OpenAI embeddings are 1536 dimensions
    
    async def store_in_knowledge_graph(self, data: Dict[str, Any]) -> str:
        """
        Store data in the knowledge graph.
        
        Args:
            data: Data to store
            
        Returns:
            ID of the stored node
        """
        return await self.db_adapter.store_in_knowledge_graph(data)
    
    async def store_in_vector_db(self, embedding: List[float], metadata: Dict[str, Any]) -> str:
        """
        Store embedding in vector database.
        
        Args:
            embedding: Vector embedding
            metadata: Metadata to store with the embedding
            
        Returns:
            ID of the stored vector
        """
        return await self.db_adapter.store_in_vector_db(embedding, metadata)
    
    async def search_content(self, query: str) -> List[Dict[str, Any]]:
        """
        Search processed content.
        
        Args:
            query: Search query
            
        Returns:
            Search results
        """
        if self.db_adapter.use_cognee:
            try:
                results = await self.db_adapter.cognee.search(
                    query_text=query,
                    query_type=SearchType.INSIGHTS if self.enable_ai else SearchType.RELEVANT
                )
                return results
            except Exception as e:
                logger.error(f"Cognee search failed: {e}, falling back to direct search")
        
        # Fallback to direct search
        # This would be implemented with direct vector search in Qdrant
        logger.warning("Direct vector search not fully implemented")
        return []
    
    def add_metadata(self, key: str, value: Any) -> None:
        """
        Add metadata to the processor.
        
        Args:
            key: Metadata key
            value: Metadata value
        """
        self.metadata[key] = value
    
    def get_metadata(self) -> Dict[str, Any]:
        """
        Get all metadata.
        
        Returns:
            Metadata dictionary
        """
        return self.metadata.copy() 