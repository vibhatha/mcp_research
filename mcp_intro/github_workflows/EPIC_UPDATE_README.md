# EPIC Summary Generator CLI

A command-line tool for generating comprehensive EPIC summaries from GitHub issues. This tool uses the built-in `github_mcp` library to crawl GitHub issues, find EPIC update comments, and generate structured reports for project management and status tracking.

## Features

- **Flexible Issue Input**: Accept issue numbers via command line or from text files
- **Smart Comment Filtering**: Only processes actual EPIC update comments, skips trigger comments
- **Multiple Output Formats**: Generates board reports, status summaries, and raw data
- **Date Filtering**: Filter updates by specific dates or date ranges
- **Repository Support**: Works with both public and private repositories
- **Comprehensive Validation**: Validates inputs and provides clear error messages

## Prerequisites

### Python Requirements
- Python 3.12 or higher
- The tool uses the built-in `github_mcp` library which handles all dependencies automatically
- No additional package installation required beyond the project dependencies

### GitHub Access
- **Public repositories**: No token required
- **Private repositories**: GitHub Personal Access Token required

#### Setting up GitHub Token
```bash
# Set environment variable
export GITHUB_TOKEN='your-github-token'

# Or add to your shell profile (~/.bashrc, ~/.zshrc, etc.)
echo 'export GITHUB_TOKEN="your-github-token"' >> ~/.zshrc
source ~/.zshrc
```

#### Creating a GitHub Token
1. Go to GitHub.com → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `read:org`, `read:user`
4. Copy the token and set it as environment variable

## Installation

1. Clone the repository:
```bash
git clone <repository-url>
cd mcp_intro/github_workflows
```

2. Install dependencies:
```bash
# Using uv (recommended)
uv sync

# Or using pip
pip install -e .
```

3. Make the script executable:
```bash
chmod +x epic_summary_generator.py
```

## Usage

### Basic Syntax

```bash
python epic_summary_generator.py --repo <org/repo> --date <YYYY-MM-DD> --output <path> [--issues <numbers> | --issues-file <path>]
```

### Required Parameters

- `--repo`, `-r`: Repository name in `org/repo` format (e.g., `microsoft/vscode`)
- `--date`, `-d`: Target date for the summary in `YYYY-MM-DD` format
- `--output`, `-o`: Path to save the output report (JSON format)

### Issue Numbers Source (one required)

- `--issues`: Comma-separated list of issue numbers (e.g., `151,152,153`)
- `--issues-file`, `-f`: Path to file containing issue numbers

### Optional Parameters

- `--verbose`, `-v`: Enable verbose output for debugging

## Examples

### 1. Using Issue Numbers from Command Line

```bash
# Basic usage with comma-separated issue numbers
python epic_summary_generator.py \
  --repo LDFLK/launch \
  --date 2025-08-07 \
  --output reports/report.json \
  --issues 144

# Using short form arguments
python epic_summary_generator.py \
  -r LDFLK/launch \
  -d 2025-08-07 \
  -o reports/report.json \
  --issues 144
```

### 2. Using Issue Numbers from File

Create a file `sample_issues.txt`:
```txt
# Sample issue numbers for testing EPIC summary generator
# You can use either comma-separated or one per line format

# Comma-separated format:
151,152,153

# Or one per line format:
# 151
# 152
# 153

# For testing with public repositories, you can use:
# microsoft/vscode issues: 1,2,3
# octocat/Hello-World issues: 1,2
```

Then run:
```bash
# Using issue file
python epic_summary_generator.py \
  --repo microsoft/vscode \
  --date 2024-01-15 \
  --output report.json \
  --issues-file sample_issues.txt

# Using short form
python epic_summary_generator.py \
  -r microsoft/vscode \
  -d 2024-01-15 \
  -o report.json \
  -f sample_issues.txt
```

### 3. Verbose Output for Debugging

```bash
python epic_summary_generator.py \
  --repo LDFLK/launch \
  --date 2025-08-07 \
  --output debug_report.json \
  --issues 144 \
  --verbose
```

## Output Format

The tool generates a JSON file containing:

