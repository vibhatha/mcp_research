# MCP Research

A comprehensive research project exploring Model Context Protocol (MCP) implementations, GitHub workflows, and data processing tools. This repository contains various MCP server implementations and research experiments.

## 🚀 Project Overview

This repository serves as a research platform for exploring and implementing Model Context Protocol (MCP) servers, with a focus on:

- **GitHub Integration**: EPIC update tools and workflow automation
- **Data Processing**: CSV and Parquet file handling
- **MCP Server Development**: Various server implementations
- **Testing & Development**: Comprehensive test suites and development workflows

## 📁 Project Structure

```
mcp_research/
├── mcp_intro/                    # MCP Introduction and Examples
│   └── github_workflows/         # GitHub MCP Server Implementation
│       ├── github_mcp/           # Main package
│       │   ├── tools/            # Core tools (CSV, Parquet, GitHub)
│       │   └── utils/            # Utility modules
│       ├── tests/                # Test suite
│       ├── data/                 # Sample data files
│       ├── pyproject.toml        # Project configuration
│       └── README.md            # Detailed documentation
├── LICENSE                       # MIT License
├── .gitignore                   # Git ignore rules
└── README.md                    # This file
```

## 🛠️ Development Setup

### Prerequisites

- **Python**: 3.12 or higher
- **Git**: For version control
- **pip**: Python package installer
- **GitHub Token**: For GitHub API access (optional)

### Quick Start

1. **Clone the repository**:
   ```bash
   git clone <repository-url>
   cd mcp_research
   ```

2. **Set up virtual environment** (recommended):
   ```bash
   python -m venv .venv
   source .venv/bin/activate  # On Windows: .venv\Scripts\activate
   ```

3. **Install dependencies**:
   ```bash
   # Install main project dependencies
   pip install -r requirements.txt  # if available
   
   # Or install specific subprojects
   cd mcp_intro/github_workflows
   pip install -e ".[dev]"
   ```

## 🧪 Testing

### Running Tests

The project uses pytest for comprehensive testing:

```bash
# Navigate to the specific project
cd mcp_intro/github_workflows

# Run all tests
pytest

# Run with verbose output
pytest -v

# Run with coverage
pytest --cov=github_mcp

# Run specific test file
pytest tests/test_github_tools.py

# Run specific test method
pytest tests/test_github_tools.py::TestGitHubEpicTools::test_epic_template_detection
```

### Test Coverage

Generate detailed coverage reports:

```bash
# HTML coverage report
pytest --cov=github_mcp --cov-report=html

# Console coverage report
pytest --cov=github_mcp --cov-report=term-missing
```

## 🔧 Development Workflow

### Code Style

The project follows PEP 8 style guidelines:

```bash
# Install linting tools
pip install flake8 black isort

# Run linting
flake8 github_mcp/
black github_mcp/
isort github_mcp/
```

### Pre-commit Hooks

Set up pre-commit hooks for automated code quality checks:

```bash
# Install pre-commit
pip install pre-commit

# Install hooks
pre-commit install

# Run hooks manually
pre-commit run --all-files
```

### Adding New Features

1. **Create a feature branch**:
   ```bash
   git checkout -b feature/your-feature-name
   ```

2. **Make your changes** and add tests

3. **Run tests** to ensure everything works:
   ```bash
   pytest
   ```

4. **Commit your changes**:
   ```bash
   git add .
   git commit -m "Add feature: description"
   ```

5. **Push and create a pull request**

## 📦 Subprojects

### GitHub Workflows MCP Server

Located in `mcp_intro/github_workflows/`, this is a comprehensive MCP server implementation that provides:

- **GitHub EPIC Tools**: Crawl and analyze GitHub EPIC updates
- **CSV Processing**: Read, write, and manipulate CSV files
- **Parquet Tools**: Handle Parquet file operations
- **MCP Integration**: Full Model Context Protocol server implementation

For detailed documentation, see [mcp_intro/github_workflows/README.md](mcp_intro/github_workflows/README.md).

## 🔐 Configuration

### GitHub Token Setup

For GitHub-related functionality:

1. Go to GitHub Settings → Developer settings → Personal access tokens
2. Generate a new token with appropriate permissions
3. Set as environment variable:
   ```bash
   export GITHUB_TOKEN="your-github-token"
   ```

### Environment Variables

```bash
# GitHub API access
export GITHUB_TOKEN="your-github-token"

# External data directory (optional)
export EXTERNAL_DATA_DIR="/path/to/external/data"
```

## 🚀 Usage Examples

### Running the MCP Server

```bash
cd mcp_intro/github_workflows
python server.py
```

### Using GitHub EPIC Tools

```python
from github_mcp.tools.github_tools import crawl_epic_updates, generate_board_report

# Crawl EPIC updates
epic_data = crawl_epic_updates("organization/repository", days_back=30)

# Generate reports
report = generate_board_report(epic_data, format="executive")
print(report)
```

### Data Processing

```python
from github_mcp.tools.csv_tools import summarize_csv_file
from github_mcp.tools.parquet_tools import summarize_parquet_file

# Process CSV files
summary = summarize_csv_file("data/sample.csv")

# Process Parquet files
summary = summarize_parquet_file("data/sample.parquet")
```

## 🐛 Troubleshooting

### Common Issues

1. **Import errors**: Ensure you've installed the package in editable mode
   ```bash
   pip install -e ".[dev]"
   ```

2. **GitHub API errors**: Verify your GitHub token is set correctly
   ```bash
   echo $GITHUB_TOKEN
   ```

3. **Test failures**: Check that all dev dependencies are installed
   ```bash
   pip install -e ".[dev]"
   pytest --version
   ```

4. **Python version issues**: Ensure you're using Python 3.12+
   ```bash
   python --version
   ```

### Getting Help

- Check the test suite for usage examples
- Review error messages carefully
- Ensure all dependencies are properly installed
- Verify Python version compatibility

## 📚 Documentation

- [GitHub Workflows MCP Server](mcp_intro/github_workflows/README.md) - Detailed documentation for the main MCP server
- [Model Context Protocol](https://modelcontextprotocol.io/) - Official MCP documentation
- [GitHub API](https://docs.github.com/en/rest) - GitHub REST API documentation

## 🤝 Contributing

We welcome contributions! Please follow these steps:

1. Fork the repository
2. Create a feature branch (`git checkout -b feature/amazing-feature`)
3. Make your changes and add tests
4. Run tests to ensure everything works (`pytest`)
5. Commit your changes (`git commit -m 'Add amazing feature'`)
6. Push to the branch (`git push origin feature/amazing-feature`)
7. Open a Pull Request

### Development Guidelines

- Write tests for new functionality
- Follow PEP 8 style guidelines
- Update documentation as needed
- Ensure all tests pass before submitting

## 📄 License

This project is licensed under the MIT License - see the [LICENSE](LICENSE) file for details.

## 🗺️ Roadmap

- [ ] Additional MCP server implementations
- [ ] Enhanced GitHub workflow tools
- [ ] More data processing capabilities
- [ ] Integration with other MCP clients
- [ ] Performance optimizations
- [ ] Extended test coverage

## 📞 Support

For questions, issues, or contributions:

1. Check existing issues and documentation
2. Create a new issue with detailed information
3. Include error messages, environment details, and reproduction steps

---

**Happy coding! 🚀**