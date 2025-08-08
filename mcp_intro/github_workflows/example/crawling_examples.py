#!/usr/bin/env python3
"""
Crawling examples for GitHub MCP EPIC tools.
Demonstrates how to crawl repositories and specific issues for EPIC updates.
"""

from base_example import BaseExample
from github_mcp.tools.github_tools import (
    crawl_epic_updates,
    crawl_specific_issues,
    get_epic_updates_from_issue
)


class CrawlingExamples(BaseExample):
    """Examples for crawling EPIC updates from GitHub repositories"""
    
    def run(self):
        """Run all crawling examples"""
        self.print_header("🚀 GitHub MCP EPIC Crawling Examples")
        
        # Setup GitHub token
        if not self.setup_github_token():
            print("\n⚠️  Some examples may not work without a GitHub token")
            print("   Set GITHUB_TOKEN environment variable to enable full functionality")
        
        # Run examples
        epic_data = self.example_crawl_epic_updates()
        self.example_crawl_specific_issues()
        self.example_get_epic_updates_from_issue()
        
        return epic_data
    
    def example_crawl_epic_updates(self):
        """Example: Crawl EPIC updates from a repository"""
        self.print_header("EXAMPLE 1: Crawling EPIC Updates from Repository")
        
        try:
            # Crawl EPIC updates from the last 30 days
            result = crawl_epic_updates(
                repo=self.repo_name,
                start_date="2024-01-01"  # Use a realistic date in the past
            )
            
            epic_data = self.handle_result(
                result, 
                "Successfully crawled EPIC updates from repository"
            )
            
            if epic_data:
                self.print_result_summary(epic_data, "Repository Crawl Results")
            
            return epic_data
            
        except Exception as e:
            print(f"❌ Error crawling EPIC updates: {e}")
            return None
    
    def example_crawl_specific_issues(self):
        """Example: Crawl EPIC updates from specific issue numbers"""
        self.print_header("EXAMPLE 2: Crawling EPIC Updates from Specific Issues")
        
        try:
            # Crawl EPIC updates from specific issue numbers
            result = crawl_specific_issues(
                repo=self.repo_name,
                issue_numbers="1,2,3"  # Example issue numbers
            )
            
            specific_data = self.handle_result(
                result,
                "Successfully crawled EPIC updates from specific issues"
            )
            
            if specific_data:
                self.print_result_summary(specific_data, "Specific Issues Crawl Results")
            
            return specific_data
            
        except Exception as e:
            print(f"❌ Error crawling specific issues: {e}")
            return None
    
    def example_get_epic_updates_from_issue(self):
        """Example: Get EPIC updates from a specific issue"""
        self.print_header("EXAMPLE 3: Getting EPIC Updates from Specific Issue")
        
        try:
            # Get EPIC updates from the specific issue URL
            issue_data = get_epic_updates_from_issue(
                issue_url=self.github_url,
                target_date="2025-07-15"  # Adjust this date as needed
            )
            
            issue_result = self.handle_result(
                issue_data,
                "Successfully retrieved EPIC updates from specific issue"
            )
            
            if issue_result:
                self.print_result_summary(issue_result, "Issue-Specific Results")
            
            return issue_result
            
        except Exception as e:
            print(f"❌ Error getting EPIC updates from issue: {e}")
            return None
    
    def example_crawl_with_issue_numbers(self, issue_numbers: str = "1,2,3"):
        """Example: Crawl EPIC updates with specific issue numbers using the main function"""
        self.print_header("EXAMPLE 4: Crawling with Issue Numbers Parameter")
        
        try:
            # Use the main crawl function with issue numbers
            result = crawl_epic_updates(
                repo=self.repo_name,
                issue_numbers=issue_numbers
            )
            
            issue_data = self.handle_result(
                result,
                f"Successfully crawled EPIC updates for issues: {issue_numbers}"
            )
            
            if issue_data:
                self.print_result_summary(issue_data, "Issue Numbers Crawl Results")
            
            return issue_data
            
        except Exception as e:
            print(f"❌ Error crawling with issue numbers: {e}")
            return None
    
    def example_crawl_with_date_range(self, start_date: str = "2024-01-01", end_date: str = "2024-12-31"):
        """Example: Crawl EPIC updates with specific date range"""
        self.print_header("EXAMPLE 5: Crawling with Date Range")
        
        try:
            # Crawl EPIC updates with specific date range
            result = crawl_epic_updates(
                repo=self.repo_name,
                start_date=start_date,
                end_date=end_date
            )
            
            date_data = self.handle_result(
                result,
                f"Successfully crawled EPIC updates from {start_date} to {end_date}"
            )
            
            if date_data:
                self.print_result_summary(date_data, "Date Range Crawl Results")
            
            return date_data
            
        except Exception as e:
            print(f"❌ Error crawling with date range: {e}")
            return None


if __name__ == "__main__":
    # Run crawling examples
    crawler = CrawlingExamples()
    crawler.run()
