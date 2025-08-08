#!/usr/bin/env python3
"""
Test cases for GitHub EPIC tools
"""

import json
import os
import sys
from datetime import datetime, timedelta
from unittest.mock import Mock, patch, MagicMock
import pytest

# Add the current directory to the path so we can import our modules
sys.path.insert(0, os.path.dirname(os.path.abspath(__file__)))

from github_mcp.tools.github_tools import (
    GitHubIssueCrawler, 
    EpicUpdate, 
    ParsedEpicData,
    crawl_epic_updates,
    get_epic_updates_from_issue,
    process_dated_epic_update,
    generate_board_report,
    generate_epic_status_summary,
    analyze_epic_trends
)

@pytest.fixture
def sample_epic_template():
    """Sample EPIC update template content"""
    return """<!-- epic-update-template -->
## 🚀 Epic Update

**Date:** 2025-01-15
**Owner:** @test-user
**Epic:** Test Epic Implementation

### Status
- **Current status:** _On Track_
- **Progress (%):** 75%

### What happened since last update
- Completed user authentication module
- Integrated payment gateway
- Fixed critical bug in data processing

### Scope changes
- Added additional validation requirements
- Extended API endpoints for mobile app

### Risks / blockers
- Third-party API rate limiting
- Database migration complexity

### Next steps (with owners & dates)
- Complete UI testing by @qa-team (2025-01-20)
- Deploy to staging by @devops (2025-01-22)
- Final review by @product-manager (2025-01-25)

### Metrics / deliverables
- 95% test coverage achieved
- Performance improved by 40%
- User satisfaction score: 4.8/5

---

> _Generated automatically because you typed `@epic-update`_"""

@pytest.fixture
def sample_github_data():
    """Sample GitHub API responses"""
    return {
        'issue': {
            'number': 151,
            'title': 'Implement User Authentication System',
            'state': 'open',
            'created_at': '2025-06-29T10:00:00Z'
        },
        'comment': {
            'id': 12345,
            'body': None,  # Will be set by individual tests
            'user': {'login': 'test-user'},
            'created_at': '2025-07-15T14:30:00Z'  # Changed to a recent date
        }
    }

@pytest.fixture
def github_token():
    """Mock GitHub token"""
    os.environ['GITHUB_TOKEN'] = 'test-token'
    yield 'test-token'
    # Clean up
    if 'GITHUB_TOKEN' in os.environ:
        del os.environ['GITHUB_TOKEN']

