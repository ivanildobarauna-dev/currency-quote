# Currency Quote Project Guide

## Commands
- Run tests: `poetry run pytest`
- Run specific test: `poetry run pytest src/tests/test_file.py::test_function`
- Coverage: `poetry run coverage run -m pytest` and `poetry run coverage report`
- Format code: `poetry run black .` 
- Lint: `poetry run pylint src`
- Build: `poetry build`
- Install: `poetry install`

## Code Style
- Follow PEP 8 with Black formatting
- Python 3.9+ required
- Hexagonal Architecture pattern (ports & adapters)
- Function names: snake_case
- Class names: PascalCase
- Error handling: Use exceptions appropriately, validate inputs
- Imports: Organize by standard library, third-party, local with line breaks
- Type hints required for function parameters and return values
- Use docstrings for public-facing functions/methods (pylint C0116 disabled)
- Always write tests for new functionality