from __future__ import annotations
import os
from pathlib import Path
from typing import Dict
from pydantic import ValidationError
import json
import sys
import logging
from .models import AppConfig

def load_config(config_path: str = None) -> AppConfig:
    """
    Load and validate configuration from config file.
    
    Args:
        config_path: Optional path to a custom config file. If None, the default config is used.
    
    Returns:
        AppConfig: Loaded and validated configuration
    """
    # Avoid circular import
    from ai_logger.src.user_interface.uiux import ui
    
    # Check environment variable for config path
    env_config_path = os.environ.get('AI_LOGGER_CONFIG')
    
    # Priority: 1. Function argument, 2. Environment variable, 3. Default location
    if config_path:
        config_path = Path(config_path)
    elif env_config_path:
        config_path = Path(env_config_path)
    else:
        # Default config file location
        config_path = Path(__file__).parent / "ai_logger.json"

    try:
        # If config doesn't exist at specified path, try to use default
        if not config_path.exists():
            default_path = Path(__file__).parent / "ai_logger.json"
            if default_path.exists() and config_path != default_path:
                print(f"Warning: Config file not found at {config_path}, using default config")
                config_path = default_path
            else:
                ui.print(f"Config file not found at path: {config_path}", style="danger")
                # Instead of exiting, return default configuration
                return AppConfig()
        
        with open(config_path) as f:
            config_data = json.load(f)
            
        # Validate configuration
        return AppConfig(**config_data)
    except json.JSONDecodeError as e:
        ui.print(f"Invalid JSON in config file: {e}", style="danger")
        # Return default config instead of exiting
        return AppConfig()
    except ValidationError as e:
        ui.print(f"Invalid configuration: {e}", style="danger")
        return AppConfig()
    except Exception as e:
        ui.print(f"Error loading configuration: {e}", style="danger")
        return AppConfig()

# Load the configuration initially with default settings
CONFIG = load_config()

# Export common configuration values for backward compatibility
VERBOSE = CONFIG.verbose
USE_DB = CONFIG.database.use_db

def reload_config(config_path: str = None) -> AppConfig:
    """
    Reload the configuration from the specified path and update global CONFIG
    
    Args:
        config_path: Path to the configuration file
        
    Returns:
        The loaded AppConfig
    """
    global CONFIG, VERBOSE, USE_DB
    
    # Reload the configuration
    CONFIG = load_config(config_path)
    
    # Update the exported values
    VERBOSE = CONFIG.verbose
    USE_DB = CONFIG.database.use_db
    
    return CONFIG

def get_db_config() -> Dict:
    """Get database configuration as a dictionary."""
    return CONFIG.database.model_dump()

def get_log_level() -> int:
    """Get log level as a logging constant."""
    level_map = {
        "DEBUG": logging.DEBUG,
        "INFO": logging.INFO,
        "WARNING": logging.WARNING,
        "ERROR": logging.ERROR,
        "CRITICAL": logging.CRITICAL
    }
    return level_map.get(CONFIG.logging.level.upper(), logging.INFO)

def load_env_from_json(file_path):
    """Load environment variables from a JSON file."""
    from ..user_interface.uiux import ui
    try:
        with open(file_path, "r") as f:
            env_config = json.load(f)
            
        # Set environment variables from the config
        for key, value in env_config.items():
            if value:
                os.environ[key] = value
        
        return env_config
    except (FileNotFoundError, json.JSONDecodeError) as e:
        ui.print(f"Error loading config file: {e}", style="danger")
        return None