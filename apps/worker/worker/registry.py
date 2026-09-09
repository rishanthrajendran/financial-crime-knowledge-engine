"""
Job Registry for managing available job types.

Provides a centralized registry for all job types, allowing
dynamic registration and lookup of job classes.
"""

import logging

from worker.job_base import JOB_TYPES, JobBase

logger = logging.getLogger(__name__)


class JobRegistry:
    """
    Registry for job types.
    
    Allows registering new job types and retrieving them by name.
    Pre-populated with built-in job types.
    """

    def __init__(self):
        """Initialize registry with built-in job types."""
        self._jobs: dict[str, type[JobBase]] = {}
        
        # Register built-in job types
        for job_type, job_class in JOB_TYPES.items():
            self.register(job_type, job_class)

    def register(self, job_type: str, job_class: type[JobBase]) -> None:
        """
        Register a job type.
        
        Args:
            job_type: Unique identifier for the job type
            job_class: Job class to register
            
        Raises:
            ValueError: If job_type is already registered
        """
        if job_type in self._jobs:
            logger.warning(
                "overwriting_job_type",
                job_type=job_type,
                existing=str(self._jobs[job_type]),
            )
        
        self._jobs[job_type] = job_class
        logger.debug("registered_job", job_type=job_type, job_class=str(job_class))

    def get(self, job_type: str) -> type[JobBase]:
        """
        Get a job class by type.
        
        Args:
            job_type: Job type identifier
            
        Returns:
            Job class for the given type
            
        Raises:
            KeyError: If job type is not registered
        """
        if job_type not in self._jobs:
            raise KeyError(f"Unknown job type: {job_type}. Available: {list(self._jobs.keys())}")
        
        return self._jobs[job_type]

    def create_instance(self, job_type: str, **kwargs) -> JobBase:
        """
        Create a new job instance of the specified type.
        
        Args:
            job_type: Job type identifier
            **kwargs: Arguments passed to job constructor
            
        Returns:
            New job instance
        """
        job_class = self.get(job_type)
        return job_class(**kwargs)

    def list_types(self) -> list[str]:
        """List all registered job types."""
        return list(self._jobs.keys())

    def is_registered(self, job_type: str) -> bool:
        """Check if a job type is registered."""
        return job_type in self._jobs

    @property
    def count(self) -> int:
        """Number of registered job types."""
        return len(self._jobs)


# Global singleton instance
registry = JobRegistry()
