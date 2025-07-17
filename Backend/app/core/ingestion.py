"""
Ingestion Manager.

This module handles the ingestion of various data sources,
including URLs, files, and raw text. It processes the data
and stores it in the knowledge graph and vector database.
Enhanced with optional AI capabilities and Cognee integration.
"""
import uuid
import json
import os
import tempfile
import logging
import asyncio
from datetime import datetime
from typing import Dict, List, Optional, Any, Union, BinaryIO
from fastapi import UploadFile
import httpx
from pathlib import Path

from app.db.neo4j_client import Neo4jClient
from app.db.qdrant_client import QdrantClient
from app.schemas.ingestion import IngestionStatus
from app.processors import ProcessorFactory

logger = logging.getLogger(__name__)

class IngestionManager:
    """
    Manager for data ingestion operations.
    
    This class provides methods for ingesting various types of data
    sources and processing them for storage in the knowledge graph
    and vector database. Supports enhanced processing capabilities.
    """
    
    def __init__(self, use_cognee: bool = False, enable_ai: bool = False):
        """
        Initialize the ingestion manager.
        
        Args:
            use_cognee: Whether to use Cognee for database operations
            enable_ai: Whether to enable AI enhancements
        """
        # Check environment variables for feature flags
        self.use_cognee = use_cognee or os.getenv("USE_COGNEE", "false").lower() == "true"
        self.enable_ai = enable_ai or os.getenv("ENABLE_AI", "false").lower() == "true"
        
        # Initialize database clients
        self.neo4j_client = Neo4jClient()
        self.qdrant_client = QdrantClient()
        
        # In-memory store for job status (replace with Redis in production)
        self.job_store = {}
        
        logger.info(f"Initialized IngestionManager with use_cognee={self.use_cognee}, enable_ai={self.enable_ai}")
    
    async def ingest_url(
        self,
        url: str,
        metadata: Optional[Dict[str, Any]] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Ingest content from a URL.
        
        Args:
            url: URL to ingest
            metadata: Additional metadata
            options: Ingestion options
            
        Returns:
            Job ID for tracking the ingestion process
        """
        # Generate a job ID
        job_id = str(uuid.uuid4())
        
        # Initialize job status
        self.job_store[job_id] = {
            "status": "processing",
            "progress": 0.0,
            "source_type": "url",
            "source": url,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Process asynchronously
        asyncio.create_task(self._process_url(job_id, url, metadata or {}, options or {}))
        
        return job_id
    
    async def _process_url(
        self,
        job_id: str,
        url: str,
        metadata: Dict[str, Any],
        options: Dict[str, Any]
    ) -> None:
        """
        Process a URL asynchronously.
        
        Args:
            job_id: Job ID
            url: URL to process
            metadata: Additional metadata
            options: Processing options
        """
        try:
            # Extract processing options
            use_cognee = options.get("use_cognee", self.use_cognee)
            enable_ai = options.get("enable_ai", self.enable_ai)
            dataset_name = options.get("dataset_name", f"url_{job_id}")
            
            # Update job status
            self._update_job_status(job_id, progress=10.0, message="Fetching URL content")
            
            # Fetch content from URL
            async with httpx.AsyncClient(timeout=30.0) as client:
                response = await client.get(url)
                response.raise_for_status()
                
                # Get content type
                content_type = response.headers.get('content-type', '').split(';')[0]
                
                # Update metadata with URL info
                metadata.update({
                    "url": url,
                    "content_type": content_type,
                    "fetch_date": datetime.now().isoformat(),
                    "status_code": response.status_code
                })
                
                # Update job status
                self._update_job_status(job_id, progress=30.0, message="Processing content")
                
                # Get appropriate processor with enhancement options
                try:
                    processor = ProcessorFactory.get_processor_for_content_type(
                        content_type,
                        use_cognee=use_cognee,
                        enable_ai=enable_ai,
                        dataset_name=dataset_name
                    )
                except ValueError:
                    # If no specific processor is available, use optimal processor
                    processor = ProcessorFactory.get_optimal_processor(
                        response.content, 
                        content_type=content_type,
                        use_cognee=use_cognee,
                        enable_ai=enable_ai,
                        dataset_name=dataset_name
                    )
                
                # Process content with or without enhancements
                if enable_ai:
                    result = await processor.process_with_enhancements(
                        response.content, 
                        metadata=metadata
                    )
                else:
                    result = await processor.process(
                        response.content, 
                        metadata=metadata
                    )
                
                # Update job status
                self._update_job_status(job_id, progress=70.0, message="Storing processed content")
                
                # Store in Neo4j and Qdrant (handled by processor)
                document_id = f"url_{job_id}"
                
                # Update job status
                self._update_job_status(
                    job_id, 
                    status="completed", 
                    progress=100.0, 
                    message="URL processing completed",
                    result={
                        "document_id": document_id,
                        "chunks_count": len(result.get("chunks", [])),
                        "has_enhancements": result.get("has_enhancements", False),
                        "metadata": result.get("metadata", {})
                    }
                )
                
        except Exception as e:
            logger.error(f"Error processing URL {url}: {str(e)}", exc_info=True)
            self._update_job_status(
                job_id,
                status="failed",
                progress=0.0,
                message=f"URL processing failed: {str(e)}"
            )
    
    async def ingest_file(
        self,
        file: UploadFile,
        metadata: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Ingest content from a file.
        
        Args:
            file: Uploaded file
            metadata: Additional metadata as JSON string
            options: Processing options
            
        Returns:
            Job ID for tracking the ingestion process
        """
        # Generate a job ID
        job_id = str(uuid.uuid4())
        
        # Parse metadata if provided
        meta_dict = json.loads(metadata) if metadata else {}
        
        # Add file info to metadata
        meta_dict.update({
            "filename": file.filename,
            "content_type": file.content_type,
            "upload_date": datetime.now().isoformat()
        })
        
        # Initialize job status
        self.job_store[job_id] = {
            "status": "processing",
            "progress": 0.0,
            "source_type": "file",
            "source": file.filename,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Process asynchronously
        asyncio.create_task(self._process_file(job_id, file, meta_dict, options or {}))
        
        return job_id
    
    async def _process_file(
        self,
        job_id: str,
        file: UploadFile,
        metadata: Dict[str, Any],
        options: Dict[str, Any]
    ) -> None:
        """
        Process a file asynchronously.
        
        Args:
            job_id: Job ID
            file: Uploaded file
            metadata: Additional metadata
            options: Processing options
        """
        temp_file_path = None
        
        try:
            # Extract processing options
            use_cognee = options.get("use_cognee", self.use_cognee)
            enable_ai = options.get("enable_ai", self.enable_ai)
            dataset_name = options.get("dataset_name", f"file_{job_id}")
            
            # Update job status
            self._update_job_status(job_id, progress=10.0, message="Saving file")
            
            # Save file to temporary location
            content = await file.read()
            
            with tempfile.NamedTemporaryFile(delete=False, suffix=Path(file.filename).suffix) as temp_file:
                temp_file.write(content)
                temp_file_path = temp_file.name
            
            # Update job status
            self._update_job_status(job_id, progress=30.0, message="Processing file")
            
            # Get appropriate processor based on file extension with enhancement options
            try:
                processor = ProcessorFactory.get_processor_for_file(
                    temp_file_path,
                    use_cognee=use_cognee,
                    enable_ai=enable_ai,
                    dataset_name=dataset_name
                )
            except ValueError:
                # If no specific processor is available, use optimal processor
                processor = ProcessorFactory.get_optimal_processor(
                    content,
                    content_type=file.content_type,
                    use_cognee=use_cognee,
                    enable_ai=enable_ai,
                    dataset_name=dataset_name
                )
            
            # Process file with or without enhancements
            with open(temp_file_path, 'rb') as f:
                if enable_ai:
                    result = await processor.process_with_enhancements(f, metadata=metadata)
                else:
                    result = await processor.process(f, metadata=metadata)
            
            # Update job status
            self._update_job_status(job_id, progress=70.0, message="Storing processed content")
            
            # Store in Neo4j and Qdrant (handled by processor)
            document_id = f"file_{job_id}"
            
            # Update job status
            self._update_job_status(
                job_id, 
                status="completed", 
                progress=100.0, 
                message="File processing completed",
                result={
                    "document_id": document_id,
                    "chunks_count": len(result.get("chunks", [])),
                    "has_enhancements": result.get("has_enhancements", False),
                    "metadata": result.get("metadata", {})
                }
            )
        
        except Exception as e:
            logger.error(f"Error processing file {file.filename}: {str(e)}", exc_info=True)
            self._update_job_status(
                job_id,
                status="failed",
                progress=0.0,
                message=f"File processing failed: {str(e)}"
            )
        
        finally:
            # Clean up temporary file
            if temp_file_path and os.path.exists(temp_file_path):
                os.unlink(temp_file_path)
    
    async def ingest_text(
        self,
        text: str,
        metadata: Optional[str] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Ingest raw text content.
        
        Args:
            text: Text content to ingest
            metadata: Additional metadata as JSON string
            options: Processing options
            
        Returns:
            Job ID for tracking the ingestion process
        """
        # Generate a job ID
        job_id = str(uuid.uuid4())
        
        # Parse metadata if provided
        meta_dict = json.loads(metadata) if metadata else {}
        
        # Add text info to metadata
        meta_dict.update({
            "content_type": "text/plain",
            "ingestion_date": datetime.now().isoformat(),
            "length": len(text)
        })
        
        # Initialize job status
        self.job_store[job_id] = {
            "status": "processing",
            "progress": 0.0,
            "source_type": "text",
            "source": text[:50] + "..." if len(text) > 50 else text,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Process asynchronously
        asyncio.create_task(self._process_text(job_id, text, meta_dict, options or {}))
        
        return job_id
    
    async def _process_text(
        self,
        job_id: str,
        text: str,
        metadata: Dict[str, Any],
        options: Dict[str, Any]
    ) -> None:
        """
        Process text content asynchronously.
        
        Args:
            job_id: Job ID
            text: Text content
            metadata: Additional metadata
            options: Processing options
        """
        try:
            # Extract processing options
            use_cognee = options.get("use_cognee", self.use_cognee)
            enable_ai = options.get("enable_ai", self.enable_ai)
            dataset_name = options.get("dataset_name", f"text_{job_id}")
            
            # Update job status
            self._update_job_status(job_id, progress=30.0, message="Processing text")
            
            # Get text processor with enhancement options
            processor = ProcessorFactory.get_processor_for_content_type(
                "text/plain",
                use_cognee=use_cognee,
                enable_ai=enable_ai,
                dataset_name=dataset_name
            )
            
            # Process text with or without enhancements
            if enable_ai:
                result = await processor.process_with_enhancements(text, metadata=metadata)
            else:
                result = await processor.process(text, metadata=metadata)
            
            # Update job status
            self._update_job_status(job_id, progress=70.0, message="Storing processed content")
            
            # Store in Neo4j and Qdrant (handled by processor)
            document_id = f"text_{job_id}"
            
            # Update job status
            self._update_job_status(
                job_id, 
                status="completed", 
                progress=100.0, 
                message="Text processing completed",
                result={
                    "document_id": document_id,
                    "chunks_count": len(result.get("chunks", [])),
                    "has_enhancements": result.get("has_enhancements", False),
                    "metadata": result.get("metadata", {})
                }
            )
            
        except Exception as e:
            logger.error(f"Error processing text: {str(e)}", exc_info=True)
            self._update_job_status(
                job_id,
                status="failed",
                progress=0.0,
                message=f"Text processing failed: {str(e)}"
            )
    
    async def ingest_with_privacy(
        self,
        content: Any,
        content_type: str,
        redact_pii: bool = True,
        pii_types: Optional[List[str]] = None,
        metadata: Optional[Dict[str, Any]] = None,
        options: Optional[Dict[str, Any]] = None
    ) -> str:
        """
        Ingest content with privacy compliance.
        
        Args:
            content: Content to ingest
            content_type: Type of content (MIME type)
            redact_pii: Whether to redact personally identifiable information
            pii_types: Types of PII to redact (email, phone, etc.)
            metadata: Additional metadata
            options: Processing options
            
        Returns:
            Job ID for tracking the ingestion process
        """
        # Generate a job ID
        job_id = str(uuid.uuid4())
        
        # Initialize job status
        self.job_store[job_id] = {
            "status": "processing",
            "progress": 0.0,
            "source_type": "privacy",
            "source": content_type,
            "created_at": datetime.now().isoformat(),
            "updated_at": datetime.now().isoformat()
        }
        
        # Process asynchronously
        asyncio.create_task(
            self._process_with_privacy(
                job_id, 
                content, 
                content_type, 
                redact_pii, 
                pii_types, 
                metadata or {}, 
                options or {}
            )
        )
        
        return job_id
    
    async def _process_with_privacy(
        self,
        job_id: str,
        content: Any,
        content_type: str,
        redact_pii: bool,
        pii_types: Optional[List[str]],
        metadata: Dict[str, Any],
        options: Dict[str, Any]
    ) -> None:
        """
        Process content with privacy compliance asynchronously.
        
        Args:
            job_id: Job ID
            content: Content to process
            content_type: Type of content
            redact_pii: Whether to redact PII
            pii_types: Types of PII to redact
            metadata: Additional metadata
            options: Processing options
        """
        try:
            # Extract processing options
            use_cognee = options.get("use_cognee", self.use_cognee)
            enable_ai = options.get("enable_ai", self.enable_ai)
            dataset_name = options.get("dataset_name", f"privacy_{job_id}")
            
            # Update job status
            self._update_job_status(job_id, progress=10.0, message="Applying privacy protection")
            
            # Get privacy processor
            privacy_processor = ProcessorFactory.get_special_processor(
                "privacy",
                use_cognee=use_cognee,
                enable_ai=enable_ai,
                dataset_name=dataset_name,
                redact_pii=redact_pii,
                pii_types=pii_types
            )
            
            # Add privacy info to metadata
            metadata.update({
                "privacy_protected": True,
                "redacted_pii": redact_pii,
                "pii_types": pii_types or []
            })
            
            # Process with privacy protection
            result = await privacy_processor.process(content, metadata=metadata, content_type=content_type)
            
            # Update job status
            self._update_job_status(job_id, progress=70.0, message="Storing privacy-protected content")
            
            # Store in Neo4j and Qdrant (handled by processor)
            document_id = f"privacy_{job_id}"
            
            # Update job status
            self._update_job_status(
                job_id, 
                status="completed", 
                progress=100.0, 
                message="Privacy-protected processing completed",
                result={
                    "document_id": document_id,
                    "chunks_count": len(result.get("chunks", [])),
                    "privacy_protection": {
                        "applied": True,
                        "pii_types": pii_types or []
                    },
                    "metadata": result.get("metadata", {})
                }
            )
            
        except Exception as e:
            logger.error(f"Error processing with privacy: {str(e)}", exc_info=True)
            self._update_job_status(
                job_id,
                status="failed",
                progress=0.0,
                message=f"Privacy-protected processing failed: {str(e)}"
            )
    
    def _update_job_status(
        self,
        job_id: str,
        status: Optional[str] = None,
        progress: Optional[float] = None,
        message: Optional[str] = None,
        result: Optional[Dict[str, Any]] = None
    ) -> None:
        """
        Update the status of an ingestion job.
        
        Args:
            job_id: Job ID
            status: Job status
            progress: Progress percentage
            message: Status message
            result: Job result
        """
        if job_id not in self.job_store:
            return
        
        # Update job status
        if status:
            self.job_store[job_id]["status"] = status
        
        if progress is not None:
            self.job_store[job_id]["progress"] = progress
        
        if message:
            self.job_store[job_id]["message"] = message
        
        if result:
            self.job_store[job_id]["result"] = result
        
        # Update timestamp
        self.job_store[job_id]["updated_at"] = datetime.now().isoformat()
    
    async def get_status(self, job_id: str) -> IngestionStatus:
        """
        Get the status of an ingestion job.
        
        Args:
            job_id: Job ID
            
        Returns:
            Job status
            
        Raises:
            ValueError: If the job is not found
        """
        if job_id not in self.job_store:
            raise ValueError(f"Job not found: {job_id}")
        
        job_data = self.job_store[job_id]
        
        return IngestionStatus(
            job_id=job_id,
            status=job_data["status"],
            progress=job_data.get("progress"),
            message=job_data.get("message"),
            result=job_data.get("result"),
            created_at=job_data["created_at"],
            updated_at=job_data["updated_at"]
        ) 