# Development Guide

This guide covers everything you need to know for developing and contributing to the GitHub MCP EPIC tools project.

## 🚀 **Quick Start for Developers**

### Prerequisites
- Python 3.8+
- `uv` package manager (recommended) or `pip`
- Git
- GitHub account with repository access

### Environment Setup

```bash
# 1. Clone the repository
git clone <your-repo-url>
cd mcp_research/mcp_intro/github_workflows

# 2. Install uv (if not already installed)
curl -LsSf https://astral.sh/uv/install.sh | sh

# 3. Create and activate virtual environment
uv venv
source .venv/bin/activate  # On Windows: .venv\Scripts\activate

# 4. Install dependencies
uv pip install -e .
```

## 🔐 **GitHub Token Setup (CRITICAL)**

> **⚠️ IMPORTANT: This is required for accessing private repositories and avoiding rate limits**

### **Why You Need a GitHub Token**

- **Private Repositories**: Access to private repos in your personal account or organization
- **Rate Limits**: Higher rate limits (5000 requests/hour vs 60 requests/hour)
- **Organization Access**: Access to organization repositories
- **Authentication**: Proper identification for API requests

### **Token Creation Steps**

1. **Go to GitHub Settings**
   ```
   GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
   ```

2. **Generate New Token**
   - Click "Generate new token (classic)"
   - Give it a descriptive name (e.g., "MCP EPIC Tools Development")
   - Set expiration (recommend 90 days for development)

3. **Select Required Scopes**
   - ✅ `repo` - Full control of private repositories
   - ✅ `read:org` - Read organization data  
   - ✅ `read:user` - Read user profile information