class TestGitHubEpicTools:
    """Test cases for GitHub EPIC tools"""
    
    def test_epic_template_detection(self, sample_epic_template, github_token):
        """Test EPIC template detection"""
        crawler = GitHubIssueCrawler()
        
        # Test valid EPIC template
        assert crawler.is_epic_update_comment(sample_epic_template) == True
        
        # Test invalid content
        invalid_content = "This is just a regular comment without EPIC update"
        assert crawler.is_epic_update_comment(invalid_content) == False
        
        # Test with @epic-update trigger
        trigger_content = "Some content\n@epic-update\nMore content"
        assert crawler.is_epic_update_comment(trigger_content) == True

    def test_epic_template_parsing(self, sample_epic_template, github_token):
        """Test EPIC template parsing"""
        crawler = GitHubIssueCrawler()
        parsed = crawler.parse_epic_template(sample_epic_template)
        
        assert parsed is not None
        assert parsed.date == "2025-01-15"
        assert parsed.owner == "@test-user"
        assert parsed.epic_name == "Test Epic Implementation"
        assert parsed.status == "On Track"
        assert parsed.progress == "75%"
        
        # Test list sections
        assert len(parsed.what_happened) == 3
        assert "Completed user authentication module" in parsed.what_happened
        assert len(parsed.risks_blockers) == 2
        assert "Third-party API rate limiting" in parsed.risks_blockers
        assert len(parsed.next_steps) == 3
        assert "Complete UI testing by @qa-team (2025-01-20)" in parsed.next_steps

    def test_epic_template_parsing_edge_cases(self, github_token):
        """Test EPIC template parsing with edge cases"""
        crawler = GitHubIssueCrawler()
        
        # Test with missing sections
        minimal_template = """<!-- epic-update-template -->
## 🚀 Epic Update

**Date:** 2025-01-15
**Owner:** @test-user
**Epic:** Minimal Epic

### Status
- **Current status:** _At Risk_
- **Progress (%):** 50%

### What happened since last update
- Basic implementation completed

---

> _Generated automatically because you typed `@epic-update`_"""
        
        parsed = crawler.parse_epic_template(minimal_template)
        assert parsed is not None
        assert parsed.status == "At Risk"
        assert parsed.progress == "50%"
        assert len(parsed.what_happened) == 1
        assert len(parsed.risks_blockers) == 0  # Missing section

    @patch('github_mcp.tools.github_tools.requests.get')
    def test_get_issues(self, mock_get, sample_github_data, github_token):
        """Test getting issues from GitHub API"""
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = [sample_github_data['issue']]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        crawler = GitHubIssueCrawler()
        issues = crawler.get_issues("test-org/test-repo")
        
        assert len(issues) == 1
        assert issues[0]['number'] == 151
        assert issues[0]['title'] == 'Implement User Authentication System'

    @patch('github_mcp.tools.github_tools.requests.get')
    def test_get_issue_comments(self, mock_get, sample_github_data, sample_epic_template, github_token):
        """Test getting issue comments from GitHub API"""
        # Set the comment body
        sample_github_data['comment']['body'] = sample_epic_template
        
        # Mock successful response
        mock_response = Mock()
        mock_response.json.return_value = [sample_github_data['comment']]
        mock_response.raise_for_status.return_value = None
        mock_get.return_value = mock_response
        
        crawler = GitHubIssueCrawler()
        comments = crawler.get_issue_comments("test-org/test-repo", 151)
        
        assert len(comments) == 1
        assert comments[0]['id'] == 12345
        assert comments[0]['user']['login'] == 'test-user'

    @patch('github_mcp.tools.github_tools.requests.get')
    def test_extract_epic_updates(self, mock_get, sample_github_data, sample_epic_template, github_token):
        """Test extracting EPIC updates from issues"""
        # Set the comment body
        sample_github_data['comment']['body'] = sample_epic_template
        
        # Mock responses for both issues and comments
        mock_issues_response = Mock()
        mock_issues_response.json.return_value = [sample_github_data['issue']]
        mock_issues_response.raise_for_status.return_value = None
        
        mock_comments_response = Mock()
        mock_comments_response.json.return_value = [sample_github_data['comment']]
        mock_comments_response.raise_for_status.return_value = None
        
        # Configure mock to return different responses for different URLs
        def mock_get_side_effect(url, **kwargs):
            if 'issues' in url and '/comments' not in url:
                return mock_issues_response
            elif '/comments' in url:
                return mock_comments_response
            return mock_issues_response
        
        mock_get.side_effect = mock_get_side_effect
        
        crawler = GitHubIssueCrawler()
        
        # Mock the instance methods directly
        crawler.is_epic_update_comment = Mock(return_value=True)
        
        # Create a mock parsed data
        mock_parsed = Mock()
        mock_parsed.status = "On Track"
        crawler.parse_epic_template = Mock(return_value=mock_parsed)
        # https://github.com/LDFLK/launch/issues/151
        epic_updates = crawler.extract_epic_updates("test-org/test-repo", days_back=30)
        
        assert len(epic_updates) == 1
        assert epic_updates[0].issue_number == 151
        assert epic_updates[0].author == "test-user"
        assert epic_updates[0].parsed_data is not None
        assert epic_updates[0].parsed_data.status == "On Track"

    def test_crawl_epic_updates_with_date_range(self, sample_epic_template, github_token):
        """Test crawling EPIC updates with specific date range"""
        with patch('github_mcp.tools.github_tools.GitHubIssueCrawler') as mock_crawler_class:
            mock_crawler = Mock()
            mock_crawler_class.return_value = mock_crawler
            
            # Create a mock EpicUpdate
            mock_epic_update = EpicUpdate(
                issue_number=151,
                issue_title="Test Issue",
                comment_id=12345,
                comment_body=sample_epic_template,
                author="test-user",
                created_at="2025-01-15T14:30:00Z",
                repo="test-org/test-repo",
                parsed_data=Mock()
            )
            
            mock_crawler.extract_epic_updates.return_value = [mock_epic_update]
            
            result = crawl_epic_updates(
                "test-org/test-repo", 
                start_date="2025-01-15", 
                end_date="2025-01-15"
            )
            
            # Verify the result structure
            assert isinstance(result, dict)
            assert result['total_updates'] == 1
            assert result['repo'] == "test-org/test-repo"
            assert len(result['updates']) == 1

    def test_crawl_epic_updates_with_issue_numbers(self, sample_epic_template, github_token):
        """Test crawling EPIC updates with specific issue numbers"""
        with patch('github_mcp.tools.github_tools.GitHubIssueCrawler') as mock_crawler_class:
            mock_crawler = Mock()
            mock_crawler_class.return_value = mock_crawler
            
            # Create a mock EpicUpdate
            mock_epic_update = EpicUpdate(
                issue_number=151,
                issue_title="Test Issue",
                comment_id=12345,
                comment_body=sample_epic_template,
                author="test-user",
                created_at="2025-01-15T14:30:00Z",
                repo="test-org/test-repo",
                parsed_data=Mock()
            )
            
            mock_crawler.extract_epic_updates.return_value = [mock_epic_update]
            
            result = crawl_epic_updates(
                "test-org/test-repo", 
                issue_numbers="151,152,153"
            )
            
            # Verify the result structure
            assert isinstance(result, dict)
            assert result['total_updates'] == 1
            assert result['repo'] == "test-org/test-repo"
            assert len(result['updates']) == 1

    def test_crawl_specific_issues(self, sample_epic_template, github_token):
        """Test crawling specific issues function"""
        with patch('github_mcp.tools.github_tools.GitHubIssueCrawler') as mock_crawler_class:
            mock_crawler = Mock()
            mock_crawler_class.return_value = mock_crawler
            
            # Create a mock EpicUpdate
            mock_epic_update = EpicUpdate(
                issue_number=151,
                issue_title="Test Issue",
                comment_id=12345,
                comment_body=sample_epic_template,
                author="test-user",
                created_at="2025-01-15T14:30:00Z",
                repo="test-org/test-repo",
                parsed_data=Mock()
            )
            
            mock_crawler.extract_epic_updates.return_value = [mock_epic_update]
            
            # Import the function
            from github_mcp.tools.github_tools import crawl_specific_issues
            
            result = crawl_specific_issues(
                "test-org/test-repo", 
                "151,152,153"
            )
            
            # Verify the result structure
            assert isinstance(result, dict)
            assert result['total_updates'] == 1
            assert result['repo'] == "test-org/test-repo"
            assert result['issue_numbers'] == [151, 152, 153]
            assert len(result['updates']) == 1

    def test_crawl_epic_updates_invalid_issue_numbers(self, github_token):
        """Test crawling EPIC updates with invalid issue numbers"""
        result = crawl_epic_updates(
            "test-org/test-repo", 
            issue_numbers="151,invalid,153"
        )
        
        # Should return error message
        assert "Error parsing issue numbers" in result

    def test_get_epic_updates_from_issue_url(self, sample_github_data, sample_epic_template, github_token):
        """Test extracting EPIC updates from specific issue URL"""
        with patch('github_mcp.tools.github_tools.GitHubIssueCrawler') as mock_crawler_class:
            mock_crawler = Mock()
            mock_crawler_class.return_value = mock_crawler
            
            # Set the comment body
            sample_github_data['comment']['body'] = sample_epic_template
            
            # Mock the comment response
            mock_crawler.get_issue_comments.return_value = [sample_github_data['comment']]
            mock_crawler.is_epic_update_comment.return_value = True
            mock_crawler.parse_epic_template.return_value = Mock()
            
            result = get_epic_updates_from_issue(
                "https://github.com/LDFLK/launch/issues/151",
                "2025-07-15"
            )

            print(">>>> result", result)
            
            assert isinstance(result, dict)
            assert result['total_updates'] == 1
            assert result['issue_number'] == 151
            assert result['repo'] == "LDFLK/launch"
            assert result['target_date'] == "2025-07-15"

    def test_generate_board_report(self, sample_epic_template, github_token):
        """Test board report generation"""
        # Create sample EPIC data
        epic_data = {
            'total_updates': 1,
            'repo': 'test-org/test-repo',
            'days_back': 30,
            'updates': [{
                'issue_number': 151,
                'issue_title': 'Test Issue',
                'comment_id': 12345,
                'comment_body': sample_epic_template,
                'author': 'test-user',
                'created_at': '2025-01-15T14:30:00Z',
                'repo': 'test-org/test-repo',
                'parsed_data': {
                    'date': '2025-01-15',
                    'owner': '@test-user',
                    'epic_name': 'Test Epic Implementation',
                    'status': 'On Track',
                    'progress': '75%',
                    'what_happened': ['Completed user authentication module'],
                    'risks_blockers': ['Third-party API rate limiting'],
                    'next_steps': ['Complete UI testing by @qa-team (2025-01-20)']
                }
            }]
        }
        
        # Test executive format
        report = generate_board_report(epic_data, "executive")
        assert "EPIC Update Report" in report
        assert "Issue #151" in report
        assert "On Track" in report
        assert "75%" in report
        
        # Test summary format
        summary = generate_board_report(epic_data, "summary")
        assert "Executive Summary" in summary
        assert "**Total EPIC Updates:** 1" in summary

    def test_generate_epic_status_summary(self, github_token):
        """Test EPIC status summary generation"""
        # Create sample EPIC data with multiple updates
        epic_data = {
            'total_updates': 2,
            'repo': 'test-org/test-repo',
            'days_back': 30,
            'updates': [
                {
                    'issue_number': 151,
                    'parsed_data': {
                        'epic_name': 'Epic 1',
                        'status': 'On Track',
                        'progress': '75%',
                        'owner': '@user1',
                        'risks_blockers': ['Risk 1'],
                        'scope_changes': ['Change 1']
                    }
                },
                {
                    'issue_number': 152,
                    'parsed_data': {
                        'epic_name': 'Epic 2',
                        'status': 'At Risk',
                        'progress': '50%',
                        'owner': '@user2',
                        'risks_blockers': ['Risk 2'],
                        'scope_changes': []
                    }
                }
            ]
        }
        
        summary = generate_epic_status_summary(epic_data)
        assert "EPIC Status Summary" in summary
        assert "Status Breakdown" in summary
        assert "**On Track:** 1 epics" in summary
        assert "**At Risk:** 1 epics" in summary

    def test_analyze_epic_trends(self, github_token):
        """Test EPIC trends analysis"""
        # Create sample EPIC data
        epic_data = {
            'total_updates': 3,
            'repo': 'test-org/test-repo',
            'days_back': 30,
            'updates': [
                {
                    'issue_number': 151,
                    'issue_title': 'Test Issue 1',
                    'author': 'user1',
                    'created_at': '2025-01-15T14:30:00Z'
                },
                {
                    'issue_number': 151,
                    'issue_title': 'Test Issue 1',
                    'author': 'user1',
                    'created_at': '2025-01-16T14:30:00Z'
                },
                {
                    'issue_number': 152,
                    'issue_title': 'Test Issue 2',
                    'author': 'user2',
                    'created_at': '2025-01-17T14:30:00Z'
                }
            ]
        }
        
        analysis = analyze_epic_trends(epic_data)
        assert "EPIC Updates Trend Analysis" in analysis
        assert "Key Metrics" in analysis
        assert "Top Contributors" in analysis
        assert "**@user1:** 2 updates" in analysis

    def test_process_dated_epic_update(self, github_token):
        """Test processing specific dated EPIC update"""
        with patch('github_mcp.tools.github_tools.get_epic_updates_from_issue') as mock_get:
            mock_get.return_value = {
                'total_updates': 1,
                'repo': 'test-org/test-repo',
                'days_back': 30,
                'updates': [{
                    'issue_number': 151, 
                    'issue_title': 'Test Issue',
                    'comment_id': 12345,
                    'comment_body': 'Test comment body',
                    'author': 'test-user',
                    'created_at': '2025-07-15T14:30:00Z',
                    'repo': 'test-org/test-repo',
                    'parsed_data': {
                        'date': '2025-07-15',
                        'owner': '@test-user',
                        'epic_name': 'Test Epic',
                        'status': 'On Track',
                        'progress': '75%',
                        'what_happened': ['Test progress'],
                        'risks_blockers': [],
                        'next_steps': []
                    }
                }]
            }
            
            result = process_dated_epic_update(
                "https://github.com/LDFLK/launch/issues/151",
                "2025-07-28",
                "board_report"
            )

            print(">>>> result", result)
            
            assert "EPIC Update Report" in result

    def test_error_handling(self):
        """Test error handling in various scenarios"""
        # Test that GitHubIssueCrawler can be created without token (for public repos)
        with patch.dict(os.environ, {}, clear=True):
            crawler = GitHubIssueCrawler()
            assert crawler.token is None
            assert 'Authorization' not in crawler.headers
        
        # Test invalid issue URL
        result = get_epic_updates_from_issue("invalid-url", "2025-01-15")
        assert "Invalid GitHub issue URL format" in result
        
        # Test empty EPIC data
        result = generate_board_report({'updates': []}, "executive")
        assert "No EPIC updates found" in result 