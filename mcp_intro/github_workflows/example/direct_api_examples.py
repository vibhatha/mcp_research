#!/usr/bin/env python3
"""
Direct API examples for GitHub MCP EPIC tools.
Demonstrates how to use the GitHubIssueCrawler directly for advanced use cases.
"""

from base_example import BaseExample
from github_mcp.tools.github_tools import GitHubIssueCrawler


class DirectAPIExamples(BaseExample):
    """Examples for using the GitHubIssueCrawler directly"""
    
    def run(self):
        """Run all direct API examples"""
        self.print_header("🔧 GitHub MCP EPIC Direct API Examples")
        
        # Setup GitHub token
        if not self.setup_github_token():
            print("\n⚠️  Some examples may not work without a GitHub token")
            print("   Set GITHUB_TOKEN environment variable to enable full functionality")
        
        # Run examples
        self.example_github_issue_crawler()
        self.example_custom_epic_extraction()
        self.example_issue_analysis()
        self.example_comment_filtering()
    
    def example_github_issue_crawler(self):
        """Example: Using GitHubIssueCrawler directly"""
        self.print_header("EXAMPLE 1: Using GitHubIssueCrawler Directly")
        
        try:
            # Create crawler instance
            crawler = GitHubIssueCrawler()
            
            # Get issues from the repository
            issues = crawler.get_issues(self.repo_name, state="open")
            print(f"📋 Found {len(issues)} open issues")
            
            # Get comments from the first issue (if any)
            if issues:
                first_issue = issues[0]
                print(f"🔍 Analyzing issue #{first_issue['number']}: {first_issue['title']}")
                
                comments = crawler.get_issue_comments(self.repo_name, first_issue['number'])
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
                        print(f"   Date: {parsed_data.date}")
                        print(f"   What happened: {len(parsed_data.what_happened)} items")
                        print(f"   Risks/Blockers: {len(parsed_data.risks_blockers)} items")
                        print(f"   Next steps: {len(parsed_data.next_steps)} items")
            
        except Exception as e:
            print(f"❌ Error using GitHubIssueCrawler: {e}")
    
    def example_custom_epic_extraction(self):
        """Example: Custom EPIC extraction with filtering"""
        self.print_header("EXAMPLE 2: Custom EPIC Extraction with Filtering")
        
        try:
            crawler = GitHubIssueCrawler()
            
            # Get issues from the last 30 days
            issues = crawler.get_issues(self.repo_name, state="open")
            print(f"📋 Found {len(issues)} open issues")
            
            # Custom filtering logic
            epic_updates = []
            for issue in issues[:5]:  # Limit to first 5 issues for demo
                print(f"\n🔍 Checking issue #{issue['number']}: {issue['title']}")
                
                comments = crawler.get_issue_comments(self.repo_name, issue['number'])
                
                for comment in comments:
                    if crawler.is_epic_update_comment(comment['body']):
                        parsed_data = crawler.parse_epic_template(comment['body'])
                        
                        if parsed_data:
                            # Custom filtering: only include "On Track" or "At Risk" epics
                            if parsed_data.status in ["On Track", "At Risk"]:
                                epic_updates.append({
                                    'issue_number': issue['number'],
                                    'issue_title': issue['title'],
                                    'epic_name': parsed_data.epic_name,
                                    'status': parsed_data.status,
                                    'progress': parsed_data.progress,
                                    'owner': parsed_data.owner,
                                    'date': parsed_data.date
                                })
                                print(f"   ✅ Found EPIC update: {parsed_data.epic_name} ({parsed_data.status})")
            
            print(f"\n📊 Summary: Found {len(epic_updates)} filtered EPIC updates")
            for update in epic_updates:
                print(f"   - #{update['issue_number']}: {update['epic_name']} ({update['status']})")
            
        except Exception as e:
            print(f"❌ Error in custom EPIC extraction: {e}")
    
    def example_issue_analysis(self):
        """Example: Detailed issue analysis"""
        self.print_header("EXAMPLE 3: Detailed Issue Analysis")
        
        try:
            crawler = GitHubIssueCrawler()
            
            # Get a specific issue for detailed analysis
            issue_number = 1  # Example issue number
            issue = crawler.get_issue(self.repo_name, issue_number)
            
            if issue:
                print(f"📋 Issue Analysis for #{issue['number']}")
                print(f"   Title: {issue['title']}")
                print(f"   State: {issue['state']}")
                print(f"   Created: {issue['created_at']}")
                print(f"   Updated: {issue['updated_at']}")
                print(f"   Author: {issue['user']['login']}")
                
                # Get all comments
                comments = crawler.get_issue_comments(self.repo_name, issue_number)
                print(f"   Comments: {len(comments)}")
                
                # Analyze comment types
                epic_comments = []
                regular_comments = []
                
                for comment in comments:
                    if crawler.is_epic_update_comment(comment['body']):
                        epic_comments.append(comment)
                    else:
                        regular_comments.append(comment)
                
                print(f"   EPIC updates: {len(epic_comments)}")
                print(f"   Regular comments: {len(regular_comments)}")
                
                # Show recent activity
                if comments:
                    print(f"\n📅 Recent Activity:")
                    for comment in comments[-3:]:  # Last 3 comments
                        comment_type = "🚀 EPIC Update" if crawler.is_epic_update_comment(comment['body']) else "💬 Comment"
                        print(f"   {comment_type} by {comment['user']['login']} on {comment['created_at'][:10]}")
            else:
                print(f"❌ Issue #{issue_number} not found")
            
        except Exception as e:
            print(f"❌ Error in issue analysis: {e}")
    
    def example_comment_filtering(self):
        """Example: Advanced comment filtering"""
        self.print_header("EXAMPLE 4: Advanced Comment Filtering")
        
        try:
            crawler = GitHubIssueCrawler()
            
            # Get issues and analyze comment patterns
            issues = crawler.get_issues(self.repo_name, state="open")
            print(f"📋 Analyzing {len(issues)} open issues")
            
            # Statistics
            total_comments = 0
            total_epic_updates = 0
            epic_authors = set()
            epic_statuses = {}
            
            for issue in issues[:10]:  # Limit for demo
                comments = crawler.get_issue_comments(self.repo_name, issue['number'])
                total_comments += len(comments)
                
                for comment in comments:
                    if crawler.is_epic_update_comment(comment['body']):
                        total_epic_updates += 1
                        epic_authors.add(comment['user']['login'])
                        
                        parsed_data = crawler.parse_epic_template(comment['body'])
                        if parsed_data:
                            status = parsed_data.status
                            epic_statuses[status] = epic_statuses.get(status, 0) + 1
            
            # Print statistics
            print(f"\n📊 Comment Analysis Summary:")
            print(f"   Total comments analyzed: {total_comments}")
            print(f"   EPIC updates found: {total_epic_updates}")
            print(f"   EPIC update authors: {len(epic_authors)}")
            print(f"   Authors: {', '.join(sorted(epic_authors))}")
            
            print(f"\n📈 EPIC Status Distribution:")
            for status, count in epic_statuses.items():
                print(f"   {status}: {count}")
            
        except Exception as e:
            print(f"❌ Error in comment filtering: {e}")
    
    def example_bulk_processing(self):
        """Example: Bulk processing of multiple repositories"""
        self.print_header("EXAMPLE 5: Bulk Processing Multiple Repositories")
        
        try:
            crawler = GitHubIssueCrawler()
            
            # Example repositories to process
            repositories = [
                self.repo_name,
                "octocat/Hello-World",
                # Add more repositories as needed
            ]
            
            all_epic_updates = []
            
            for repo in repositories:
                print(f"\n🔍 Processing repository: {repo}")
                
                try:
                    # Get issues from the repository
                    issues = crawler.get_issues(repo, state="open")
                    print(f"   Found {len(issues)} open issues")
                    
                    repo_epic_updates = 0
                    
                    for issue in issues[:5]:  # Limit per repo for demo
                        comments = crawler.get_issue_comments(repo, issue['number'])
                        
                        for comment in comments:
                            if crawler.is_epic_update_comment(comment['body']):
                                repo_epic_updates += 1
                                all_epic_updates.append({
                                    'repo': repo,
                                    'issue_number': issue['number'],
                                    'issue_title': issue['title'],
                                    'author': comment['user']['login'],
                                    'created_at': comment['created_at']
                                })
                    
                    print(f"   Found {repo_epic_updates} EPIC updates")
                    
                except Exception as e:
                    print(f"   ❌ Error processing {repo}: {e}")
            
            print(f"\n📊 Bulk Processing Summary:")
            print(f"   Total EPIC updates across all repositories: {len(all_epic_updates)}")
            
            # Group by repository
            repo_stats = {}
            for update in all_epic_updates:
                repo = update['repo']
                repo_stats[repo] = repo_stats.get(repo, 0) + 1
            
            for repo, count in repo_stats.items():
                print(f"   {repo}: {count} EPIC updates")
            
        except Exception as e:
            print(f"❌ Error in bulk processing: {e}")


if __name__ == "__main__":
    # Run direct API examples
    api_examples = DirectAPIExamples()
    api_examples.run()
