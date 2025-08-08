#!/usr/bin/env python3
"""
Example script demonstrating how to use the GitHub MCP API to generate EPIC updates.
This script shows various ways to interact with GitHub EPIC updates using the github_mcp package.
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

# Configuration
GITHUB_URL = "https://github.com/LDFLK/launch/issues/151"
REPO_NAME = "LDFLK/launch"  # Change this to your own repository
GITHUB_TOKEN = os.getenv('GITHUB_TOKEN')

# Alternative repositories for testing:
# REPO_NAME = "your-username/your-repo"  # Your own repository
# REPO_NAME = "microsoft/vscode"  # Public repository for testing

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
        return False
    
    os.environ['GITHUB_TOKEN'] = GITHUB_TOKEN
    print("✅ GitHub token configured")
    return True

def example_crawl_epic_updates():
    """Example: Crawl EPIC updates from a repository"""
    print("\n" + "="*60)
    print("EXAMPLE 1: Crawling EPIC Updates from Repository")
    print("="*60)
    
    try:
        # Crawl EPIC updates from the last 30 days
        result = crawl_epic_updates(
            repo=REPO_NAME,
            start_date="2024-01-01"  # Use a realistic date in the past
        )
        
        # Handle the result - it might be a string (error) or dict
        if isinstance(result, str):
            print(f"📊 Result: {result}")
            return None
        
        # If result is a dictionary, it should have the expected structure
        if isinstance(result, dict):
            print(f"📊 Found {result.get('total_updates', 0)} EPIC updates")
            print(f"📁 Repository: {result.get('repo', 'N/A')}")
            print(f"📅 Period: Last {result.get('days_back', 0)} days")
            
            # Display each update
            updates = result.get('updates', [])
            for i, update in enumerate(updates, 1):
                print(f"\n📝 Update {i}:")
                print(f"   Issue: #{update.get('issue_number', 'N/A')} - {update.get('issue_title', 'N/A')}")
                print(f"   Author: {update.get('author', 'N/A')}")
                print(f"   Date: {update.get('created_at', 'N/A')}")
                
                parsed_data = update.get('parsed_data', {})
                if parsed_data:
                    print(f"   Epic: {parsed_data.get('epic_name', 'N/A')}")
                    print(f"   Status: {parsed_data.get('status', 'N/A')}")
                    print(f"   Progress: {parsed_data.get('progress', 'N/A')}")
            
            return result
        else:
            print(f"📊 Unexpected result type: {type(result)}")
            print(f"📊 Result: {result}")
            return None
        
    except Exception as e:
        print(f"❌ Error crawling EPIC updates: {e}")
        return None

def example_crawl_specific_issues():
    """Example: Crawl EPIC updates from specific issue numbers"""
    print("\n" + "="*60)
    print("EXAMPLE 1b: Crawling EPIC Updates from Specific Issues")
    print("="*60)
    
    try:
        # Import the new function
        from github_mcp.tools.github_tools import crawl_specific_issues
        
        # Crawl EPIC updates from specific issue numbers
        result = crawl_specific_issues(
            repo=REPO_NAME,
            issue_numbers="181,144,150"  # Example issue numbers
        )
        
        # Handle the result
        if isinstance(result, str):
            print(f"📊 Result: {result}")
            return None
        
        if isinstance(result, dict):
            print(f"📊 Found {result.get('total_updates', 0)} EPIC updates")
            print(f"📁 Repository: {result.get('repo', 'N/A')}")
            print(f"🔢 Issues checked: {result.get('issue_numbers', [])}")
            
            # Display each update
            updates = result.get('updates', [])
            for i, update in enumerate(updates, 1):
                print(f"\n📝 Update {i}:")
                print(f"   Issue: #{update.get('issue_number', 'N/A')} - {update.get('issue_title', 'N/A')}")
                print(f"   Author: {update.get('author', 'N/A')}")
                print(f"   Date: {update.get('created_at', 'N/A')}")
                
                parsed_data = update.get('parsed_data', {})
                if parsed_data:
                    print(f"   Epic: {parsed_data.get('epic_name', 'N/A')}")
                    print(f"   Status: {parsed_data.get('status', 'N/A')}")
                    print(f"   Progress: {parsed_data.get('progress', 'N/A')}")
            
            return result
        else:
            print(f"📊 Unexpected result type: {type(result)}")
            print(f"📊 Result: {result}")
            return None
        
    except Exception as e:
        print(f"❌ Error crawling specific issues: {e}")
        return None

def example_get_epic_updates_from_issue():
    """Example: Get EPIC updates from a specific issue"""
    print("\n" + "="*60)
    print("EXAMPLE 2: Getting EPIC Updates from Specific Issue")
    print("="*60)
    
    try:
        # Get EPIC updates from the specific issue URL
        issue_data = get_epic_updates_from_issue(
            issue_url=GITHUB_URL,
            target_date="2025-07-15"  # Adjust this date as needed
        )
        
        print(f"📊 Found {issue_data['total_updates']} EPIC updates")
        print(f"🔗 Issue URL: {issue_data['issue_url']}")
        print(f"📅 Target Date: {issue_data['target_date']}")
        
        for i, update in enumerate(issue_data['updates'], 1):
            print(f"\n📝 Update {i}:")
            print(f"   Issue: #{update['issue_number']}")
            if 'parsed_data' in update and update['parsed_data']:
                parsed = update['parsed_data']
                print(f"   Epic: {parsed.get('epic_name', 'N/A')}")
                print(f"   Status: {parsed.get('status', 'N/A')}")
        
        return issue_data
        
    except Exception as e:
        print(f"❌ Error getting EPIC updates from issue: {e}")
        return None

def example_generate_board_report(epic_data):
    """Example: Generate board report from EPIC data"""
    print("\n" + "="*60)
    print("EXAMPLE 3: Generating Board Report")
    print("="*60)
    
    if not epic_data or epic_data['total_updates'] == 0:
        print("⚠️  No EPIC data available for report generation")
        return
    
    try:
        # Generate executive format report
        executive_report = generate_board_report(epic_data, "executive")
        print("📋 Executive Report:")
        print("-" * 40)
        print(executive_report)
        
        # Generate summary format report
        summary_report = generate_board_report(epic_data, "summary")
        print("\n📊 Summary Report:")
        print("-" * 40)
        print(summary_report)
        
    except Exception as e:
        print(f"❌ Error generating board report: {e}")

def example_generate_epic_status_summary(epic_data):
    """Example: Generate EPIC status summary"""
    print("\n" + "="*60)
    print("EXAMPLE 4: Generating EPIC Status Summary")
    print("="*60)
    
    if not epic_data or epic_data['total_updates'] == 0:
        print("⚠️  No EPIC data available for status summary")
        return
    
    try:
        status_summary = generate_epic_status_summary(epic_data)
        print("📈 EPIC Status Summary:")
        print("-" * 40)
        print(status_summary)
        
    except Exception as e:
        print(f"❌ Error generating status summary: {e}")

def example_analyze_epic_trends(epic_data):
    """Example: Analyze EPIC trends"""
    print("\n" + "="*60)
    print("EXAMPLE 5: Analyzing EPIC Trends")
    print("="*60)
    
    if not epic_data or epic_data['total_updates'] == 0:
        print("⚠️  No EPIC data available for trend analysis")
        return
    
    try:
        trends_analysis = analyze_epic_trends(epic_data)
        print("📊 EPIC Trends Analysis:")
        print("-" * 40)
        print(trends_analysis)
        
    except Exception as e:
        print(f"❌ Error analyzing trends: {e}")

def example_process_dated_epic_update():
    """Example: Process EPIC update for a specific date"""
    print("\n" + "="*60)
    print("EXAMPLE 6: Processing Dated EPIC Update")
    print("="*60)
    
    try:
        # Process EPIC update for a specific date and generate board report
        result = process_dated_epic_update(
            issue_url=GITHUB_URL,
            target_date="2025-07-15",  # Adjust this date as needed
            output_format="board_report"
        )
        
        print("📋 Dated EPIC Update Report:")
        print("-" * 40)
        print(result)
        
    except Exception as e:
        print(f"❌ Error processing dated EPIC update: {e}")

def example_github_issue_crawler():
    """Example: Using GitHubIssueCrawler directly"""
    print("\n" + "="*60)
    print("EXAMPLE 7: Using GitHubIssueCrawler Directly")
    print("="*60)
    
    try:
        # Create crawler instance
        crawler = GitHubIssueCrawler()
        
        # Get issues from the repository
        issues = crawler.get_issues(REPO_NAME, state="open")
        print("="*60)
        print(f"📋 Found {len(issues)} open issues\n\n")
        print("="*60)
        
        # Get comments from the first issue (if any)
        if issues:
            first_issue = issues[0]
            print(f"🔍 Analyzing issue #{first_issue['number']}: {first_issue['title']}")
            
            comments = crawler.get_issue_comments(REPO_NAME, first_issue['number'])
            print(f"💬 Found {len(comments)} comments")
            
            # Check for EPIC updates
            epic_comments = []
            for comment in comments:
                if crawler.is_epic_update_comment(comment['body']):
                    epic_comments.append(comment)
            
            print(f"🚀 Found {len(epic_comments)} EPIC update comments")
            
            # Parse the first EPIC update (if any)
            if epic_comments:
                first_epic = epic_comments[0]
                parsed_data = crawler.parse_epic_template(first_epic['body'])
                
                if parsed_data:
                    print(f"📊 Parsed EPIC Data:")
                    print(f"   Epic: {parsed_data.epic_name}")
                    print(f"   Status: {parsed_data.status}")
                    print(f"   Progress: {parsed_data.progress}")
                    print(f"   Owner: {parsed_data.owner}")
        
    except Exception as e:
        print(f"❌ Error using GitHubIssueCrawler: {e}")

def main():
    """Main function to run all examples"""
    print("🚀 GitHub MCP EPIC Updates Example")
    print("=" * 60)
    
    # Setup GitHub token
    if not setup_github_token():
        print("\n⚠️  Some examples may not work without a GitHub token")
        print("   Set GITHUB_TOKEN environment variable to enable full functionality")
    
    # Run examples
    epic_data = example_crawl_epic_updates()
    
    # Test crawling specific issues
    example_crawl_specific_issues()
    
    # example_get_epic_updates_from_issue()
    
    if epic_data:
        example_generate_board_report(epic_data)
        example_generate_epic_status_summary(epic_data)
        example_analyze_epic_trends(epic_data)
    
    example_process_dated_epic_update()
    example_github_issue_crawler()
    
    print("\n" + "="*60)
    print("✅ All examples completed!")
    print("="*60)
    print("\n💡 Tips:")
    print("   - Adjust dates in the examples to match your data")
    print("   - Set GITHUB_TOKEN for full functionality")
    print("   - Check the github_mcp.tools.github_tools module for more functions")
    print("   - Use the MCP server for integration with MCP clients")

if __name__ == "__main__":
    main()