```json
{
  "repo": "org/repo",
  "target_date": "2024-01-15",
  "issue_numbers": [151, 152, 153],
  "generated_at": "2024-01-15T10:30:00.000000",
  "board_report": "# EPIC Update Report\n\n...",
  "status_summary": "# EPIC Status Summary\n\n...",
  "raw_epic_data": {
    "total_updates": 2,
    "repo": "org/repo",
    "issue_numbers": [151, 152, 153],
    "updates": [
      {
        "issue_number": 151,
        "issue_title": "EPIC Title",
        "comment_id": 123456,
        "comment_body": "<!-- epic-update-template -->\n## 🚀 Epic Update\n...",
        "author": "username",
        "created_at": "2024-01-15T10:00:00Z",
        "repo": "org/repo",
        "parsed_data": {
          "date": "2024-01-15",
          "owner": "@username",
          "epic_name": "Epic Name",
          "status": "On Track",
          "progress": "75%",
          "what_happened": ["Progress item 1", "Progress item 2"],
          "scope_changes": ["Scope change 1"],
          "risks_blockers": ["Risk 1"],
          "next_steps": ["Next step 1", "Next step 2"],
          "metrics_deliverables": ["Metric 1"]
        }
      }
    ]
  }
}
```

## EPIC Update Comment Format

The tool looks for comments that follow this EPIC update template:

```markdown
<!-- epic-update-template -->
## 🚀 Epic Update

**Date:** 2024-01-15
**Owner:** @username 
**Epic:** Epic Name

### Status
- **Current status:** _On Track_
- **Progress (%):** 75%

### What happened since last update
- Progress item 1
- Progress item 2

### Scope changes
- Scope change 1

### Risks / blockers
- Risk 1

### Next steps (with owners & dates)
- Next step 1
- Next step 2

### Metrics / deliverables
- Metric 1

---

> _Generated automatically because you typed `@epic-update`_
```

## Comment Filtering

The tool intelligently filters comments to only process actual EPIC updates:

### ✅ Included Comments
- Comments containing `<!-- epic-update-template -->`
- Comments with `## 🚀 Epic Update` header
- Comments with structured EPIC update content

### ❌ Excluded Comments
- Comments that are just `@epic-update` (trigger comments)
- Regular issue comments without EPIC update format
- Empty or very short comments

## Error Handling

The tool provides clear error messages for common issues:

### Validation Errors
```bash
❌ Validation error: Invalid repository format: invalid-repo. Use 'org/repo' format.
❌ Validation error: Invalid date format: invalid-date. Use YYYY-MM-DD format.
❌ No valid issue numbers found.
```

### GitHub Token Warnings
```bash
⚠️  Warning: GITHUB_TOKEN environment variable not set
   Set it with: export GITHUB_TOKEN='your-github-token'
   For public repositories, this may not be required.
```

### File Errors
```bash
Error: Issue file 'nonexistent.txt' not found.
Error reading issue file: [Errno 2] No such file or directory
```

## Troubleshooting

### No EPIC Updates Found

1. **Check issue numbers**: Verify the issue numbers exist in the repository
2. **Check date range**: Ensure the target date matches when EPIC updates were posted
3. **Check comment format**: Verify comments follow the EPIC update template
4. **Check repository access**: Ensure you have access to the repository

### Permission Errors

1. **Public repositories**: Should work without a token
2. **Private repositories**: Ensure `GITHUB_TOKEN` is set with correct permissions
3. **Rate limiting**: GitHub API has rate limits; wait and retry

### Parsing Issues

1. **Comment format**: Ensure comments follow the exact EPIC update template
2. **Special characters**: Check for encoding issues in comments
3. **Template variations**: The tool supports common variations of the template

## Integration Examples

### With CI/CD Pipelines

```yaml
# GitHub Actions example
- name: Generate EPIC Summary
  run: |
    python epic_summary_generator.py \
      --repo ${{ github.repository }} \
      --date $(date +%Y-%m-%d) \
      --output epic_summary.json \
      --issues-file epic_issues.txt
```

### With Scripts

```bash
#!/bin/bash
# Generate weekly EPIC summary
python epic_summary_generator.py \
  --repo myorg/myproject \
  --date $(date -d "last monday" +%Y-%m-%d) \
  --output weekly_epic_summary.json \
  --issues-file weekly_epics.txt

# Send to Slack or other tools
curl -X POST -H 'Content-type: application/json' \
  --data @weekly_epic_summary.json \
  https://hooks.slack.com/services/YOUR/WEBHOOK/URL
```

## Contributing

1. Fork the repository
2. Create a feature branch
3. Make your changes
4. Add tests if applicable
5. Submit a pull request

## License

[Add your license information here]

## Support

For issues and questions:
1. Check the troubleshooting section above
2. Review the error messages for specific guidance
3. Open an issue in the repository with:
   - Command used
   - Error message
   - Repository and issue numbers (if applicable)
   - Expected vs actual behavior
