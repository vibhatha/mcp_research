#!/usr/bin/env python3
"""
EPIC Summary Generator CLI

This script provides a command-line interface to generate EPIC summaries
from GitHub issues. It can read issue numbers from a file or accept them
as command-line arguments.

Usage:
    python epic_summary_generator.py --repo org/repo --date 2024-01-15 --output report.json --issues 151,152,153
    python epic_summary_generator.py --repo org/repo --date 2024-01-15 --output report.json --issues-file sample_issues.txt
"""

import argparse
import os
import sys
import json
from datetime import datetime
from typing import List, Optional
from pathlib import Path

# Import the GitHub MCP library
from github_mcp import (
    crawl_specific_issues,
    generate_board_report,
    generate_epic_status_summary,
    generate_epic_summary_report
)


def parse_issue_numbers(issues_input: str) -> List[int]:
    """
    Parse issue numbers from a string input.
    Supports comma-separated values and newline-separated values.
    
    Args:
        issues_input: String containing issue numbers
        
    Returns:
        List of integer issue numbers
    """
    issues = []
    
    # Split by comma first, then by newline for each part
    for part in issues_input.split(','):
        part = part.strip()
        if part:
            # Handle newline-separated values within each comma-separated part
            for line in part.split('\n'):
                line = line.strip()
                if line and not line.startswith('#'):  # Skip comments
                    try:
                        issues.append(int(line))
                    except ValueError:
                        print(f"Warning: Skipping invalid issue number '{line}'")
    
    return issues


def read_issues_from_file(file_path: str) -> List[int]:
    """
    Read issue numbers from a text file.
    
    Args:
        file_path: Path to the file containing issue numbers
        
    Returns:
        List of integer issue numbers
    """
    try:
        with open(file_path, 'r') as f:
            content = f.read()
        return parse_issue_numbers(content)
    except FileNotFoundError:
        print(f"Error: Issue file '{file_path}' not found.")
        sys.exit(1)
    except Exception as e:
        print(f"Error reading issue file: {e}")
        sys.exit(1)


def validate_date(date_string: str) -> str:
    """
    Validate and format a date string.
    
    Args:
        date_string: Date string in YYYY-MM-DD format
        
    Returns:
        Formatted date string
        
    Raises:
        ValueError: If date is invalid
    """
    try:
        datetime.strptime(date_string, '%Y-%m-%d')
        return date_string
    except ValueError:
        raise ValueError(f"Invalid date format: {date_string}. Use YYYY-MM-DD format.")


def validate_repo(repo_string: str) -> str:
    """
    Validate repository format.
    
    Args:
        repo_string: Repository string in org/repo format
        
    Returns:
        Repository string
        
    Raises:
        ValueError: If repository format is invalid
    """
    if '/' not in repo_string or repo_string.count('/') != 1:
        raise ValueError(f"Invalid repository format: {repo_string}. Use 'org/repo' format.")
    return repo_string


def create_date_folder_structure(target_date: str, base_output_dir: str = "reports") -> tuple[str, str]:
    """
    Create a date-based folder structure for organizing reports.
    
    Args:
        target_date: Target date in YYYY-MM-DD format
        base_output_dir: Base directory for reports (default: "reports")
        
    Returns:
        Tuple of (date_folder_path, full_output_path)
    """
    # Parse the date to create folder structure
    try:
        date_obj = datetime.strptime(target_date, '%Y-%m-%d')
        year_month = date_obj.strftime('%Y-%m')
        date_folder = date_obj.strftime('%Y-%m-%d')
    except ValueError:
        # If date parsing fails, use the date string as-is
        year_month = target_date[:7] if len(target_date) >= 7 else target_date
        date_folder = target_date
    
    # Create the folder structure
    date_folder_path = Path(base_output_dir) / year_month / date_folder
    date_folder_path.mkdir(parents=True, exist_ok=True)
    
    return str(date_folder_path), str(date_folder_path)


