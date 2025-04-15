# AI Logger

A Python module for structured logging in a format that's easily parsable by AI systems. It provides comprehensive, context-rich logs to help AI systems understand application behavior.

## Features

- JSON-formatted logs optimized for AI consumption
- Automatic capturing of context (filename, line number, function)
- Decorators for easy function and class wrapping
- Support for different event types (model, data, error)
- Simple integration with existing Python logging

## Installation

```bash
# Install from PyPI
pip install ai-logger

# Or install from source using Poetry
poetry install
```

## Example Usage

The package includes a complete example with Click CLI commands to demonstrate the AI Logger functionality:

```bash
# Run all examples
poetry run run-example run-all

# Run just the function example
poetry run run-example run-function --size 200

# Run just the class example
poetry run run-example run-class --initial 10 --operations 8

# Run just the module example
poetry run run-example run-module
```

## Configuration

AI Logger can be configured through several methods:

### Using a Configuration File

Create a JSON configuration file like:

```json
{
  "verbose": true,
  "database": {
    "use_db": true,
    "dbname": "my_logger_db",
    "user": "postgres",
    "password": "secretpassword",
    "host": "localhost",
    "port": "5432",
    "table_name": "ai_logs"
  },
  "logging": {
    "level": "INFO",
    "log_to_file": true,
    "log_dir": "logs",
    "log_to_console": true
  }
}
```

You can specify your custom configuration file in several ways:

1. **Environment variable**:
   ```bash
   export AI_LOGGER_CONFIG=/path/to/your/config.json
   ```

2. **Programmatic loading**:
   ```python
   from ai_logger import reload_config
   reload_config("/path/to/your/config.json")
   ```

3. **When initializing**:
   ```python
   from ai_logger import init_ai_logger
   init_ai_logger(app_name="my_app", config_path="/path/to/your/config.json")
   ```

## Basic Code Usage

### Direct Import and Usage

```python
# Import directly from the package
import logging
from ai_logger import init_ai_logger, auto_wrap, auto_wrap_class

# Initialize the global logger
logger = init_ai_logger(
    app_name="my_app",
    log_file="ai_logs.json",
    console_output=True,
    log_level=logging.INFO,  # Optional, defaults to WARNING
    capture_loggers=["sqlalchemy", "uvicorn", "custom_logger_name"],  # Optional, capture other loggers
    capture_all_loggers=False,  # Optional, capture all Python loggers
    use_db=True,  # Optional, enable database logging
    db_name="my_logger_db",  # Optional, custom database name
    db_table="my_app_logs"  # Optional, custom table name (defaults to app_name)
)

# Log a model event
logger.log_model_event(
    model_name="gpt-4",
    event_type="inference",
    input_tokens=150,
    output_tokens=30,
    latency_ms=500
)

# Use the auto_wrap decorator for functions
@auto_wrap(component="data_processor")
def process_data(data):
    # Function code here
    return result

# Use the auto_wrap_class decorator for classes
@auto_wrap_class(component="ml_model")
class MyModel:
    def predict(self, inputs):
        # All methods are automatically wrapped
        return prediction
    
    def train(self, dataset):
        # Training is also logged
        return training_results
```

### Advanced Usage with Manual Logger

```python
from ai_logger import AILogger

# Create a logger instance manually
custom_logger = AILogger(
    app_name="custom_app",
    log_file="custom_logs.json",
    console_output=True,
    use_db=True,
    db_name="custom_logger_db",
    db_table="custom_logs"
)

# Log a data event
custom_logger.log_data_event(
    data_source="database",
    event_type="query",
    record_count=1250,
    details={"query_time_ms": 45, "table": "users"}
)

# Log an error event
try:
    # Some code that might fail
    result = 1 / 0
except Exception as e:
    custom_logger.log_error(
        error_type="ZeroDivisionError",
        error_message=str(e),
        component="math_operations",
        include_traceback=True,
        severity="ERROR"
    )

# Wrap a function with this specific logger
@custom_logger.wrap_function(component="data_processor")
def process_data(data):
    # Function code here
    return result

# Wrap an entire class with this specific logger
@custom_logger.wrap_class(component="ml_model")
class MyModel:
    def predict(self, inputs):
        # Method code here
        return prediction
```

## Log Structure

Events are stored as JSON objects with the following structure:

```json
{
  "event_id": "unique-uuid",
  "timestamp": "2023-07-20T14:30:00.123456",
  "event_type": "inference",
  "component": "model",
  "file_name": "/path/to/file.py",
  "line_number": 42,
  "function_name": "predict",
  "model_name": "gpt-4",
  "input_tokens": 150,
  "output_tokens": 30,
  "latency_ms": 500,
  "details": {
    "app_name": "my_app",
    "custom_field": "custom_value"
  }
}
```

## License

MIT
