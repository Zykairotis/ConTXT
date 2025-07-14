"""
Base processor class for data processing.
"""
from abc import ABC, abstractmethod
from enum import Enum
from typing import Any, Dict, Optional, Union

from pydantic import BaseModel, Field


class ProcessingStatus(str, Enum):
    """Status of a processing job."""
    PENDING = "pending"
    PROCESSING = "processing"
    COMPLETED = "completed"
    FAILED = "failed"


class ProcessingResult(BaseModel):
    """Result of a processing operation."""
    job_id: str
    status: ProcessingStatus = ProcessingStatus.COMPLETED
    data: Optional[Dict[str, Any]] = None
    error: Optional[str] = None


class BaseProcessor(ABC):
    """Base class for all data processors."""
    
    @abstractmethod
    async def process(self, data: Any, **kwargs) -> ProcessingResult:
        """
        Process the input data.
        
        Args:
            data: The input data to process.
            **kwargs: Additional processing parameters.
            
        Returns:
            ProcessingResult: The result of the processing operation.
        """
        pass
    
    @abstractmethod
    async def get_status(self, job_id: str) -> Dict[str, Any]:
        """
        Get the status of a processing job.
        
        Args:
            job_id: The ID of the processing job.
            
        Returns:
            Dict[str, Any]: The status information.
        """
        pass 