def generate_epic_summary(repo: str, issue_numbers: List[int], target_date: str, output_path: str) -> None:
    """
    Generate EPIC summary for the given issues and save to output file.
    
    Args:
        repo: Repository name in org/repo format
        issue_numbers: List of issue numbers to process
        target_date: Target date for the summary
        output_path: Path to save the output report
    """
    print(f"🔍 Processing {len(issue_numbers)} issues from {repo}")
    print(f"📅 Target date: {target_date}")
    print(f"💾 Output will be saved to: {output_path}")
    
    # Convert issue numbers to comma-separated string
    issues_str = ','.join(map(str, issue_numbers))
    
    try:
        # Crawl specific issues to get EPIC updates
        print("📊 Crawling EPIC updates...")
        epic_data = crawl_specific_issues(repo=repo, issue_numbers=issues_str)
        
        if isinstance(epic_data, str) and epic_data.startswith("Error"):
            print(f"❌ Error crawling issues: {epic_data}")
            sys.exit(1)
        
        # Generate board report
        print("📋 Generating board report...")
        board_report = generate_board_report(epic_data, format_type="executive")
        
        # Generate epic status summary
        print("📈 Generating epic status summary...")
        status_summary = generate_epic_status_summary(epic_data)
        
        # Combine results
        result = {
            "repo": repo,
            "target_date": target_date,
            "issue_numbers": issue_numbers,
            "generated_at": datetime.now().isoformat(),
            "board_report": board_report,
            "status_summary": status_summary,
            "raw_epic_data": epic_data
        }
        
        # Save to file
        with open(output_path, 'w') as f:
            json.dump(result, f, indent=2)
        
        print(f"✅ EPIC summary generated successfully!")
        print(f"📄 Report saved to: {output_path}")
        
    except Exception as e:
        print(f"❌ Error generating EPIC summary: {e}")
        sys.exit(1)


