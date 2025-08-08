# GitHub MCP EPIC Examples

This directory contains organized examples for the GitHub MCP EPIC tools, demonstrating various use cases and functionality.

## ⚠️ **IMPORTANT: GitHub Token Required for Private Repositories**

> **🔐 Authentication Required**
> 
> **For Private Repositories:** You **MUST** set up a GitHub Personal Access Token to access private repositories in your personal account or organization.
> 
> **For Public Repositories:** A token is optional but recommended for higher rate limits.
> 
> **Without a token:** You'll encounter rate limiting (403 errors) and won't be able to access private repositories.

### 🚀 **Quick Token Setup**

```bash
# 1. Create a GitHub Personal Access Token
#    Go to: GitHub.com → Settings → Developer settings → Personal access tokens → Tokens (classic)
#    Generate new token with scopes: repo, read:org, read:user

# 2. Set the token in your environment
export GITHUB_TOKEN='your-github-token-here'

# 3. Verify the token is set
echo $GITHUB_TOKEN
```

### 📋 **Token Scopes Required**
- `repo` - Full control of private repositories
- `read:org` - Read organization data
- `read:user` - Read user profile information

### 🔧 **Alternative Setup Methods**

```bash
# Method 1: Environment variable (recommended)
export GITHUB_TOKEN='your-token'

# Method 2: In your shell profile (~/.zshrc, ~/.bashrc)
echo 'export GITHUB_TOKEN="your-token"' >> ~/.zshrc
source ~/.zshrc

# Method 3: In the script (not recommended for security)
import os
os.environ['GITHUB_TOKEN'] = 'your-token'
```

### 🚨 **Common Issues & Solutions**

| Issue | Cause | Solution |
|-------|-------|----------|
| `403 rate limit exceeded` | No token or invalid token | Set valid `GITHUB_TOKEN` |
| `Repository not found` | Private repo without access | Ensure token has `repo` scope |
| `401 Unauthorized` | Invalid or expired token | Generate new token |
| `403 Forbidden` | Insufficient permissions | Check token scopes |

## Structure

The examples are organized into focused classes for better maintainability and clarity:

### Core Files

- **`base_example.py`** - Base class with common utilities and configuration
- **`crawling_examples.py`** - Examples for crawling repositories and issues
- **`report_examples.py`** - Examples for generating reports and summaries
- **`direct_api_examples.py`** - Examples for using the GitHubIssueCrawler directly
- **`main_runner.py`** - Main orchestrator that runs all examples

### Legacy Files

- **`epic_updates.py`** - Original monolithic example file (deprecated)
- **`epic_updates_public.py`** - Public repository example (deprecated)

## Quick Start

### Run All Examples
```bash
python main_runner.py
```

### Run Specific Types of Examples
```bash
# Only crawling examples
python main_runner.py --type crawling

# Only report generation examples
python main_runner.py --type reports

# Only direct API examples
python main_runner.py --type api
```

### Run a Specific Example
```bash
# List all available examples
python main_runner.py --list

# Run a specific example
python main_runner.py --example crawling:repository
python main_runner.py --example reports:board_report
python main_runner.py --example api:crawler
```

### Customize Repository
```bash
# Use a different repository
python main_runner.py --repo "your-username/your-repo"

# Use a different issue URL
python main_runner.py --url "https://github.com/your-username/your-repo/issues/123"
```

## Example Categories

### 🔍 Crawling Examples (`crawling_examples.py`)

Demonstrates how to crawl EPIC updates from GitHub repositories:

- **Repository Crawling** - Crawl all EPIC updates from a repository
- **Specific Issues** - Crawl EPIC updates from specific issue numbers
- **Issue-Specific** - Get EPIC updates from a specific issue URL
- **Date Range** - Crawl EPIC updates within a specific date range
- **Issue Numbers Parameter** - Use the main function with issue numbers

### 📊 Report Examples (`report_examples.py`)

Demonstrates how to generate various reports from EPIC data:

- **Board Reports** - Generate executive and summary format reports
- **Status Summaries** - Generate EPIC status summaries
- **Trend Analysis** - Analyze EPIC trends over time
- **Dated Updates** - Process EPIC updates for specific dates
- **Custom Reports** - Generate reports in different formats
- **Report Comparison** - Compare reports from different time periods

