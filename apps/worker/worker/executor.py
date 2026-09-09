"""
Job Executor for running background jobs.

Provides async execution of jobs with:
- Concurrency control
- Status tracking
- Error handling
- Graceful shutdown support
"""

import asyncio
import logging
from dataclasses import dataclass, field
from datetime import datetime, timezone
from enum import Enum
from typing import Any

from worker.job_base import JobBase, JobContext, JobResult, JobStatus
from worker.registry import registry


class ExecutorState(str, Enum):
    """Executor state values."""

    IDLE = "idle"
    RUNNING = "running"
    SHUTTING_DOWN = "shutting_down"
    STOPPED = "stopped"


@dataclass
class ExecutionRecord:
    """Record of a job execution."""

    job_id: str
    job_type: str
    status: JobStatus
    started_at: datetime
    completed_at: datetime | None = None
    result: JobResult[Any] | None = None
    error: str | None = None


class JobExecutor:
    """
    Async job executor with concurrency control.
    
    Manages a pool of workers that execute jobs concurrently.
    Supports graceful shutdown and execution tracking.
    """

    def __init__(
        self,
        max_concurrency: int = 2,
        max_retries: int = 3,
    ):
        """
        Initialize the executor.
        
        Args:
            max_concurrency: Maximum number of concurrent jobs
            max_retries: Default maximum retries for all jobs
        """
        self.max_concurrency = max_concurrency
        self.max_retries = max_retries
        
        # State management
        self._state = ExecutorState.IDLE
        self._semaphore = asyncio.Semaphore(max_concurrency)
        
        # Tracking
        self._active_jobs: dict[str, asyncio.Task[JobResult[Any]]] = {}
        self._execution_history: list[ExecutionRecord] = []
        
        # Shutdown event
        self._shutdown_event = asyncio.Event()

    @property
    def state(self) -> ExecutorState:
        """Current executor state."""
        return self._state

    @property
    def active_count(self) -> int:
        """Number of currently active jobs."""
        return len(self._active_jobs)

    @property
    def is_running(self) -> bool:
        """Whether executor is accepting new jobs."""
        return self._state == ExecutorState.RUNNING

    async def start(self) -> None:
        """Start the executor."""
        if self._state == ExecutorState.RUNNING:
            return
        
        self._state = ExecutorState.RUNNING
        self._shutdown_event.clear()
        logger.info(
            "executor_started",
            max_concurrency=self.max_concurrency,
        )

    async def stop(self, wait_for_completion: bool = True) -> None:
        """
        Stop the executor.
        
        Args:
            wait_for_completion: If True, wait for active jobs to complete
        """
        if self._state == ExecutorState.STOPPED:
            return
        
        self._state = ExecutorState.SHUTTING_DOWN
        logger.info("executor_stopping", wait=wait_for_completion)
        
        if wait_for_completion and self._active_jobs:
            # Wait for active jobs to complete
            await asyncio.gather(*self._active_jobs.values(), return_exceptions=True)
        
        self._state = ExecutorState.STOPPED
        self._shutdown_event.set()
        logger.info("executor_stopped")

    async def submit(
        self,
        job_type: str,
        payload: dict[str, Any] | None = None,
        **kwargs,
    ) -> str:
        """
        Submit a job for execution.
        
        Args:
            job_type: Type of job to execute
            payload: Optional input data for the job
            **kwargs: Additional arguments passed to job constructor
            
        Returns:
            Job ID of the submitted job
            
        Raises:
            RuntimeError: If executor is not running
            KeyError: If job type is not registered
        """
        if not self.is_running:
            raise RuntimeError(f"Executor is not running (state: {self._state})")
        
        # Create job instance
        job = registry.create_instance(job_type, payload=payload, **kwargs)
        
        # Create and store task
        task = asyncio.create_task(self._execute_job(job))
        self._active_jobs[job.job_id] = task
        
        logger.info(
            "job_submitted",
            job_id=job.job_id,
            job_type=job_type,
        )
        
        return job.job_id

    async def _execute_job(self, job: JobBase) -> JobResult[Any]:
        """Execute a job with semaphore-based concurrency control."""
        record = ExecutionRecord(
            job_id=job.job_id,
            job_type=job.job_type,
            status=JobStatus.RUNNING,
            started_at=datetime.now(timezone.utc),
        )
        
        try:
            async with self._semaphore:
                result = await job.run()
                record.status = job.status
                record.result = result
                record.completed_at = datetime.now(timezone.utc)
                
                logger.info(
                    "job_completed",
                    job_id=job.job_id,
                    success=result.success,
                    duration_ms=result.duration_ms,
                )
                
                return result
                
        except Exception as e:
            record.status = JobStatus.FAILED
            record.error = str(e)
            record.completed_at = datetime.now(timezone.utc)
            
            logger.exception(
                "job_failed",
                job_id=job.job_id,
                error=str(e),
            )
            
            raise
            
        finally:
            # Cleanup
            self._active_jobs.pop(job.job_id, None)
            self._execution_history.append(record)

    async def get_job_status(self, job_id: str) -> dict[str, Any] | None:
        """Get status of a specific job."""
        if job_id in self._active_jobs:
            task = self._active_jobs[job_id]
            return {
                "job_id": job_id,
                "status": "running",
                "done": task.done(),
            }
        
        # Check history
        for record in reversed(self._execution_history):
            if record.job_id == job_id:
                return {
                    "job_id": job_id,
                    "status": record.status.value,
                    "completed_at": record.completed_at.isoformat() if record.completed_at else None,
                    "error": record.error,
                }
        
        return None

    def get_recent_executions(self, limit: int = 50) -> list[dict[str, Any]]:
        """Get recent execution records."""
        records = self._execution_history[-limit:]
        return [
            {
                "job_id": r.job_id,
                "job_type": r.job_type,
                "status": r.status.value,
                "started_at": r.started_at.isoformat(),
                "completed_at": r.completed_at.isoformat() if r.completed_at else None,
                "error": r.error,
            }
            for r in records
        ]


# Module-level logger
logger = logging.getLogger(__name__)
