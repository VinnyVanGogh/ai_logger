"""
AI Logger - A module for AI-friendly JSON logging.

This package provides structured logging in a format that's
easily parsable by AI systems, with rich context.
"""

# Re-export key functionality for direct imports
from ai_logger.src import init_ai_logger, AILogger, auto_wrap, auto_wrap_class

# Export all important symbols for direct import from ai_logger
__all__ = [
    'init_ai_logger',
    'AILogger',
    'auto_wrap',
    'auto_wrap_class',
]