"""
Abstract job base class for background job processing.

All worker jobs must inherit from JobBase and implement
the execute() method. The framework handles:
- Job identification and idempotency
- Status tracking and persistence
- Retry logic with configurable policies
- Error handling and logging
"""

import abc
import time
import uuid
from datetime import datetime, timezone
from enum import Enum
from typing import Any, Generic, TypeVar

from pydantic import BaseModel, Field


class JobStatus(str, Enum):
    """Job execution status values."""

    PENDING = "pending"
    RUNNING = "running"
    COMPLETED = "completed"
    FAILED = "failed"
    RETRYING = "retrying"
    CANCELLED = "cancelled"


class JobPriority(str, Enum):
    """Job priority levels."""

    LOW = "low"
    NORMAL = "normal"
    HIGH = "high"
    CRITICAL = "critical"


# Type variable for job result type
T = TypeVar("T")


class JobResult(BaseModel, Generic[T]):
    """Result of a job execution."""

    success: bool = Field(description="Whether the job succeeded")
    data: T | None = Field(default=None, description="Job result data")
    error: str | None = Field(default=None, description="Error message if failed")
    duration_ms: float = Field(description="Execution duration in milliseconds")


class JobContext(BaseModel):
    """Context information passed to jobs during execution."""

    job_id: str = Field(description="Unique job identifier")
    attempt: int = Field(default=1, description="Current attempt number (1-indexed)")
    max_attempts: int = Field(default=3, description="Maximum retry attempts")
    trace_id: str | None = Field(default=None, description="Distributed tracing ID")


class JobBase(abc.ABC, Generic[T]):
    """
    Abstract base class for all background jobs.
    
    To create a new job:
        1. Subclass JobBase
        2. Set job_type class attribute
        3. Implement execute() method
        4. Register in JobRegistry
    
    Example:
        class MyJob(JobBase[dict]):
            job_type = "my_job_type"
            
            async def execute(self, context: JobContext) -> JobResult[dict]:
                # Do work here
                return JobResult(success=True, data={"result": "value"})
    """

    # Class attributes - must be set by subclasses
    job_type: str = ""
    """Unique identifier for this job type."""
    
    default_priority: JobPriority = JobPriority.NORMAL
    """Default priority for this job type."""
    
    default_max_retries: int = 3
    """Default maximum retry attempts."""
    
    default_retry_delay_seconds: float = 60.0
    """Default delay between retries in seconds."""

    def __init__(
        self,
        job_id: str | None = None,
        idempotency_key: str | None = None,
        priority: JobPriority | None = None,
        max_retries: int | None = None,
        payload: dict[str, Any] | None = None,
    ):
        """
        Initialize a new job instance.
        
        Args:
            job_id: Unique job identifier (auto-generated if not provided)
            idempotency_key: Key for idempotent operations
            priority: Job priority override
            max_retries: Maximum retry attempts override
            payload: Input data for the job
        """
        self.job_id = job_id or str(uuid.uuid4())
        self.idempotency_key = idempotency_key
        self.priority = priority or self.default_priority
        self.max_retries = max_retries if max_retries is not None else self.default_max_retries
        self.payload = payload or {}
        
        # Runtime state
        self.status = JobStatus.PENDING
        self.created_at = datetime.now(timezone.utc)
        self.started_at: datetime | None = None
        self.completed_at: datetime | None = None
        self.attempt_count = 0
        self.last_error: str | None = None

    @abc.abstractmethod
    async def execute(self, context: JobContext) -> JobResult[T]:
        """
        Execute the job logic.
        
        This method must be implemented by all subclasses.
        
        Args:
            context: Execution context with job metadata
        
        Returns:
            JobResult containing success status and optional result data
        """
        raise NotImplementedError("Subclasses must implement execute()")

    async def run(self) -> JobResult[T]:
        """
        Run the job with built-in retry logic.
        
        Handles status tracking, timing, retries, and error handling.
        """
        self.status = JobStatus.RUNNING
        self.started_at = datetime.now(timezone.utc)
        start_time = time.monotonic()
        
        context = JobContext(
            job_id=self.job_id,
            attempt=0,
            max_attempts=self.max_retries,
        )

        last_result: JobResult[T] | None = None

        for attempt in range(1, self.max_retries + 1):
            self.attempt_count = attempt
            context.attempt = attempt
            
            try:
                if attempt > 1:
                    self.status = JobStatus.RETRYING
                    # Exponential backoff
                    delay = self.default_retry_delay_seconds * (2 ** (attempt - 2))
                    await asyncio_sleep(delay)
                
                result = await self.execute(context)
                result.duration_ms = (time.monotonic() - start_time) * 1000
                
                if result.success:
                    self.status = JobStatus.COMPLETED
                    self.completed_at = datetime.now(timezone.utc)
                    return result
                else:
                    last_result = result
                    self.last_error = result.error or "Job returned unsuccessful"
                    
            except Exception as e:
                last_result = JobResult(
                    success=False,
                    error=str(e),
                    duration_ms=(time.monotonic() - start_time) * 1000,
                )
                self.last_error = str(e)

        # All retries exhausted
        self.status = JobStatus.FAILED
        self.completed_at = datetime.now(timezone.utc)
        
        return last_result or JobResult(
            success=False,
            error="Max retries exceeded",
            duration_ms=(time.monotonic() - start_time) * 1000,
        )

    def to_dict(self) -> dict[str, Any]:
        """Serialize job state to dictionary."""
        return {
            "job_id": self.job_id,
            "job_type": self.job_type,
            "idempotency_key": self.idempotency_key,
            "status": self.status.value,
            "priority": self.priority.value,
            "attempt_count": self.attempt_count,
            "max_retries": self.max_retries,
            "created_at": self.created_at.isoformat(),
            "started_at": self.started_at.isoformat() if self.started_at else None,
            "completed_at": self.completed_at.isoformat() if self.completed_at else None,
            "last_error": self.last_error,
            "payload": self.payload,
        }


