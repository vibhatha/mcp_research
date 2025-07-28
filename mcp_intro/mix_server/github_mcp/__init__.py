"""
GitHub MCP Package

A Python package for GitHub EPIC tools and MCP server implementation.
"""

__version__ = "0.1.0"
__author__ = " Vibhatha Abeykoon"
__email__ = "vibhatha@gmail.com"

# Import main modules for easier access
from .tools.github_tools import (
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

# Import CSV and Parquet functions
from .tools.csv_tools import summarize_csv_file, read_csv_file
from .tools.parquet_tools import summarize_parquet_file, read_parquet_file

__all__ = [
    'GitHubIssueCrawler',
    'EpicUpdate', 
    'ParsedEpicData',
    'crawl_epic_updates',
    'get_epic_updates_from_issue',
    'process_dated_epic_update',
    'generate_board_report',
    'generate_epic_status_summary',
    'analyze_epic_trends',
    'summarize_csv_file',
    'read_csv_file',
    'summarize_parquet_file',
    'read_parquet_file'
] 