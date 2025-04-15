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
# Install using Poetry
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

## Basic Code Usage

```python
from ai_logger.src.utils.ai_logger import AILogger

# Initialize logger
logger = AILogger(
    app_name="my_app",
    log_file="ai_logs.json",
    console_output=True
)

# Log a model event
logger.log_model_event(
    model_name="gpt-4",
    event_type="inference",
    input_tokens=150,
    output_tokens=30,
    latency_ms=500
)

# Wrap a function with logging
@logger.wrap_function(component="data_processor")
def process_data(data):
    # Function code here
    return result

# Wrap an entire class
@logger.wrap_class(component="ml_model")
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
