#!/usr/bin/env python3
"""
Example script demonstrating how to use the GitHub MCP API with a public repository.
This script shows how to test the functionality without needing access to private repos.
"""

import os
import json
from datetime import datetime, timedelta

# Import the GitHub MCP tools
from github_mcp.tools.github_tools import (
    GitHubIssueCrawler,
    crawl_epic_updates,
    get_epic_updates_from_issue,
    generate_board_report,
    generate_epic_status_summary,
    analyze_epic_trends,
    process_dated_epic_update
)

# Configuration - Using a public repository for testing
PUBLIC_REPO_NAME = "LDFLK/archives"  # Well-known public repository
PUBLIC_ISSUE_URL = "https://github.com/LDFLK/archives/issues/1"  # Example issue
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

def setup_github_token():
    """Set up GitHub token for API access"""
    if not GITHUB_TOKEN:
        print("⚠️  Warning: GITHUB_TOKEN environment variable not set")
        print("   Set it with: export GITHUB_TOKEN='your-github-token'")
        print("   Or set it in the script: os.environ['GITHUB_TOKEN'] = 'your-token'")
        print("\n💡 To create a GitHub token:")
        print("   1. Go to GitHub.com → Settings → Developer settings → Personal access tokens")
        print("   2. Generate new token (classic)")
        print("   3. Select scopes: repo, read:org, read:user")
        print("   4. Copy the token and set: export GITHUB_TOKEN='your-token'")
        print("\n💡 Note: For public repositories, you can use a token with minimal permissions")
        return False
    
    os.environ['GITHUB_TOKEN'] = GITHUB_TOKEN
    print("✅ GitHub token configured")
    return True

def test_public_repository_access():
    """Test access to the public repository"""
    print("\n" + "="*60)
    print("TESTING: Public Repository Access")
    print("="*60)
    
    try:
        crawler = GitHubIssueCrawler()
        
        # Test getting issues from the public repository
        print(f"🔍 Testing access to {PUBLIC_REPO_NAME}...")
        issues = crawler.get_issues(PUBLIC_REPO_NAME, state="open", since="2024-01-01")
        
        print(f"✅ Successfully accessed {PUBLIC_REPO_NAME}")
        print(f"📊 Found {len(issues)} open issues since 2024-01-01")
        
        if issues:
            print(f"📝 Sample issue: #{issues[0]['number']} - {issues[0]['title'][:50]}...")
        
        return True
        
    except Exception as e:
        print(f"❌ Error accessing public repository: {e}")
        return False

def example_crawl_public_repository():
    """Example: Crawl issues from a public repository"""
    print("\n" + "="*60)
    print("EXAMPLE: Crawling Issues from Public Repository")
    print("="*60)
    
    try:
        # Note: This will look for EPIC updates, which might not exist in this repo
        # but it will test the basic functionality
        result = crawl_epic_updates(
            repo=PUBLIC_REPO_NAME,
            start_date="2024-01-01"
        )
        
        if isinstance(result, str):
            print(f"📊 Result: {result}")
            return None
        
        if isinstance(result, dict):
            print(f"📊 Found {result.get('total_updates', 0)} EPIC updates")
            print(f"📁 Repository: {result.get('repo', 'N/A')}")
            print(f"📅 Period: Since {result.get('start_date', 'N/A')}")
            
            # Display each update
            updates = result.get('updates', [])
            for i, update in enumerate(updates, 1):
                print(f"\n📝 Update {i}:")
                print(f"   Issue: #{update.get('issue_number', 'N/A')} - {update.get('issue_title', 'N/A')}")
                print(f"   Author: {update.get('author', 'N/A')}")
                print(f"   Date: {update.get('created_at', 'N/A')}")
            
            return result
        else:
            print(f"📊 Unexpected result type: {type(result)}")
            return None
        
    except Exception as e:
        print(f"❌ Error crawling public repository: {e}")
        return None

def example_get_issue_comments():
    """Example: Get comments from a specific issue"""
    print("\n" + "="*60)
    print("EXAMPLE: Getting Comments from Specific Issue")
    print("="*60)
    
    try:
        crawler = GitHubIssueCrawler()
        
        # Get comments from a specific issue
        issue_number = 1  # Use issue #1 as an example
        comments = crawler.get_issue_comments(PUBLIC_REPO_NAME, issue_number)
        
        print(f"📊 Found {len(comments)} comments in issue #{issue_number}")
        
        if comments:
            print(f"💬 Sample comment by {comments[0]['user']['login']}:")
            print(f"   {comments[0]['body'][:100]}...")
        
        return comments
        
    except Exception as e:
        print(f"❌ Error getting issue comments: {e}")
        return None

def example_github_issue_crawler_direct():
    """Example: Using GitHubIssueCrawler directly with public repo"""
    print("\n" + "="*60)
    print("EXAMPLE: Using GitHubIssueCrawler Directly")
    print("="*60)
    
    try:
        # Create crawler instance
        crawler = GitHubIssueCrawler()
        
        # Get issues from the public repository
        issues = crawler.get_issues(PUBLIC_REPO_NAME, state="open", since="2024-01-01")
        print(f"📋 Found {len(issues)} open issues since 2024-01-01")
        
        # Get comments from the first issue (if any)
        if issues:
            first_issue = issues[0]
            print(f"🔍 Analyzing issue #{first_issue['number']}: {first_issue['title'][:50]}...")
            
            comments = crawler.get_issue_comments(PUBLIC_REPO_NAME, first_issue['number'])
            print(f"💬 Found {len(comments)} comments")
            
            # Check for EPIC updates (unlikely in this repo, but good for testing)
            epic_comments = []
            for comment in comments:
                if crawler.is_epic_update_comment(comment['body']):
                    epic_comments.append(comment)
            
            print(f"🚀 Found {len(epic_comments)} EPIC update comments")
            
            # Show sample comment structure
            if comments:
                print(f"\n📝 Sample comment structure:")
                sample_comment = comments[0]
                print(f"   ID: {sample_comment['id']}")
                print(f"   Author: {sample_comment['user']['login']}")
                print(f"   Created: {sample_comment['created_at']}")
                print(f"   Body length: {len(sample_comment['body'])} characters")
        
    except Exception as e:
        print(f"❌ Error using GitHubIssueCrawler: {e}")

def main():
    """Main function to run all examples with public repository"""
    print("🚀 GitHub MCP Public Repository Example")
    print("=" * 60)
    
    # Setup GitHub token
    if not setup_github_token():
        print("\n⚠️  Some examples may not work without a GitHub token")
        print("   Set GITHUB_TOKEN environment variable to enable full functionality")
    
    # Test public repository access
    if test_public_repository_access():
        # Run examples
        example_crawl_public_repository()
        example_get_issue_comments()
        example_github_issue_crawler_direct()
        
        print("\n" + "="*60)
        print("✅ All examples completed!")
        print("="*60)
        print("\n💡 Tips:")
        print("   - This example uses a public repository for testing")
        print("   - EPIC updates are unlikely to exist in this repo")
        print("   - The main goal is to test API connectivity")
        print("   - For real EPIC updates, use your own repository")
        print("   - Make sure your repository has issues with EPIC update comments")
    else:
        print("\n❌ Cannot proceed without repository access")
        print("   Please check your GitHub token and try again")

if __name__ == "__main__":
    main() 