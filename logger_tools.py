import sys
from typing import List, Optional
import logging
from .ai_logger import AILogger


_GLOBAL_LOGGER = None

def init_ai_logger(app_name: str, 
                log_file: Optional[str] = None,
                console_output: bool = True,
                log_level: int = logging.WARNING,
                excluded_patterns: Optional[List[str]] = None,
                capture_loggers: Optional[List[str]] = None,
                capture_all_loggers: bool = False) -> AILogger:
    """
    Initialize the global AI logger
    
    Args:
        app_name: Name of your application
        log_file: Path to log file (optional)
        console_output: Whether to output to console
        log_level: Logging level (default: WARNING)
        excluded_patterns: List of regex patterns for functions/classes to exclude
        capture_loggers: List of logger names to capture (e.g., ['sqlalchemy', 'uvicorn'])
        capture_all_loggers: If True, capture all loggers (use with caution!)
        
    Returns:
        AILogger instance
    """
    global _GLOBAL_LOGGER
    _GLOBAL_LOGGER = AILogger(
        app_name=app_name,
        log_file=log_file,
        console_output=console_output,
        log_level=log_level,
        excluded_patterns=excluded_patterns
    )
    
    # Set up global exception handler
    def global_exception_handler(exc_type, exc_value, exc_traceback):
        if _GLOBAL_LOGGER:
            _GLOBAL_LOGGER.log_error(
                error_type=exc_type.__name__,
                error_message=str(exc_value),
                component="global",
                include_traceback=True,
                severity="CRITICAL"
            )
        # Call the default exception handler
        sys.__excepthook__(exc_type, exc_value, exc_traceback)

    sys.excepthook = global_exception_handler
    
    # Capture existing loggers if specified
    if capture_loggers or capture_all_loggers:
        _GLOBAL_LOGGER.capture_existing_loggers(
            logger_names=capture_loggers,
            capture_all=capture_all_loggers
        )
    
    return _GLOBAL_LOGGER

def get_logger() -> AILogger:
    """Get the global AI logger"""
    if _GLOBAL_LOGGER is None:
        raise RuntimeError("Logger not initialized. Call init_ai_logger first.")
    return _GLOBAL_LOGGER

# Auto-wrap decorator
def auto_wrap(func=None, component=None):
    """
    Decorator to automatically wrap functions with the global logger
    
    Usage:
        @auto_wrap
        def my_function():
            pass
            
        @auto_wrap(component="custom_component")
        def another_function():
            pass
    """
    def decorator(f):
        if _GLOBAL_LOGGER is None:
            return f
        return _GLOBAL_LOGGER.wrap_function(component)(f)
        
    if func is None:
        return decorator
    return decorator(func)

# Auto-wrap class decorator
def auto_wrap_class(cls=None, component=None):
    """
    Decorator to automatically wrap classes with the global logger
    
    Usage:
        @auto_wrap_class
        class MyClass:
            pass
            
        @auto_wrap_class(component="custom_component")
        class AnotherClass:
            pass
    """
    def decorator(c):
        if _GLOBAL_LOGGER is None:
            return c
        return _GLOBAL_LOGGER.wrap_class(component)(c)
        
    if cls is None:
        return decorator
    return decorator(cls)