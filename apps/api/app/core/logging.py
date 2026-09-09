"""
Structured logging configuration using structlog.

Provides consistent, structured logging across the application
with JSON output in production and human-readable output in development.
"""

import logging
import sys
from typing import TYPE_CHECKING, cast

import structlog
from structlog.types import Processor

if TYPE_CHECKING:
    from structlog.stdlib import BoundLogger


def setup_logging(
    log_level: str = "INFO",
    json_logs: bool = False,
) -> None:
    """
    Configure structured logging for the application.

    Args:
        log_level: Logging level (DEBUG, INFO, WARNING, ERROR)
        json_logs: If True, output JSON-formatted logs (for production)
    """
    # Configure standard library logging
    logging.basicConfig(
        format="%(message)s",
        stream=sys.stdout,
        level=getattr(logging, log_level.upper(), logging.INFO),
    )

    # Build processors list
    processors: list[Processor] = [
        # Add context variables from structlog.contextvars
        structlog.contextvars.merge_contextvars,
        # Add log level
        structlog.stdlib.add_log_level,
        # Add logger name
        structlog.stdlib.add_logger_name,
        # Evaluate timestamp
        structlog.processors.TimeStamper(fmt="iso"),
    ]

    if json_logs:
        # Production: JSON output
        processors.extend([
            structlog.processors.format_exc_info,
            structlog.processors.JSONRenderer(),
        ])
    else:
        # Development: Human-readable console output
        processors.extend([
            # Colorize output if terminal supports it
            structlog.dev.ConsoleRenderer(colors=True),
        ])

    # Configure structlog
    structlog.configure(
        processors=processors,
        wrapper_class=structlog.stdlib.BoundLogger,
        context_class=dict,
        logger_factory=structlog.stdlib.LoggerFactory(),
        cache_logger_on_first_use=True,
    )


def get_logger(name: str | None = None) -> "BoundLogger":
    """Get a structured logger instance."""
    return cast("BoundLogger", structlog.get_logger(name))
