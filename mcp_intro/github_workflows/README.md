# GitHub MCP Server

A comprehensive Model Context Protocol (MCP) server implementation that provides tools for working with CSV, Parquet files, and GitHub EPIC updates. This package includes utilities for data processing, file operations, and GitHub issue management.

## Features

- **GitHub EPIC Tools**: Crawl and analyze GitHub EPIC updates from issues
- **CSV Tools**: Read, write, and manipulate CSV files
- **Parquet Tools**: Handle Parquet file operations with pandas and pyarrow
- **MCP Integration**: Full Model Context Protocol server implementation
- **Comprehensive Testing**: Complete test suite with pytest

## Installation

### Prerequisites

- Python 3.12 or higher
- pip (Python package installer)
- GitHub personal access token (for GitHub features)

> **⚠️ IMPORTANT: GitHub Token Required**
> 
> **For Private Repositories:** You **MUST** set up a GitHub Personal Access Token to access private repositories in your personal account or organization.
> 
> **For Public Repositories:** A token is optional but recommended for higher rate limits.
> 
> See **[DEVELOPMENT.md](DEVELOPMENT.md)** for detailed token setup instructions.

### Basic Installation

```bash
# Clone the repository
git clone <repository-url>
cd mcp_research/mcp_intro/github_workflows

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
github_workflows/
├── github_mcp/              # Main package
│   ├── __init__.py          # Package initialization
│   ├── tools/               # Core tool modules
│   │   ├── __init__.py
│   │   ├── csv_tools.py     # CSV file operations
│   │   ├── github_tools.py  # GitHub EPIC tools
│   │   └── parquet_tools.py # Parquet file operations
│   └── utils/               # Utility modules
│       ├── __init__.py
│       └── file_reader.py   # File reading utilities
├── tests/                   # Test suite
│   └── test_github_tools.py # GitHub tools tests
├── data/                    # Sample data files
│   ├── sample.csv
│   └── sample.parquet
├── main.py                  # Main entry point
├── server.py                # MCP server implementation
├── generate_parquet.py      # Data generation script
├── pyproject.toml           # Project configuration
└── README.md               # This file
```

## Development

For comprehensive development information, including GitHub token setup, environment management, and contribution guidelines, see **[DEVELOPMENT.md](DEVELOPMENT.md)**.

## Testing

### Running Tests

The project uses pytest for testing. After installing dev dependencies, you can run tests with:

```bash
# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage report
pytest --cov=github_mcp

# Run a specific test file
pytest tests/test_github_tools.py

# Run a specific test method
pytest tests/test_github_tools.py::TestGitHubEpicTools::test_epic_template_detection

# Run tests with output capture disabled (for debugging)
pytest -v -s
```

### Test Coverage

To generate a detailed coverage report:

```bash
# HTML coverage report
pytest --cov=github_mcp --cov-report=html

# Console coverage report
pytest --cov=github_mcp --cov-report=term-missing

# XML coverage report (for CI/CD)
pytest --cov=github_mcp --cov-report=xml
```

This will create an HTML coverage report in the `htmlcov/` directory.

### Test Structure

The test suite follows pytest best practices:

- **Fixtures**: Reusable test data and setup
- **Mocking**: Proper isolation of external dependencies
- **Parameterized tests**: Testing multiple scenarios
- **Error handling**: Testing edge cases and error conditions

## Usage Examples

### GitHub EPIC Tools

```python
from github_mcp.tools.github_tools import GitHubIssueCrawler, crawl_epic_updates

# Set up GitHub token
import os
os.environ['GITHUB_TOKEN'] = 'your-github-token'

# Crawl EPIC updates from a repository
epic_data = crawl_epic_updates(
    repo="organization/repository",
    days_back=30
)

# Generate board report
from github_mcp.tools.github_tools import generate_board_report
report = generate_board_report(epic_data, format="executive")
print(report)

# Analyze trends
from github_mcp.tools.github_tools import analyze_epic_trends
trends = analyze_epic_trends(epic_data)
print(trends)
```

### CSV Tools

```python
from github_mcp.tools.csv_tools import summarize_csv_file, read_csv_file

# Summarize CSV file
summary = summarize_csv_file("data/sample.csv")
print(summary)

# Read CSV file contents
contents = read_csv_file("data/sample.csv")
print(contents)
```

### Parquet Tools

