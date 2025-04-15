import os
import time
import random
import click
import logging
from pathlib import Path

from ai_logger.src.utils.ai_logger import AILogger
cwd = Path.cwd()
log_file = os.path.join(cwd, "ai_logger_example.json")
logger = AILogger(
    app_name="ai_logger_example",
    log_file=log_file,
    console_output=True,
    log_level=logging.INFO
)

# Example standalone function that will be wrapped
@logger.wrap_function(component="example_module")
def process_data(data_size: int = 100) -> dict:
    """Process a simulated dataset and return statistics."""
    logger.log_data_event(
        data_source="example_source",
        event_type="data_processing_started",
        record_count=data_size
    )
    
    # Simulate processing time
    time.sleep(0.5)
    
    # Generate fake results
    result = {
        "processed_items": data_size,
        "success_rate": random.uniform(0.90, 0.99),
        "processing_time_ms": random.randint(100, 500)
    }
    
    logger.log_data_event(
        data_source="example_source",
        event_type="data_processing_completed",
        record_count=data_size,
        details=result
    )
    
    # Random chance to throw an error
    if random.random() < 0.1:
        raise ValueError("Random error in data processing")
        
    return result

# Example class that will be wrapped
@logger.wrap_class(component="calculator")
class Calculator:
    def __init__(self, initial_value: float = 0):
        self.value = initial_value
        
    def add(self, x: float) -> float:
        """Add a number to the current value."""
        self.value += x
        return self.value
        
    def subtract(self, x: float) -> float:
        """Subtract a number from the current value."""
        self.value -= x
        return self.value
        
    def multiply(self, x: float) -> float:
        """Multiply the current value by a number."""
        self.value *= x
        return self.value
        
    def divide(self, x: float) -> float:
        """Divide the current value by a number."""
        if x == 0:
            raise ZeroDivisionError("Cannot divide by zero")
        self.value /= x
        return self.value
        
    def complex_calculation(self, x: float, y: float, operation: str) -> float:
        """Perform a more complex calculation."""
        logger.log_model_event(
            model_name="calculator_model",
            event_type="complex_calculation",
            details={"x": x, "y": y, "operation": operation}
        )
        
        if operation == "power":
            result = self.value ** x
        elif operation == "root":
            result = self.value ** (1/x)
        elif operation == "modulo":
            result = self.value % x
        else:
            raise ValueError(f"Unknown operation: {operation}")
            
        self.value = result
        return result

# Module level functions to be wrapped
def module_example():
    """
    Run through and wrap all functions at module level.
    
    This is useful for libraries or utility modules where you want to 
    automatically wrap all functions without decorating each one.
    """
    # Define a simple module-level function to demonstrate wrapping
    @logger.wrap_function(component="module_level")
    def helper_function(x: int, y: int) -> int:
        """A simple helper function to demonstrate module wrapping."""
        return x + y
        
    # Call the helper function we just defined
    result = helper_function(5, 10)
    
    # Log information about the example
    logger.log_data_event(
        data_source="module_example",
        event_type="module_test_completed",
        details={"wrapped_function_result": result}
    )
    
    return result

# Click CLI commands
@click.group()
def cli():
    """AI Logger example application with Click CLI."""

@cli.command()
@click.option("--size", default=100, help="Size of data to process")
def run_function(size: int):
    """Run the wrapped function example."""
    click.echo(f"Running wrapped function example with data size {size}...")
    try:
        result = process_data(size)
        click.echo(f"Processing completed successfully: {result}")
    except Exception as e:
        click.echo(f"Error during processing: {e}")
    click.echo(f"Check the log file at: {log_file}")

@cli.command()
@click.option("--initial", default=10, help="Initial calculator value")
@click.option("--operations", default=5, help="Number of operations to perform")
def run_class(initial: float, operations: int):
    """Run the wrapped class example."""
    click.echo(f"Running calculator class example with initial value {initial}...")
    
    calc = Calculator(initial)
    
    for i in range(operations):
        try:
            operation = random.choice(["add", "subtract", "multiply", "divide", "complex"])
            if operation == "add":
                value = random.uniform(1, 10)
                result = calc.add(value)
                click.echo(f"Add {value}: {result}")
            elif operation == "subtract":
                value = random.uniform(1, 5)
                result = calc.subtract(value)
                click.echo(f"Subtract {value}: {result}")
            elif operation == "multiply":
                value = random.uniform(1, 3)
                result = calc.multiply(value)
                click.echo(f"Multiply by {value}: {result}")
            elif operation == "divide":
                value = random.uniform(0.5, 5)
                result = calc.divide(value)
                click.echo(f"Divide by {value}: {result}")
            elif operation == "complex":
                x = random.uniform(1, 3)
                y = random.uniform(1, 2)
                op = random.choice(["power", "root", "modulo"])
                result = calc.complex_calculation(x, y, op)
                click.echo(f"Complex {op}({x}, {y}): {result}")
        except Exception as e:
            click.echo(f"Error during operation: {e}")
    
    click.echo(f"Final calculator value: {calc.value}")
    click.echo(f"Check the log file at: {log_file}")

@cli.command()
def run_module():
    """Run the module wrapping example."""
    click.echo("Running module wrapping example...")
    
    result = module_example()
    click.echo(f"Module example completed with result: {result}")
    click.echo(f"Check the log file at: {log_file}")

@cli.command()
def run_all():
    """Run all examples in sequence."""
    click.echo("Running all examples...")
    
    click.echo("\n--- Function Example ---")
    run_function.callback(size=150)
    
    click.echo("\n--- Class Example ---")
    run_class.callback(initial=5, operations=7)
    
    click.echo("\n--- Module Example ---")
    run_module.callback()
    
    click.echo("\nAll examples completed!")

if __name__ == "__main__":
    cli()