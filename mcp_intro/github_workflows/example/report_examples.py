#!/usr/bin/env python3
"""
Report generation examples for GitHub MCP EPIC tools.
Demonstrates how to generate board reports, status summaries, and trend analysis.
"""

from base_example import BaseExample
from github_mcp.tools.github_tools import (
    generate_board_report,
    generate_epic_status_summary,
    analyze_epic_trends,
    process_dated_epic_update
)


class ReportExamples(BaseExample):
    """Examples for generating reports from EPIC data"""
    
    def run(self, epic_data=None):
        """Run all report generation examples"""
        self.print_header("📊 GitHub MCP EPIC Report Generation Examples")
        
        # Setup GitHub token
        if not self.setup_github_token():
            print("\n⚠️  Some examples may not work without a GitHub token")
            print("   Set GITHUB_TOKEN environment variable to enable full functionality")
        
        # Use provided epic_data or create sample data
        if not epic_data:
            epic_data = self._create_sample_epic_data()
        
        # Run examples
        self.example_generate_board_report(epic_data)
        self.example_generate_epic_status_summary(epic_data)
        self.example_analyze_epic_trends(epic_data)
        self.example_process_dated_epic_update()
        self.example_process_dated_epic_update_public()
        self.example_demonstrate_dated_processing_with_sample_data()
    
    def _create_sample_epic_data(self):
        """Create sample EPIC data for demonstration"""
        return {
            'total_updates': 2,
            'repo': self.repo_name,
            'days_back': 30,
            'updates': [
                {
                    'issue_number': 151,
                    'issue_title': 'Sample Epic Implementation',
                    'comment_id': 12345,
                    'comment_body': 'Sample EPIC update content',
                    'author': 'test-user',
                    'created_at': '2025-01-15T14:30:00Z',
                    'repo': self.repo_name,
                    'parsed_data': {
                        'date': '2025-01-15',
                        'owner': '@test-user',
                        'epic_name': 'Sample Epic Implementation',
                        'status': 'On Track',
                        'progress': '75%',
                        'what_happened': ['Completed user authentication module'],
                        'risks_blockers': ['Third-party API rate limiting'],
                        'next_steps': ['Complete UI testing by @qa-team (2025-01-20)']
                    }
                },
                {
                    'issue_number': 152,
                    'issue_title': 'Another Epic Feature',
                    'comment_id': 12346,
                    'comment_body': 'Another EPIC update content',
                    'author': 'another-user',
                    'created_at': '2025-01-16T14:30:00Z',
                    'repo': self.repo_name,
                    'parsed_data': {
                        'date': '2025-01-16',
                        'owner': '@another-user',
                        'epic_name': 'Another Epic Feature',
                        'status': 'At Risk',
                        'progress': '50%',
                        'what_happened': ['Started database migration'],
                        'risks_blockers': ['Complex data transformation'],
                        'next_steps': ['Review migration plan by @dba-team (2025-01-25)']
                    }
                }
            ]
        }
    
    def example_generate_board_report(self, epic_data):
        """Example: Generate board report from EPIC data"""
        self.print_header("EXAMPLE 1: Generating Board Report")
        
        if not epic_data or epic_data.get('total_updates', 0) == 0:
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
    
    def example_generate_epic_status_summary(self, epic_data):
        """Example: Generate EPIC status summary"""
        self.print_header("EXAMPLE 2: Generating EPIC Status Summary")
        
        if not epic_data or epic_data.get('total_updates', 0) == 0:
            print("⚠️  No EPIC data available for status summary")
            return
        
        try:
            status_summary = generate_epic_status_summary(epic_data)
            print("📈 EPIC Status Summary:")
            print("-" * 40)
            print(status_summary)
            
        except Exception as e:
            print(f"❌ Error generating status summary: {e}")
    
    def example_analyze_epic_trends(self, epic_data):
        """Example: Analyze EPIC trends"""
        self.print_header("EXAMPLE 3: Analyzing EPIC Trends")
        
        if not epic_data or epic_data.get('total_updates', 0) == 0:
            print("⚠️  No EPIC data available for trend analysis")
            return
        
        try:
            trends_analysis = analyze_epic_trends(epic_data)
            print("📊 EPIC Trends Analysis:")
            print("-" * 40)
            print(trends_analysis)
            
        except Exception as e:
            print(f"❌ Error analyzing trends: {e}")
    
    def example_process_dated_epic_update(self):
        """Example: Process EPIC update for a specific date"""
        self.print_header("EXAMPLE 4: Processing Dated EPIC Update")
        
        try:
            # Process EPIC update for a specific date and generate board report
            result = process_dated_epic_update(
                issue_url=self.github_url,
                target_date="2025-08-07",  # Adjust this date as needed
                output_format="board_report"
            )
            
            # Check if the result is an error message
            if isinstance(result, str) and result.startswith("Error"):
                print("📋 Dated EPIC Update Report:")
                print("-" * 40)
                print(f"❌ {result}")
                
                # Provide helpful guidance based on the error type
                if "403" in result or "rate limit" in result.lower():
                    print("\n💡 This error indicates:")
                    print("   - GitHub API rate limit exceeded")
                    print("   - Or insufficient permissions for the repository")
                    print("   - Or missing/invalid GitHub token")
                    print("\n🔧 To fix this:")
                    print("   1. Set a valid GITHUB_TOKEN environment variable")
                    print("   2. Wait for rate limit to reset (usually 1 hour)")
                    print("   3. Use a public repository for testing")
                    print("   4. Check repository permissions")
                
                elif "404" in result:
                    print("\n💡 This error indicates:")
                    print("   - Repository or issue not found")
                    print("   - Repository is private and you don't have access")
                    print("   - Issue number doesn't exist")
                
                else:
                    print("\n💡 Try using a public repository for testing:")
                    print("   - microsoft/vscode")
                    print("   - octocat/Hello-World")
                    print("   - facebook/react")
                
                return
            
            print("📋 Dated EPIC Update Report:")
            print("-" * 40)
            print(result)
            
        except Exception as e:
            print(f"❌ Error processing dated EPIC update: {e}")
            print("\n💡 This might be due to:")
            print("   - Network connectivity issues")
            print("   - Invalid repository URL")
            print("   - Missing GitHub token")
    
    def example_process_dated_epic_update_public(self):
        """Example: Process EPIC update for a specific date using public repository"""
        self.print_header("EXAMPLE 4b: Processing Dated EPIC Update (Public Repository)")
        
        try:
            # Use a public repository for demonstration
            public_issue_url = "https://github.com/octocat/Hello-World/issues/1"
            
            print(f"🔍 Trying with public repository: {public_issue_url}")
            
            # Process EPIC update for a specific date and generate board report
            result = process_dated_epic_update(
                issue_url=public_issue_url,
                target_date="2024-01-01",  # Use a date that might have data
                output_format="board_report"
            )
            
            # Check if the result is an error message
            if isinstance(result, str) and result.startswith("Error"):
                print("📋 Dated EPIC Update Report (Public Repo):")
                print("-" * 40)
                print(f"❌ {result}")
                print("\n💡 Even public repositories may not have EPIC updates on specific dates.")
                print("   This is normal - EPIC updates are specific to certain projects.")
                return
            
            print("📋 Dated EPIC Update Report (Public Repo):")
            print("-" * 40)
            print(result)
            
        except Exception as e:
            print(f"❌ Error processing dated EPIC update with public repo: {e}")
    
    def example_demonstrate_dated_processing_with_sample_data(self):
        """Example: Demonstrate dated EPIC processing with sample data"""
        self.print_header("EXAMPLE 4c: Dated EPIC Processing (Sample Data Demo)")
        
        try:
            # Create sample EPIC data that mimics the structure from get_epic_updates_from_issue
            sample_epic_data = {
                'total_updates': 1,
                'repo': 'sample/repo',
                'issue_number': 123,
                'issue_url': 'https://github.com/sample/repo/issues/123',
                'target_date': '2025-08-07',
                'updates': [{
                    'issue_number': 123,
                    'issue_title': 'Sample EPIC Implementation',
                    'comment_id': 456,
                    'comment_body': 'Sample EPIC update content',
                    'author': 'sample-user',
                    'created_at': '2025-08-07T10:00:00Z',
                    'repo': 'sample/repo',
                    'parsed_data': {
                        'date': '2025-08-07',
                        'owner': '@sample-user',
                        'epic_name': 'Sample EPIC Implementation',
                        'status': 'On Track',
                        'progress': '80%',
                        'what_happened': ['Completed core functionality', 'Added unit tests'],
                        'risks_blockers': ['Integration testing pending'],
                        'next_steps': ['Deploy to staging by @devops (2025-08-10)']
                    }
                }]
            }
            
            print("🔍 Demonstrating with sample EPIC data...")
            
            # Generate board report from sample data
            board_report = generate_board_report(sample_epic_data, "executive")
            print("📋 Board Report from Sample Data:")
            print("-" * 40)
            print(board_report)
            
            # Generate status summary from sample data
            status_summary = generate_epic_status_summary(sample_epic_data)
            print("\n📈 Status Summary from Sample Data:")
            print("-" * 40)
            print(status_summary)
            
            # Generate trends analysis from sample data
            trends_analysis = analyze_epic_trends(sample_epic_data)
            print("\n📊 Trends Analysis from Sample Data:")
            print("-" * 40)
            print(trends_analysis)
            
            print("\n✅ This demonstrates how the report functions work with EPIC data!")
            print("   The same functions can be used with real data from GitHub API.")
            
        except Exception as e:
            print(f"❌ Error demonstrating with sample data: {e}")
    
    def example_generate_custom_reports(self, epic_data):
        """Example: Generate custom format reports"""
        self.print_header("EXAMPLE 5: Generating Custom Format Reports")
        
        if not epic_data or epic_data.get('total_updates', 0) == 0:
            print("⚠️  No EPIC data available for custom report generation")
            return
        
        try:
            # Generate different report formats
            formats = ["executive", "summary", "detailed"]
            
            for format_type in formats:
                print(f"\n📋 {format_type.title()} Format Report:")
                print("-" * 40)
                report = generate_board_report(epic_data, format_type)
                print(report)
                
        except Exception as e:
            print(f"❌ Error generating custom reports: {e}")
    
    def example_compare_reports(self, epic_data1, epic_data2):
        """Example: Compare reports from different time periods"""
        self.print_header("EXAMPLE 6: Comparing Reports from Different Periods")
        
        try:
            # Generate reports for different periods
            print("📊 Report for Period 1:")
            print("-" * 40)
            report1 = generate_board_report(epic_data1, "summary")
            print(report1)
            
            print("\n📊 Report for Period 2:")
            print("-" * 40)
            report2 = generate_board_report(epic_data2, "summary")
            print(report2)
            
            print("\n📈 Comparison Summary:")
            print("-" * 40)
            print("This demonstrates how to compare EPIC progress across different time periods.")
            
        except Exception as e:
            print(f"❌ Error comparing reports: {e}")


if __name__ == "__main__":
    # Run report examples
    reporter = ReportExamples()
    reporter.run()