```python
from github_mcp.tools.parquet_tools import summarize_parquet_file, read_parquet_file

# Summarize Parquet file
summary = summarize_parquet_file("data/sample.parquet")
print(summary)

# Read Parquet file contents
contents = read_parquet_file("data/sample.parquet")
print(contents)
```

### MCP Server

```python
from github_mcp.server import main

# Run the MCP server
if __name__ == "__main__":
    main()
```

Or run directly:

```bash
python server.py
```

## Configuration

### GitHub Token

For GitHub EPIC tools, you need to set up a GitHub personal access token:

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with appropriate permissions (repo, issues, comments)
3. Set the token as an environment variable:

```bash
export GITHUB_TOKEN="your-github-token"
```

Or set it in your Python code:

```python
import os
os.environ['GITHUB_TOKEN'] = 'your-github-token'
```

### Environment Variables

```bash
# Required for GitHub features
export GITHUB_TOKEN="your-github-token"

# Optional: External data directory
export EXTERNAL_DATA_DIR="/path/to/external/data"
```

## Development

### Setting Up Development Environment

1. Clone the repository and navigate to the project:
   ```bash
   cd mcp_research/mcp_intro/github_workflows
   ```

2. Install in editable mode with dev dependencies:
   ```bash
   pip install -e ".[dev]"
   ```

3. Set up pre-commit hooks (optional):
   ```bash
   pip install pre-commit
   pre-commit install
   ```

### Code Style

The project follows PEP 8 style guidelines. You can check your code with:

```bash
# Install linting tools
pip install flake8 black isort

# Run flake8
flake8 github_mcp/

# Format code with black
black github_mcp/

# Sort imports with isort
isort github_mcp/
```

### Adding New Tests

When adding new functionality, please include corresponding tests:

1. Create test functions in the appropriate test file
2. Use pytest fixtures for test data setup
3. Follow the existing test naming convention: `test_<function_name>`
4. Use proper mocking for external dependencies
5. Test both success and error cases
6. Run tests to ensure they pass

Example test structure:

```python
def test_new_functionality(self, sample_data):
    """Test new functionality"""
    # Arrange
    expected_result = "expected"
    
    # Act
    result = new_function(sample_data)
    
    # Assert
    assert result == expected_result
```

### Running the Server

To run the MCP server:

```bash
# Run the server directly
python server.py

# Or use the main entry point
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
5. Check code style: `flake8 github_mcp/`
6. Commit your changes: `git commit -am 'Add feature'`
7. Push to the branch: `git push origin feature-name`
8. Submit a pull request

### Development Guidelines

- Write tests for all new functionality
- Follow PEP 8 style guidelines
- Use type hints where appropriate
- Update documentation as needed
- Ensure all tests pass before submitting

## Troubleshooting

### Common Issues

1. **Import errors**: Make sure you've installed the package in editable mode with `pip install -e ".[dev]"`
2. **GitHub API errors**: Verify your GitHub token is set correctly and has appropriate permissions
3. **Test failures**: Ensure all dev dependencies are installed with `pip install -e ".[dev]"`
4. **Package not found**: Check that you're in the correct directory (`mcp_intro/github_workflows`)

### Getting Help

If you encounter issues:

1. Check the test suite for usage examples
2. Review the error messages carefully
3. Ensure all dependencies are properly installed
4. Check that your Python version is 3.12 or higher
5. Verify your GitHub token has the correct permissions

### Debug Mode

For debugging test issues:

```bash
# Run tests with output capture disabled
pytest -v -s

# Run specific test with debugging
pytest tests/test_github_tools.py::TestGitHubEpicTools::test_specific_test -v -s
```

## License

This project is licensed under the MIT License - see the LICENSE file for details.

## Changelog

### Version 0.1.0
- Initial release
- GitHub EPIC tools with comprehensive parsing
- CSV and Parquet file tools
- MCP server implementation
- Comprehensive test suite with pytest
- Full development workflow setup

---

**For more information about the overall project, see the main [README.md](../../README.md)**

---

## 🤖 **Generated with Cursor**

This documentation was generated with the help of **Cursor**, an AI-powered code editor that provides intelligent assistance for documentation, code generation, and development workflows.

**Cursor Features Used:**
- 📝 **Documentation Generation** - AI-assisted writing and structuring
- 🔧 **Code Analysis** - Intelligent code review and suggestions
- 🎯 **Context Awareness** - Understanding of project structure and requirements
- 📚 **Best Practices** - Integration of development standards and conventions

