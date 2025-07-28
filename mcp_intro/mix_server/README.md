# Mix Server

A Python package that provides tools for working with CSV, Parquet files, and GitHub EPIC updates. This package includes utilities for data processing, file operations, and GitHub issue management.

## Features

- **CSV Tools**: Read, write, and manipulate CSV files
- **Parquet Tools**: Handle Parquet file operations with pandas and pyarrow
- **GitHub EPIC Tools**: Crawl and analyze GitHub EPIC updates from issues
- **MCP Integration**: Model Context Protocol (MCP) server implementation

## Installation

### Prerequisites

- Python 3.12 or higher
- pip (Python package installer)

### Basic Installation

```bash
# Clone the repository
git clone <repository-url>
cd mcp_research/mcp_intro/mix_server

# Install the package in editable mode
pip install -e .
```

### Development Installation

To install with development dependencies (including pytest):

```bash
# Install with dev dependencies
pip install -e ".[dev]"
```

Or install dev dependencies separately:

```bash
# First install the package
pip install -e .

# Then install dev dependencies
pip install -e ".[dev]"
```

## Project Structure

```
mix_server/
├── data/                   # Sample data files
│   ├── sample.csv
│   └── sample.parquet
├── tools/                  # Core tool modules
│   ├── __init__.py
│   ├── csv_tools.py        # CSV file operations
│   ├── github_tools.py     # GitHub EPIC tools
│   └── parquet_tools.py    # Parquet file operations
├── utils/                  # Utility modules
│   └── file_reader.py      # File reading utilities
├── tests/                  # Test suite
│   └── test_github_tools.py
├── main.py                 # Main entry point
├── server.py               # MCP server implementation
├── pyproject.toml          # Project configuration
└── README.md              # This file
```

## Testing

### Running Tests

The project uses pytest for testing. After installing dev dependencies, you can run tests with:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=mix_server

# Run a specific test file
pytest tests/test_github_tools.py

# Run a specific test method
pytest tests/test_github_tools.py::TestGitHubEpicTools::test_epic_template_detection
```

### Test Coverage

To generate a detailed coverage report:

```bash
pytest --cov=mix_server --cov-report=html
```

This will create an HTML coverage report in the `htmlcov/` directory.

## Usage Examples

### CSV Tools

```python
from mix_server.tools.csv_tools import CSVProcessor

# Read CSV file
processor = CSVProcessor()
data = processor.read_csv("data/sample.csv")

# Write CSV file
processor.write_csv(data, "output.csv")
```

### Parquet Tools

```python
from mix_server.tools.parquet_tools import ParquetProcessor

# Read Parquet file
processor = ParquetProcessor()
data = processor.read_parquet("data/sample.parquet")

# Write Parquet file
processor.write_parquet(data, "output.parquet")
```

### GitHub EPIC Tools

```python
from mix_server.tools.github_tools import GitHubIssueCrawler, crawl_epic_updates

# Set up GitHub token
import os
os.environ['GITHUB_TOKEN'] = 'your-github-token'

# Crawl EPIC updates from a repository
epic_data = crawl_epic_updates(
    repo="organization/repository",
    days_back=30
)

# Generate board report
from mix_server.tools.github_tools import generate_board_report
report = generate_board_report(epic_data, format="executive")
print(report)
```

### MCP Server

```python
from mix_server.server import main

# Run the MCP server
if __name__ == "__main__":
    main()
```

## Configuration

### GitHub Token

For GitHub EPIC tools, you need to set up a GitHub personal access token:

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with appropriate permissions
3. Set the token as an environment variable:

```bash
export GITHUB_TOKEN="your-github-token"
```

Or set it in your Python code:

```python
import os
os.environ['GITHUB_TOKEN'] = 'your-github-token'
```

## Development

### Setting Up Development Environment

1. Clone the repository
2. Install in editable mode with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```
3. Set up pre-commit hooks (optional):
   ```bash
   pre-commit install
   ```

### Code Style

The project follows PEP 8 style guidelines. You can check your code with:

```bash
# Install flake8 if not already installed
pip install flake8

# Run flake8
flake8 mix_server/
```

### Adding New Tests

When adding new functionality, please include corresponding tests:

1. Create test functions in the appropriate test file
2. Use pytest fixtures for test data setup
3. Follow the existing test naming convention: `test_<function_name>`
4. Run tests to ensure they pass

### Running the Server

To run the MCP server:

```bash
python server.py
```

Or use the main entry point:

```bash
python main.py
```

## Dependencies

### Core Dependencies

- `mcp[cli]>=1.12.1`: Model Context Protocol implementation
- `pandas>=2.3.1`: Data manipulation and analysis
- `pyarrow>=21.0.0`: Apache Arrow integration for Parquet files
- `requests>=2.31.0`: HTTP library for API calls

### Development Dependencies

- `pytest>=7.0.0`: Testing framework
- `pytest-cov>=4.0.0`: Coverage reporting for pytest

## Contributing

1. Fork the repository
2. Create a feature branch: `git checkout -b feature-name`
3. Make your changes and add tests
4. Run tests to ensure everything works: `pytest`
5. Commit your changes: `git commit -am 'Add feature'`
6. Push to the branch: `git push origin feature-name`
7. Submit a pull request

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you've installed the package in editable mode with `pip install -e .`
2. **GitHub API errors**: Verify your GitHub token is set correctly and has appropriate permissions
3. **Test failures**: Ensure all dev dependencies are installed with `pip install -e ".[dev]"`

### Getting Help

If you encounter issues:

1. Check the test suite for usage examples
2. Review the error messages carefully
3. Ensure all dependencies are properly installed
4. Check that your Python version is 3.12 or higher

## Changelog

### Version 0.1.0
- Initial release
- CSV and Parquet file tools
- GitHub EPIC tools
- MCP server implementation
- Comprehensive test suite