### 🔧 Direct API Examples (`direct_api_examples.py`)

Demonstrates advanced usage of the GitHubIssueCrawler directly:

- **Direct Crawler Usage** - Use GitHubIssueCrawler directly
- **Custom Extraction** - Custom EPIC extraction with filtering
- **Issue Analysis** - Detailed analysis of specific issues
- **Comment Filtering** - Advanced comment filtering and statistics
- **Bulk Processing** - Process multiple repositories

## Available Examples

### Crawling Examples
- `repository` - Crawl EPIC updates from repository
- `specific_issues` - Crawl EPIC updates from specific issue numbers
- `issue` - Get EPIC updates from a specific issue

### Report Examples
- `board_report` - Generate board report
- `status_summary` - Generate EPIC status summary
- `trends` - Analyze EPIC trends
- `dated_update` - Process dated EPIC update

### API Examples
- `crawler` - Use GitHubIssueCrawler directly
- `custom_extraction` - Custom EPIC extraction with filtering
- `issue_analysis` - Detailed issue analysis
- `comment_filtering` - Advanced comment filtering
- `bulk_processing` - Bulk processing of multiple repositories

## Usage Examples

### Basic Usage
```python
from main_runner import MainRunner

# Run all examples
runner = MainRunner()
runner.run_all_examples()
```

### Run Specific Categories
```python
from main_runner import MainRunner

runner = MainRunner("microsoft/vscode")

# Run only crawling examples
epic_data = runner.run_crawling_only()

# Run report examples with the crawled data
runner.run_reports_only(epic_data)

# Run API examples
runner.run_api_only()
```

### Run Individual Examples
```python
from crawling_examples import CrawlingExamples
from report_examples import ReportExamples

# Run specific crawling example
crawler = CrawlingExamples()
epic_data = crawler.example_crawl_epic_updates()

# Run specific report example
reporter = ReportExamples()
reporter.example_generate_board_report(epic_data)
```

## Configuration

### GitHub Token Setup

> **📌 See the [GitHub Token Requirements](#-important-github-token-required-for-private-repositories) section above for detailed setup instructions.**

Most examples require a GitHub Personal Access Token for full functionality, especially for private repositories:

```bash
# Set your GitHub token
export GITHUB_TOKEN='your-github-token'

# Or set it in the script
import os
os.environ['GITHUB_TOKEN'] = 'your-token'
```

### Repository Configuration

You can customize the repository and issue URL used in examples:

```python
# Use your own repository
runner = MainRunner(
    repo_name="your-username/your-repo",
    github_url="https://github.com/your-username/your-repo/issues/123"
)
```

## Benefits of the New Structure

1. **Modularity** - Each example type is in its own class
2. **Reusability** - Common utilities are shared via the base class
3. **Maintainability** - Easier to add new examples or modify existing ones
4. **Clarity** - Clear separation of concerns
5. **Flexibility** - Run all examples, specific categories, or individual examples
6. **Documentation** - Each example is well-documented with clear purposes

## Migration from Old Structure

If you were using the old `epic_updates.py` file:

1. **Replace direct function calls** with the new class-based approach
2. **Use the main runner** for orchestrated execution
3. **Import specific classes** for targeted functionality
4. **Update configuration** to use the new constructor parameters

## Contributing

When adding new examples:

1. **Add to appropriate class** - Put examples in the most relevant class
2. **Follow naming convention** - Use `example_*` prefix for example methods
3. **Add documentation** - Include clear docstrings explaining the example
4. **Update main runner** - Add new examples to the main runner if needed
5. **Update README** - Document new examples in this README

---

## 🤖 **Generated with Cursor**

This documentation was generated with the help of **Cursor**, an AI-powered code editor that provides intelligent assistance for documentation, code generation, and development workflows.

**Cursor Features Used:**
- 📝 **Documentation Generation** - AI-assisted writing and structuring
- 🔧 **Code Analysis** - Intelligent code review and suggestions
- 🎯 **Context Awareness** - Understanding of project structure and requirements
- 📚 **Best Practices** - Integration of development standards and conventions

**Learn more:** [cursor.sh](https://cursor.sh)
