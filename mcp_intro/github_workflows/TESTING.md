# Testing Guide

This document explains how to test the GitHub MCP tools and repository access.

> **📌 For comprehensive development setup, including GitHub token configuration, see [DEVELOPMENT.md](DEVELOPMENT.md)**

## ⚠️ **GitHub Token Requirements**

> **🔐 Authentication Required for Private Repositories**
> 
> **Private Repositories:** You **MUST** set up a GitHub Personal Access Token to test private repository access.
> 
> **Public Repositories:** Tests work without a token, but rate limits apply.
> 
> **Without a token:** Private repository tests will be skipped, and you'll see rate limiting warnings.

## Test Structure

The project uses pytest for testing with the following test files:

- `tests/test_github_setup.py` - Tests for GitHub API access and repository permissions
- `tests/test_github_tools.py` - Tests for the GitHub EPIC tools functionality

## Running Tests

### All Tests
```bash
python -m pytest tests/ -v
```

### Specific Test Categories
```bash
# Test public repository access (works without token)
python -m pytest tests/test_github_setup.py::TestPublicRepositoryAccess -v

# Test private repository access (requires token)
python -m pytest tests/test_github_setup.py::TestPrivateRepositoryAccess -v

# Test GitHub token functionality
python -m pytest tests/test_github_setup.py::TestGitHubToken -v

# Test EPIC tools functionality
python -m pytest tests/test_github_tools.py -v
```

## GitHub Token Setup

To test private repository access and full functionality, you need a GitHub Personal Access Token.

> **📌 For detailed token setup instructions, see [DEVELOPMENT.md#github-token-setup-critical](DEVELOPMENT.md#-github-token-setup-critical)**

### Quick Setup
Run the setup helper:
```bash
python setup_github_token.py
```

### Manual Setup
1. Go to GitHub.com → Settings → Developer settings → Personal access tokens
2. Generate new token (classic)
3. Select scopes: `repo`, `read:org`, `read:user`
4. Set the token:
   ```bash
   export GITHUB_TOKEN='your-token-here'
   ```

### Token Scopes Required
- `repo` - Full control of private repositories
- `read:org` - Read organization data
- `read:user` - Read user profile information

## Test Categories

### Public Repository Tests
- ✅ Work without GitHub token
- Test access to public repositories like `octocat/Hello-World`, `microsoft/vscode`
- Verify rate limiting headers
- Test issue access

### Private Repository Tests
- ⚠️ Require valid GitHub token
- Test access to private repositories like `LDFLK/launch`
- Verify authentication works correctly
- Test private repository issues

### Token Validation Tests
- Test behavior with no token
- Test behavior with invalid token
- Test behavior with valid token
- Verify user authentication

### EPIC Tools Tests
- Test EPIC template detection and parsing
- Test GitHub API integration (mocked)
- Test report generation
- Test error handling

## Test Results Interpretation

### Without Token
- ✅ Public repository tests pass
- ⏭️ Private repository tests skipped
- ⏭️ Token validation tests skipped
- ✅ EPIC tools tests pass (with mocks)

### With Valid Token
- ✅ All tests run
- ✅ Private repository access verified
- ✅ Full functionality tested

## Troubleshooting

### Tests Skipped
If tests are being skipped, check:
1. Is `GITHUB_TOKEN` environment variable set?
2. Is the token valid and not expired?
3. Does the token have the required scopes?

### Private Repository Access Fails

---

1. Verify you have access to the repository on GitHub
2. Check that your token has the `repo` scope
3. Ensure the repository name is correct

### Rate Limiting
GitHub API has rate limits:
- Unauthenticated: 60 requests/hour
- Authenticated: 5000+ requests/hour

Tests are designed to be efficient and avoid hitting rate limits.

## Continuous Integration

For CI/CD environments:
1. Set `GITHUB_TOKEN` as a secret
2. Run tests with: `python -m pytest tests/ -v`
3. Tests will automatically skip private repository tests if no token is available

## Adding New Tests

When adding new tests:
1. Use appropriate test classes for organization
2. Use `@pytest.mark.skipif` for token-dependent tests
3. Mock external API calls when possible
4. Include both positive and negative test cases

## 🤖 **Generated with Cursor**

This documentation was generated with the help of **Cursor**, an AI-powered code editor that provides intelligent assistance for documentation, code generation, and development workflows.

**Cursor Features Used:**
- 📝 **Documentation Generation** - AI-assisted writing and structuring
- 🔧 **Code Analysis** - Intelligent code review and suggestions
- 🎯 **Context Awareness** - Understanding of project structure and requirements
- 📚 **Best Practices** - Integration of development standards and conventions