# Helper function to avoid circular import issues
async def asyncio_sleep(seconds: float) -> None:
    """Async sleep helper."""
    import asyncio
    await asyncio.sleep(seconds)


# =============================================================================
# Predefined Job Types (for Phase 1+ implementation)
# =============================================================================

class KnowledgeIngestionJob(JobBase[dict]):
    """
    Job for ingesting knowledge from external sources.
    
    Phase 1+: Will ingest documents from the Knowledge Base repository.
    """
    
    job_type = "knowledge_ingestion"
    default_max_retries = 5
    default_retry_delay_seconds = 120.0  # Longer delay for I/O heavy tasks

    async def execute(self, context: JobContext) -> JobResult[dict]:
        # TODO: Implement knowledge ingestion logic in Phase 1
        raise NotImplementedError("Knowledge ingestion will be implemented in Phase 1")


class EmbeddingGenerationJob(JobBase[dict]):
    """
    Job for generating vector embeddings for knowledge documents.
    
    Phase 2+: Will generate embeddings using AI services.
    """
    
    job_type = "embedding_generation"
    default_max_retries = 3
    default_retry_delay_seconds = 30.0

    async def execute(self, context: JobContext) -> JobResult[dict]:
        # TODO: Implement embedding generation in Phase 2
        raise NotImplementedError("Embedding generation will be implemented in Phase 2")


class IndexingJob(JobBase[dict]):
    """
    Job for updating search indexes.
    
    Phase 2+: Will update vector and graph indexes.
    """
    
    job_type = "indexing"
    default_max_retries = 3
    default_retry_delay_seconds = 30.0

    async def execute(self, context: JobContext) -> JobResult[dict]:
        # TODO: Implement indexing logic in Phase 2
        raise NotImplementedError("Indexing will be implemented in Phase 2")


class AssessmentProcessingJob(JobBase[dict]):
    """
    Job for processing risk assessments.
    
    Phase 3+: Will process assessment workflows.
    """
    
    job_type = "assessment_processing"
    default_max_retries = 3
    default_retry_delay_seconds = 60.0

    async def execute(self, context: JobContext) -> JobResult[dict]:
        # TODO: Implement assessment processing in Phase 3
        raise NotImplementedError("Assessment processing will be implemented in Phase 3")


# Export all job types for registry
JOB_TYPES = {
    "knowledge_ingestion": KnowledgeIngestionJob,
    "embedding_generation": EmbeddingGenerationJob,
    "indexing": IndexingJob,
    "assessment_processing": AssessmentProcessingJob,
}
