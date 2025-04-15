# CLAUDE.md

This file provides guidance to Claude Code (claude.ai/code) when working with code in this repository.

## Build Commands
- Install: `poetry install`
- Run example: `poetry run run-example`
- Lint: `ruff check src/`
- Type check: `mypy src/`

## Code Style Guidelines
- Imports: Standard library first, third-party next, local modules last; alphabetized
- Types: Use type hints from typing module for all function parameters and return types
- Error handling: Use specific exception types with informative messages; log errors
- Naming: snake_case for variables/functions, PascalCase for classes, UPPERCASE for constants
- Classes: Use Pydantic models for data validation; inherit from BaseModel
- Formatting: Max line length 100 chars; docstrings with parameter descriptions
- Logging: Use AILogger for structured logging; wrap functions with decorator pattern

## Project Structure
- src/ layout with utils/ for core functionality
- Python 3.11+ required
- Rich for UI, Pydantic for data models