#!/usr/bin/env python3
"""
Main runner for GitHub MCP EPIC examples.
Orchestrates all example classes and provides a clean interface.
"""

import sys
import argparse
from typing import List, Optional

from base_example import BaseExample
from crawling_examples import CrawlingExamples
from report_examples import ReportExamples
from direct_api_examples import DirectAPIExamples


class MainRunner(BaseExample):
    """Main runner that orchestrates all example classes"""
    
    def __init__(self, repo_name: str = None, github_url: str = None):
        super().__init__(repo_name, github_url)
        self.crawler = CrawlingExamples(repo_name, github_url)
        self.reporter = ReportExamples(repo_name, github_url)
        self.api_examples = DirectAPIExamples(repo_name, github_url)
    
    def run_all_examples(self):
        """Run all examples in sequence"""
        self.print_header("🚀 GitHub MCP EPIC Updates - Complete Example Suite")
        
        # Setup GitHub token
        if not self.setup_github_token():
            print("\n⚠️  Some examples may not work without a GitHub token")
            print("   Set GITHUB_TOKEN environment variable to enable full functionality")
        
        # Run crawling examples and get data for reports
        print("\n" + "="*60)
        print("STEP 1: Crawling Examples")
        print("="*60)
        epic_data = self.crawler.run()
        
        # Run report examples with the crawled data
        print("\n" + "="*60)
        print("STEP 2: Report Generation Examples")
        print("="*60)
        self.reporter.run(epic_data)
        
        # Run direct API examples
        print("\n" + "="*60)
        print("STEP 3: Direct API Examples")
        print("="*60)
        self.api_examples.run()
        
        # Print completion message
        self.print_completion_message()
    
    def run_crawling_only(self):
        """Run only crawling examples"""
        self.print_header("🚀 GitHub MCP EPIC Crawling Examples")
        return self.crawler.run()
    
    def run_reports_only(self, epic_data=None):
        """Run only report generation examples"""
        self.print_header("📊 GitHub MCP EPIC Report Generation Examples")
        self.reporter.run(epic_data)
    
    def run_api_only(self):
        """Run only direct API examples"""
        self.print_header("🔧 GitHub MCP EPIC Direct API Examples")
        self.api_examples.run()
    
    def run_specific_example(self, example_type: str, example_name: str):
        """Run a specific example"""
        self.print_header(f"🎯 Running Specific Example: {example_type} - {example_name}")
        
        if example_type == "crawling":
            if example_name == "repository":
                return self.crawler.example_crawl_epic_updates()
            elif example_name == "specific_issues":
                return self.crawler.example_crawl_specific_issues()
            elif example_name == "issue":
                return self.crawler.example_get_epic_updates_from_issue()
            else:
                print(f"❌ Unknown crawling example: {example_name}")
        
        elif example_type == "reports":
            # Create sample data for report examples
            sample_data = self.reporter._create_sample_epic_data()
            
            if example_name == "board_report":
                self.reporter.example_generate_board_report(sample_data)
            elif example_name == "status_summary":
                self.reporter.example_generate_epic_status_summary(sample_data)
            elif example_name == "trends":
                self.reporter.example_analyze_epic_trends(sample_data)
            elif example_name == "dated_update":
                self.reporter.example_process_dated_epic_update()
            else:
                print(f"❌ Unknown report example: {example_name}")
        
        elif example_type == "api":
            if example_name == "crawler":
                self.api_examples.example_github_issue_crawler()
            elif example_name == "custom_extraction":
                self.api_examples.example_custom_epic_extraction()
            elif example_name == "issue_analysis":
                self.api_examples.example_issue_analysis()
            elif example_name == "comment_filtering":
                self.api_examples.example_comment_filtering()
            elif example_name == "bulk_processing":
                self.api_examples.example_bulk_processing()
            else:
                print(f"❌ Unknown API example: {example_name}")
        
        else:
            print(f"❌ Unknown example type: {example_type}")
    
    def print_completion_message(self):
        """Print completion message with tips"""
        print("\n" + "="*60)
        print("✅ All examples completed!")
        print("="*60)
        self.print_tips()
    
    def list_available_examples(self):
        """List all available examples"""
        print("📋 Available Examples:")
        print("\n🔍 Crawling Examples:")
        print("   - repository: Crawl EPIC updates from repository")
        print("   - specific_issues: Crawl EPIC updates from specific issue numbers")
        print("   - issue: Get EPIC updates from a specific issue")
        
        print("\n📊 Report Examples:")
        print("   - board_report: Generate board report")
        print("   - status_summary: Generate EPIC status summary")
        print("   - trends: Analyze EPIC trends")
        print("   - dated_update: Process dated EPIC update")
        
        print("\n🔧 API Examples:")
        print("   - crawler: Use GitHubIssueCrawler directly")
        print("   - custom_extraction: Custom EPIC extraction with filtering")
        print("   - issue_analysis: Detailed issue analysis")
        print("   - comment_filtering: Advanced comment filtering")
        print("   - bulk_processing: Bulk processing of multiple repositories")
    
    def run(self):
        """Main run method - runs all examples"""
        self.run_all_examples()


def main():
    """Main function with command line argument parsing"""
    parser = argparse.ArgumentParser(description="GitHub MCP EPIC Examples Runner")
    parser.add_argument("--repo", default="ldflk/launch", 
                       help="Repository name in format 'owner/repo'")
    parser.add_argument("--url", default="https://github.com/ldflk/launch/issues/144",
                       help="Example GitHub issue URL")
    parser.add_argument("--type", choices=["all", "crawling", "reports", "api"],
                       default="all", help="Type of examples to run")
    parser.add_argument("--example", help="Specific example to run")
    parser.add_argument("--list", action="store_true", help="List all available examples")
    
    args = parser.parse_args()
    
    # Create runner
    runner = MainRunner(args.repo, args.url)
    
    if args.list:
        runner.list_available_examples()
        return
    
    if args.example:
        # Parse example type and name
        if ":" in args.example:
            example_type, example_name = args.example.split(":", 1)
            runner.run_specific_example(example_type, example_name)
        else:
            print("❌ Please specify example in format 'type:name' (e.g., 'crawling:repository')")
            print("   Use --list to see available examples")
    else:
        # Run based on type
        if args.type == "all":
            runner.run_all_examples()
        elif args.type == "crawling":
            runner.run_crawling_only()
        elif args.type == "reports":
            runner.run_reports_only()
        elif args.type == "api":
            runner.run_api_only()


if __name__ == "__main__":
    main()