4. **Generate and Copy Token**
   - Click "Generate token"
   - **IMPORTANT**: Copy the token immediately (you won't see it again)

### **Setting Up the Token**

```bash
# Method 1: Environment variable (recommended for development)
export GITHUB_TOKEN='ghp_your_token_here'

# Method 2: Add to shell profile (persistent)
echo 'export GITHUB_TOKEN="ghp_your_token_here"' >> ~/.zshrc
source ~/.zshrc

# Method 3: Verify token is set
echo $GITHUB_TOKEN
```

### **Token Security Best Practices**

- 🔒 **Never commit tokens to version control**
- 🔒 **Use environment variables, not hardcoded values**
- 🔒 **Set appropriate expiration dates**
- 🔒 **Use minimal required scopes**
- 🔒 **Rotate tokens regularly**

## 🛠️ **Development Tools**

### **UV Package Manager (Recommended)**

```bash
# Install uv
curl -LsSf https://astral.sh/uv/install.sh | sh

# Create virtual environment
uv venv

# Activate environment
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dependencies
uv pip install -e .

# Add new dependency
uv add requests

# Install dev dependencies
uv add --dev pytest pytest-cov black flake8
```

### **Alternative: Traditional pip/venv**

```bash
# Create virtual environment
python -m venv .venv

# Activate environment
source .venv/bin/activate  # Linux/macOS
# .venv\Scripts\activate   # Windows

# Install dependencies
pip install -e .

# Install dev dependencies
pip install -r requirements-dev.txt
```

## 🧪 **Testing**

### **Running Tests**

```bash
# Run all tests
pytest

# Run tests with coverage
pytest --cov=github_mcp

# Run specific test file
pytest tests/test_github_tools.py

# Run specific test
pytest tests/test_github_tools.py::TestGitHubEpicTools::test_extract_epic_updates

# Run tests with verbose output
pytest -v

# Run tests and generate HTML coverage report
pytest --cov=github_mcp --cov-report=html
```

### **Test Structure**

```
tests/
├── test_github_setup.py      # GitHub token and repository access tests
├── test_github_tools.py      # Core functionality tests
└── conftest.py              # Test configuration and fixtures
```

### **Writing Tests**

```python
# Example test structure
import pytest
from unittest.mock import patch, Mock
from github_mcp.tools.github_tools import GitHubIssueCrawler

class TestGitHubEpicTools:
    def test_extract_epic_updates(self):
        """Test EPIC update extraction"""
        # Arrange
        crawler = GitHubIssueCrawler()
        
        # Act
        result = crawler.extract_epic_updates("microsoft/vscode", days_back=7)
        
        # Assert
        assert isinstance(result, list)
        assert len(result) >= 0
```

## 📝 **Code Quality**

### **Code Formatting**

```bash
# Format code with black
black github_mcp/ tests/ example/

# Check formatting without changes
black --check github_mcp/ tests/ example/
```

### **Linting**

```bash
# Run flake8 linting
flake8 github_mcp/ tests/ example/

# Run with specific configuration
flake8 --max-line-length=88 --ignore=E203,W503 github_mcp/
```

### **Type Checking**

```bash
# Run mypy type checking
mypy github_mcp/

# Run with strict mode
mypy --strict github_mcp/
```

## 🏗️ **Project Structure**

```
mcp_intro/github_workflows/
├── github_mcp/                 # Core library
│   ├── tools/                 # MCP tools implementation
│   │   ├── github_tools.py    # Main GitHub tools
│   │   ├── csv_tools.py       # CSV processing tools
│   │   └── parquet_tools.py   # Parquet processing tools
│   └── utils/                 # Utility functions
│       └── file_reader.py     # File reading utilities
├── example/                   # Example implementations
│   ├── base_example.py        # Base class for examples
│   ├── crawling_examples.py   # Crawling examples
│   ├── report_examples.py     # Report generation examples
│   ├── direct_api_examples.py # Direct API usage examples
│   └── main_runner.py         # Example orchestrator
├── tests/                     # Test suite
│   ├── test_github_setup.py   # Setup and access tests
│   └── test_github_tools.py   # Core functionality tests
├── github_workflows/          # GitHub Actions workflows
├── data/                      # Sample data files
├── pyproject.toml            # Project configuration
├── README.md                 # Main project documentation
├── DEVELOPMENT.md            # This development guide
└── TESTING.md               # Testing documentation
```

## 🔄 **Development Workflow**

### **1. Feature Development**

```bash
# Create feature branch
git checkout -b feature/new-epic-tool

# Make changes and test
pytest tests/

# Format and lint code
black github_mcp/
flake8 github_mcp/

# Commit changes
git add .
git commit -m "feat: add new EPIC tool functionality"
```

### **2. Running Examples**

```bash
# Run all examples
cd example
python main_runner.py

# Run specific example type
python main_runner.py --type reports

# Run specific example
python main_runner.py --example reports:board_report
```

### **3. Testing with Different Repositories**

```bash
# Test with public repository
python main_runner.py --repo "microsoft/vscode"

# Test with private repository (requires token)
export GITHUB_TOKEN='your-token'
python main_runner.py --repo "your-org/private-repo"
```

## 🐛 **Debugging**

### **Common Issues**

#### **1. Rate Limiting (403 Errors)**
```bash
# Check if token is set
echo $GITHUB_TOKEN

# Verify token permissions
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/user
```

#### **2. Repository Access Issues**
```bash
# Test repository access
curl -H "Authorization: token $GITHUB_TOKEN" https://api.github.com/repos/your-org/your-repo
```

#### **3. Import Errors**
```bash
# Ensure you're in the virtual environment
which python
# Should show: /path/to/project/.venv/bin/python

# Reinstall package in development mode
uv pip install -e .
```

### **Debug Mode**

```python
# Enable debug logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Or set environment variable
export PYTHONPATH="${PYTHONPATH}:$(pwd)"
```

## 📦 **Packaging and Distribution**

### **Building Package**

```bash
# Build package
uv build

# Install in development mode
uv pip install -e .
```

### **Publishing**

```bash
# Build and publish to PyPI
uv publish
```

## 🤝 **Contributing**

### **Before Submitting**

1. **Run all tests**
   ```bash
   pytest
   ```

2. **Check code quality**
   ```bash
   black --check github_mcp/ tests/
   flake8 github_mcp/ tests/
   ```

3. **Update documentation**
   - Update README.md if needed
   - Add docstrings to new functions
   - Update example documentation

4. **Test examples**
   ```bash
   cd example
   python main_runner.py --type all
   ```

### **Pull Request Checklist**

- [ ] Tests pass
- [ ] Code is formatted (black)
- [ ] Linting passes (flake8)
- [ ] Documentation updated
- [ ] Examples tested
- [ ] GitHub token setup documented (if relevant)

## 🔧 **Environment Variables**

| Variable | Purpose | Required | Example |
|----------|---------|----------|---------|
| `GITHUB_TOKEN` | GitHub API authentication | Yes (for private repos) | `ghp_abc123...` |
| `PYTHONPATH` | Python module path | No | `.:/path/to/project` |
| `DEBUG` | Enable debug logging | No | `1` |

## 📚 **Additional Resources**

- [GitHub API Documentation](https://docs.github.com/en/rest)
- [GitHub Personal Access Tokens](https://docs.github.com/en/authentication/keeping-your-account-and-data-secure/creating-a-personal-access-token)
- [UV Package Manager](https://docs.astral.sh/uv/)
- [Pytest Documentation](https://docs.pytest.org/)
- [Black Code Formatter](https://black.readthedocs.io/)

## 🆘 **Getting Help**

1. **Check the documentation** - Start with README.md and this guide
2. **Run tests** - Ensure your environment is set up correctly
3. **Check GitHub token** - Verify authentication is working
4. **Review examples** - Look at the example implementations
5. **Open an issue** - If you're still stuck, create a detailed issue

---

**Happy coding! 🚀**

---

## 🤖 **Generated with Cursor**

This documentation was generated with the help of **Cursor**, an AI-powered code editor that provides intelligent assistance for documentation, code generation, and development workflows.

**Cursor Features Used:**
- 📝 **Documentation Generation** - AI-assisted writing and structuring
- 🔧 **Code Analysis** - Intelligent code review and suggestions
- 🎯 **Context Awareness** - Understanding of project structure and requirements
- 📚 **Best Practices** - Integration of development standards and conventions
