from __future__ import annotations
import os
from pathlib import Path
from typing import Dict, Union
from pydantic import ValidationError
import json
import sys
import logging
from .models import AppConfig


def load_config() -> AppConfig:
    """Load and validate configuration from config file."""
    # agentic_flow_config.json
    # Avoid circular import
    from uiux import ui
    
    config_path = Path(__file__).parent / "ai_logger.json"

    if not config_path.exists():
        ui.print(f"Config file not found at path: {config_path}", style="danger")
        sys.exit(1)
        
    try:
        with open(config_path) as f:
            config_data = json.load(f)
            
        # Validate configuration
        return AppConfig(**config_data)
    except json.JSONDecodeError as e:
        ui.print(f"Invalid JSON in config file: {e}", style="danger")
        sys.exit(1)
    except ValidationError as e:
        ui.print(f"Invalid configuration: {e}", style="danger")
        sys.exit(1)
    except Exception as e:
        ui.print(f"Error loading configuration: {e}", style="danger")
        sys.exit(1)

# Load the configuration
CONFIG = load_config()

# Export common configuration values for backward compatibility
VERBOSE = CONFIG.verbose
USE_DB = CONFIG.use_db
USE_BOTH = CONFIG.use_index_file_with_db

# Helper functions to access configuration
def get_db_config() -> Dict[str, str]:
    """Get database configuration as a dictionary."""
    return CONFIG.database.model_dump()

def get_model_config() -> Dict[str, Union[str, float]]:
    """Get model configuration as a dictionary."""
    return CONFIG.model.model_dump()

def get_paths_config() -> Dict[str, str]:
    """Get paths configuration as a dictionary."""
    return CONFIG.paths.model_dump()

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

def get_spinner_type() -> str:
    """Get the configured spinner type."""
    return CONFIG.ui.spinner_type

def load_env_from_json(file_path):
    from .uiux import ui
    try:
        with open(file_path, "r") as f:
            env_config = json.load(f)
            
        # Set environment variables from the config
        for server_name, server_config in env_config.get("mcpServers", {}).items():
            if "env" in server_config:
                for key, value in server_config["env"].items():
                    # Only set if the value is not empty
                    if value:
                        os.environ[key] = value
                    # If the value is empty but an environment variable exists, use that
                    elif key in os.environ and os.environ[key]:
                        server_config["env"][key] = os.environ[key]
                    # Otherwise try to load from .env file (which load_dotenv should have done)
                    elif os.getenv(key):
                        server_config["env"][key] = os.getenv(key)
        
        return env_config
    except (FileNotFoundError, json.JSONDecodeError) as e:
        ui.print(f"Error loading config file: {e}", style="danger")
        return None
    
def process_config(config_dict):
    """Process config dictionary to replace placeholder values in args with env values"""
    processed_config = {"mcpServers": {}}
    
    for server_name, server_config in config_dict.get("mcpServers", {}).items():
        # Copy server config to avoid modifying the original
        processed_server = server_config.copy()
        
        # If env variables exist
        if "env" in processed_server:
            # Process args if they exist
            if "args" in processed_server:
                processed_args = []
                for arg in processed_server["args"]:
                    # Check if arg is a string and matches an env key
                    if isinstance(arg, str) and arg in processed_server["env"]:
                        # Replace arg with its corresponding env value
                        processed_args.append(processed_server["env"][arg])
                    else:
                        processed_args.append(arg)
                processed_server["args"] = processed_args
        
        processed_config["mcpServers"][server_name] = processed_server
    
    return processed_config