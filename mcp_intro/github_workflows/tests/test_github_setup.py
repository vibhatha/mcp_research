#!/usr/bin/env python3
"""
Pytest-based tests for GitHub setup and repository access.
Tests both public and private repository access scenarios.
"""

import os
import pytest
import requests
from unittest.mock import patch, Mock


class TestGitHubToken:
    """Test GitHub token functionality"""
    
    def test_github_token_not_set(self):
        """Test behavior when GitHub token is not set"""
        with patch.dict(os.environ, {}, clear=True):
            # Test that we can still access public repositories without a token
            headers = {'Accept': 'application/vnd.github.v3+json'}
            response = requests.get('https://api.github.com/repos/octocat/Hello-World', headers=headers)
            assert response.status_code == 200
    
    def test_github_token_invalid(self):
        """Test behavior with invalid GitHub token"""
        with patch.dict(os.environ, {'GITHUB_TOKEN': 'invalid-token'}):
            headers = {
                'Authorization': 'token invalid-token',
                'Accept': 'application/vnd.github.v3+json'
            }
            response = requests.get('https://api.github.com/user', headers=headers)
            assert response.status_code == 401
    
    def test_github_token_valid(self):
        """Test behavior with valid GitHub token (requires actual token)"""
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            pytest.skip("GITHUB_TOKEN not set - skipping valid token test")
        
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get('https://api.github.com/user', headers=headers)
        assert response.status_code == 200
        
        user_data = response.json()
        assert 'login' in user_data
        assert 'id' in user_data


class TestPublicRepositoryAccess:
    """Test access to public repositories (should work without token)"""
    
    @pytest.fixture
    def public_repos(self):
        """List of public repositories to test"""
        return [
            "octocat/Hello-World",
            "microsoft/vscode", 
            "facebook/react",
            "LDFLK/archives"
        ]
    
    def test_public_repo_access_without_token(self, public_repos):
        """Test that public repositories are accessible without a token"""
        headers = {'Accept': 'application/vnd.github.v3+json'}
        
        for repo in public_repos:
            response = requests.get(f'https://api.github.com/repos/{repo}', headers=headers)
            assert response.status_code == 200, f"Failed to access {repo}"
            
            repo_data = response.json()
            assert repo_data['private'] == False, f"{repo} should be public"
            assert 'name' in repo_data
            assert 'full_name' in repo_data
    
    def test_public_repo_access_with_token(self, public_repos):
        """Test that public repositories are accessible with a token"""
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            pytest.skip("GITHUB_TOKEN not set - skipping token test")
        
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        for repo in public_repos:
            response = requests.get(f'https://api.github.com/repos/{repo}', headers=headers)
            assert response.status_code == 200, f"Failed to access {repo}"
            
            repo_data = response.json()
            assert repo_data['private'] == False, f"{repo} should be public"
            assert 'name' in repo_data
            assert 'full_name' in repo_data


class TestPrivateRepositoryAccess:
    """Test access to private repositories (requires valid token)"""
    
    @pytest.fixture
    def private_repos(self):
        """List of private repositories to test"""
        return [
            "LDFLK/launch"  # Your private repository
        ]
    
    def test_private_repo_access_without_token(self, private_repos):
        """Test that private repositories are NOT accessible without a token"""
        headers = {'Accept': 'application/vnd.github.v3+json'}
        
        for repo in private_repos:
            response = requests.get(f'https://api.github.com/repos/{repo}', headers=headers)
            # Should return 404 for private repos without token
            assert response.status_code in [404, 401], f"Unexpected response for {repo}"
    
    def test_private_repo_access_with_token(self, private_repos):
        """Test that private repositories are accessible with a valid token"""
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            pytest.skip("GITHUB_TOKEN not set - cannot test private repository access")
        
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        for repo in private_repos:
            response = requests.get(f'https://api.github.com/repos/{repo}', headers=headers)
            assert response.status_code == 200, f"Failed to access private repo {repo}"
            
            repo_data = response.json()
            assert repo_data['private'] == True, f"{repo} should be private"
            assert 'name' in repo_data
            assert 'full_name' in repo_data
    
    def test_private_repo_access_with_invalid_token(self, private_repos):
        """Test that private repositories are NOT accessible with invalid token"""
        headers = {
            'Authorization': 'token invalid-token',
            'Accept': 'application/vnd.github.v3+json'
        }
        
        for repo in private_repos:
            response = requests.get(f'https://api.github.com/repos/{repo}', headers=headers)
            assert response.status_code in [401, 404], f"Unexpected response for {repo}"


class TestGitHubAPIRateLimiting:
    """Test GitHub API rate limiting behavior"""
    
    def test_rate_limit_headers_present(self):
        """Test that rate limit headers are present in API responses"""
        headers = {'Accept': 'application/vnd.github.v3+json'}
        response = requests.get('https://api.github.com/repos/octocat/Hello-World', headers=headers)
        
        # Check for rate limit headers
        assert 'X-RateLimit-Limit' in response.headers
        assert 'X-RateLimit-Remaining' in response.headers
        assert 'X-RateLimit-Reset' in response.headers
    
    def test_rate_limit_with_token(self):
        """Test rate limiting with authenticated requests"""
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            pytest.skip("GITHUB_TOKEN not set - skipping authenticated rate limit test")
        
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get('https://api.github.com/repos/octocat/Hello-World', headers=headers)
        
        # Authenticated requests have higher rate limits
        assert 'X-RateLimit-Limit' in response.headers
        limit = int(response.headers['X-RateLimit-Limit'])
        assert limit >= 5000  # Authenticated requests have 5000+ requests per hour


class TestRepositoryIssuesAccess:
    """Test access to repository issues"""
    
    def test_public_repo_issues_without_token(self):
        """Test accessing issues from public repository without token"""
        headers = {'Accept': 'application/vnd.github.v3+json'}
        response = requests.get('https://api.github.com/repos/octocat/Hello-World/issues', headers=headers)
        assert response.status_code == 200
    
    def test_public_repo_issues_with_token(self):
        """Test accessing issues from public repository with token"""
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            pytest.skip("GITHUB_TOKEN not set - skipping token test")
        
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get('https://api.github.com/repos/octocat/Hello-World/issues', headers=headers)
        assert response.status_code == 200
    
    def test_private_repo_issues_with_token(self):
        """Test accessing issues from private repository with token"""
        token = os.getenv('GITHUB_TOKEN')
        if not token:
            pytest.skip("GITHUB_TOKEN not set - cannot test private repository issues")
        
        headers = {
            'Authorization': f'token {token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        response = requests.get('https://api.github.com/repos/LDFLK/launch/issues', headers=headers)
        assert response.status_code == 200


# Utility functions for testing
def get_github_token():
    """Get GitHub token from environment"""
    return os.getenv('GITHUB_TOKEN')


def has_github_token():
    """Check if GitHub token is available"""
    return bool(get_github_token())


def requires_github_token():
    """Decorator to skip tests that require GitHub token"""
    return pytest.mark.skipif(
        not has_github_token(),
        reason="GITHUB_TOKEN not set"
    )