def main():
    """Main CLI function."""
    parser = argparse.ArgumentParser(
        description="Generate EPIC summaries from GitHub issues. Reports are automatically organized in date-based folders (reports/YYYY-MM/YYYY-MM-DD/).",
        formatter_class=argparse.RawDescriptionHelpFormatter,
        epilog="""
Examples:
  # Using issue numbers from command line (creates reports/2025-08/2025-08-07/report.json)
  python epic_summary_generator.py --repo LDFLK/launch --date 2025-08-07 --output report.json --issues 144
  
  # Using issue numbers from file
  python epic_summary_generator.py --repo LDFLK/launch --date 2025-08-07 --output report.json --issues-file sample_issues.txt
  
  # Generate both JSON report and LLM summary
  python epic_summary_generator.py --repo LDFLK/launch --date 2025-08-07 --output report.json --issues 144 --generate-summary
  
  # Generate summary with custom output path
  python epic_summary_generator.py --repo LDFLK/launch --date 2025-08-07 --output report.json --issues 144 --generate-summary --summary-output summary.md
  
  # Use absolute paths to override folder structure
  python epic_summary_generator.py --repo LDFLK/launch --date 2025-08-07 --output /absolute/path/report.json --issues 144
        """
    )
    
    # Required arguments
    parser.add_argument(
        '--repo', '-r',
        required=True,
        help='Repository name in org/repo format (e.g., microsoft/vscode)'
    )
    
    parser.add_argument(
        '--date', '-d',
        required=True,
        help='Target date for the summary in YYYY-MM-DD format'
    )
    
    parser.add_argument(
        '--output', '-o',
        required=True,
        help='Path to save the output report (JSON format). Will be placed in reports/YYYY-MM/YYYY-MM-DD/ folder unless absolute path is specified.'
    )
    
    # Issue numbers source (mutually exclusive)
    issue_group = parser.add_mutually_exclusive_group(required=True)
    issue_group.add_argument(
        '--issues',
        help='Comma-separated list of issue numbers (e.g., 151,152,153)'
    )
    
    issue_group.add_argument(
        '--issues-file', '-f',
        help='Path to file containing issue numbers (one per line or comma-separated)'
    )
    
    # Optional arguments
    parser.add_argument(
        '--verbose', '-v',
        action='store_true',
        help='Enable verbose output'
    )
    
    parser.add_argument(
        '--generate-summary', '-s',
        action='store_true',
        help='Generate LLM-powered summary report in addition to JSON report'
    )
    
    parser.add_argument(
        '--summary-output',
        help='Path to save the LLM summary report (default: <output>.md). Will be placed in reports/YYYY-MM/YYYY-MM-DD/ folder unless absolute path is specified.'
    )
    
    args = parser.parse_args()
    
    # Validate inputs
    try:
        repo = validate_repo(args.repo)
        target_date = validate_date(args.date)
    except ValueError as e:
        print(f"❌ Validation error: {e}")
        sys.exit(1)
    
    # Get issue numbers
    if args.issues:
        issue_numbers = parse_issue_numbers(args.issues)
    else:
        issue_numbers = read_issues_from_file(args.issues_file)
    
    if not issue_numbers:
        print("❌ No valid issue numbers found.")
        sys.exit(1)
    
    # Create date-based folder structure
    date_folder_path, _ = create_date_folder_structure(target_date)
    
    # Update output paths to use the date folder
    if not args.output.startswith('/') and not args.output.startswith('./'):
        # If output is not an absolute path, place it in the date folder
        output_filename = os.path.basename(args.output)
        final_output_path = os.path.join(date_folder_path, output_filename)
    else:
        final_output_path = args.output
    
    # Determine summary output path
    if args.generate_summary:
        if args.summary_output:
            if not args.summary_output.startswith('/') and not args.summary_output.startswith('./'):
                # If summary output is not an absolute path, place it in the date folder
                summary_filename = os.path.basename(args.summary_output)
                final_summary_path = os.path.join(date_folder_path, summary_filename)
            else:
                final_summary_path = args.summary_output
        else:
            # Default summary output in the same date folder
            summary_filename = f"{os.path.splitext(os.path.basename(final_output_path))[0]}.md"
            final_summary_path = os.path.join(date_folder_path, summary_filename)
    
    if args.verbose:
        print(f"🔍 Repository: {repo}")
        print(f"📅 Target date: {target_date}")
        print(f"📋 Issue numbers: {issue_numbers}")
        print(f"📁 Date folder: {date_folder_path}")
        print(f"💾 Output path: {final_output_path}")
        if args.generate_summary:
            print(f"📝 Summary output: {final_summary_path}")
    
    # Check if GitHub token is available
    if not os.getenv('GITHUB_TOKEN'):
        print("⚠️  Warning: GITHUB_TOKEN environment variable not set")
        print("   Set it with: export GITHUB_TOKEN='your-github-token'")
        print("   For public repositories, this may not be required.")
    
    # Check if DeepSeek token is available for summary generation
    if args.generate_summary and not os.getenv('DEEPSEEK_API_KEY'):
        print("⚠️  Warning: DEEPSEEK_API_KEY environment variable not set")
        print("   Set it with: export DEEPSEEK_API_KEY='your-deepseek-api-key'")
        print("   Required for generating LLM-powered summaries.")
    
    # Generate the EPIC summary
    generate_epic_summary(repo, issue_numbers, target_date, final_output_path)
    
    # Generate LLM summary if requested
    if args.generate_summary:
        print(f"🤖 Generating LLM-powered summary...")
        try:
            # Read the generated JSON report
            with open(final_output_path, 'r') as f:
                report_data = json.load(f)
            
            # Generate the summary
            summary_report = generate_epic_summary_report(json.dumps(report_data))
            
            # Save the summary
            with open(final_summary_path, 'w') as f:
                f.write(summary_report)
            
            print(f"✅ LLM summary saved to: {final_summary_path}")
        except Exception as e:
            print(f"❌ Error generating LLM summary: {e}")


if __name__ == "__main__":
    main()
