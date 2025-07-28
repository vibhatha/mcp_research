# tools/github_tools.py

import os
import re
from typing import List, Dict, Optional
from datetime import datetime, timedelta
from dataclasses import dataclass
import requests
from server import mcp

@dataclass
class EpicUpdate:
    """Represents an EPIC update from a GitHub issue comment"""
    issue_number: int
    issue_title: str
    comment_id: int
    comment_body: str
    author: str
    created_at: str
    repo: str
    parsed_data: Optional[Dict] = None

@dataclass
class ParsedEpicData:
    """Parsed structured data from EPIC update template"""
    date: str
    owner: str
    epic_name: str
    status: str
    progress: str
    what_happened: List[str]
    scope_changes: List[str]
    risks_blockers: List[str]
    next_steps: List[str]
    metrics_deliverables: List[str]

class GitHubIssueCrawler:
    """Crawls GitHub issues to find EPIC update comments"""
    
    def __init__(self, token: Optional[str] = None):
        self.token = token or os.getenv('GITHUB_TOKEN')
        if not self.token:
            raise ValueError("GitHub token is required. Set GITHUB_TOKEN environment variable.")
        
        self.headers = {
            'Authorization': f'token {self.token}',
            'Accept': 'application/vnd.github.v3+json'
        }
        self.base_url = "https://api.github.com"
    
    def get_issues(self, repo: str, state: str = "open", since: Optional[str] = None) -> List[Dict]:
        """Get issues from a repository"""
        url = f"{self.base_url}/repos/{repo}/issues"
        params = {
            'state': state,
            'per_page': 100
        }
        if since:
            params['since'] = since
            
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def get_issue_comments(self, repo: str, issue_number: int) -> List[Dict]:
        """Get all comments for a specific issue"""
        url = f"{self.base_url}/repos/{repo}/issues/{issue_number}/comments"
        params = {'per_page': 100}
        
        response = requests.get(url, headers=self.headers, params=params)
        response.raise_for_status()
        return response.json()
    
    def is_epic_update_comment(self, comment_body: str) -> bool:
        """Check if a comment contains an EPIC update"""
        # Look for the specific EPIC update template pattern
        epic_patterns = [
            r'<!-- epic-update-template -->',
            r'## 🚀 Epic Update',
            r'@epic-update'
        ]
        
        comment_upper = comment_body.upper()
        return any(re.search(pattern, comment_upper, re.IGNORECASE) for pattern in epic_patterns)
    
    def extract_epic_updates(self, repo: str, days_back: int = 30, start_date: str = None, end_date: str = None) -> List[EpicUpdate]:
        """Extract EPIC updates from issues in the specified date range"""
        if start_date:
            # Use specific date range
            start_dt = datetime.strptime(start_date, '%Y-%m-%d')
            end_dt = datetime.strptime(end_date, '%Y-%m-%d') if end_date else datetime.now()
            since_date = start_dt.isoformat()
        else:
            # Use days_back
            since_date = (datetime.now() - timedelta(days=days_back)).isoformat()
            start_dt = datetime.now() - timedelta(days=days_back)
            end_dt = datetime.now()
        
        issues = self.get_issues(repo, since=since_date)
        
        epic_updates = []
        
        for issue in issues:
            comments = self.get_issue_comments(repo, issue['number'])
            
            for comment in comments:
                # Check if comment is within the date range
                comment_date = datetime.strptime(comment['created_at'][:10], '%Y-%m-%d')
                if start_dt <= comment_date <= end_dt:
                    if self.is_epic_update_comment(comment['body']):
                        # Parse the structured EPIC data
                        parsed_data = self.parse_epic_template(comment['body'])
                        
                        epic_update = EpicUpdate(
                            issue_number=issue['number'],
                            issue_title=issue['title'],
                            comment_id=comment['id'],
                            comment_body=comment['body'],
                            author=comment['user']['login'],
                            created_at=comment['created_at'],
                            repo=repo,
                            parsed_data=parsed_data
                        )
                        epic_updates.append(epic_update)
        
        return epic_updates
    
    def parse_epic_template(self, comment_body: str) -> Optional[ParsedEpicData]:
        """Parse structured data from EPIC update template"""
        try:
            lines = comment_body.split('\n')
            parsed = ParsedEpicData(
                date="",
                owner="",
                epic_name="",
                status="",
                progress="",
                what_happened=[],
                scope_changes=[],
                risks_blockers=[],
                next_steps=[],
                metrics_deliverables=[]
            )
            
            current_section = None
            
            for line in lines:
                line = line.strip()
                if not line:
                    continue
                
                # Extract date
                if line.startswith('**Date:**'):
                    parsed.date = line.replace('**Date:**', '').strip()
                
                # Extract owner
                elif line.startswith('**Owner:**'):
                    parsed.owner = line.replace('**Owner:**', '').strip()
                
                # Extract epic name
                elif line.startswith('**Epic:**'):
                    parsed.epic_name = line.replace('**Epic:**', '').strip()
                
                # Extract status
                elif line.startswith('- **Current status:**'):
                    status_text = line.replace('- **Current status:**', '').strip()
                    if '_' in status_text:
                        parsed.status = status_text.split('_')[1].split('_')[0].strip()
                    else:
                        parsed.status = status_text
                
                # Extract progress
                elif line.startswith('- **Progress (%):**'):
                    parsed.progress = line.replace('- **Progress (%):**', '').strip()
                
                # Detect sections
                elif line == '### What happened since last update':
                    current_section = 'what_happened'
                elif line == '### Scope changes':
                    current_section = 'scope_changes'
                elif line == '### Risks / blockers':
                    current_section = 'risks_blockers'
                elif line == '### Next steps (with owners & dates)':
                    current_section = 'next_steps'
                elif line == '### Metrics / deliverables':
                    current_section = 'metrics_deliverables'
                
                # Collect section content
                elif current_section and line.startswith('- '):
                    content = line[2:].strip()  # Remove the "- " prefix
                    if current_section == 'what_happened':
                        parsed.what_happened.append(content)
                    elif current_section == 'scope_changes':
                        parsed.scope_changes.append(content)
                    elif current_section == 'risks_blockers':
                        parsed.risks_blockers.append(content)
                    elif current_section == 'next_steps':
                        parsed.next_steps.append(content)
                    elif current_section == 'metrics_deliverables':
                        parsed.metrics_deliverables.append(content)
            
            return parsed
            
        except Exception as e:
            print(f"Error parsing EPIC template: {e}")
            return None

@mcp.tool()
def crawl_epic_updates(repo: str, days_back: int = 30, start_date: str = None, end_date: str = None) -> str:
    """
    Crawl GitHub issues to find EPIC update comments from the last N days or specific date range.
    
    Args:
        repo: Repository name in format 'owner/repo' (e.g., 'LDFLK/launch')
        days_back: Number of days to look back for updates (default: 30)
        start_date: Start date in YYYY-MM-DD format (optional, overrides days_back)
        end_date: End date in YYYY-MM-DD format (optional, defaults to today)
    
    Returns:
        JSON string containing all EPIC updates found
    """
    try:
        crawler = GitHubIssueCrawler()
        epic_updates = crawler.extract_epic_updates(repo, days_back, start_date, end_date)
        
        # Convert to serializable format
        updates_data = []
        for update in epic_updates:
            update_data = {
                'issue_number': update.issue_number,
                'issue_title': update.issue_title,
                'comment_id': update.comment_id,
                'comment_body': update.comment_body,
                'author': update.author,
                'created_at': update.created_at,
                'repo': update.repo
            }
            
            # Add parsed data if available
            if update.parsed_data:
                update_data['parsed_data'] = {
                    'date': update.parsed_data.date,
                    'owner': update.parsed_data.owner,
                    'epic_name': update.parsed_data.epic_name,
                    'status': update.parsed_data.status,
                    'progress': update.parsed_data.progress,
                    'what_happened': update.parsed_data.what_happened,
                    'scope_changes': update.parsed_data.scope_changes,
                    'risks_blockers': update.parsed_data.risks_blockers,
                    'next_steps': update.parsed_data.next_steps,
                    'metrics_deliverables': update.parsed_data.metrics_deliverables
                }
            
            updates_data.append(update_data)
        
        return {
            'total_updates': len(updates_data),
            'repo': repo,
            'days_back': days_back,
            'updates': updates_data
        }
    
    except Exception as e:
        return f"Error crawling EPIC updates: {str(e)}"

@mcp.tool()
def get_epic_updates_from_issue(issue_url: str, target_date: str = None) -> str:
    """
    Extract EPIC updates from a specific GitHub issue URL.
    
    Args:
        issue_url: Full GitHub issue URL (e.g., 'https://github.com/LDFLK/launch/issues/151')
        target_date: Specific date to filter for in YYYY-MM-DD format (optional)
    
    Returns:
        JSON string containing EPIC updates from the specific issue
    """
    try:
        # Parse the issue URL to extract repo and issue number
        import re
        url_pattern = r'https://github\.com/([^/]+/[^/]+)/issues/(\d+)'
        match = re.match(url_pattern, issue_url)
        
        if not match:
            return "Invalid GitHub issue URL format. Expected: https://github.com/owner/repo/issues/number"
        
        repo = match.group(1)
        issue_number = int(match.group(2))
        
        crawler = GitHubIssueCrawler()
        comments = crawler.get_issue_comments(repo, issue_number)
        
        epic_updates = []
        target_dt = None
        
        if target_date:
            target_dt = datetime.strptime(target_date, '%Y-%m-%d')
        
        print(">>>> comments", comments)
        
        for comment in comments:
            # Filter by date if specified
            if target_dt:
                comment_date = datetime.strptime(comment['created_at'][:10], '%Y-%m-%d')
                if comment_date != target_dt:
                    continue
            
            if crawler.is_epic_update_comment(comment['body']):
                # Parse the structured EPIC data
                parsed_data = crawler.parse_epic_template(comment['body'])
                
                epic_update = EpicUpdate(
                    issue_number=issue_number,
                    issue_title=f"Issue #{issue_number}",  # We'll get the actual title if needed
                    comment_id=comment['id'],
                    comment_body=comment['body'],
                    author=comment['user']['login'],
                    created_at=comment['created_at'],
                    repo=repo,
                    parsed_data=parsed_data
                )
                epic_updates.append(epic_update)
        
        # Convert to serializable format
        updates_data = []
        print(">>>> epic_updates", epic_updates)
        
        for update in epic_updates:
            update_data = {
                'issue_number': update.issue_number,
                'issue_title': update.issue_title,
                'comment_id': update.comment_id,
                'comment_body': update.comment_body,
                'author': update.author,
                'created_at': update.created_at,
                'repo': update.repo,
                'issue_url': issue_url
            }
            
            # Add parsed data if available
            if update.parsed_data:
                update_data['parsed_data'] = {
                    'date': update.parsed_data.date,
                    'owner': update.parsed_data.owner,
                    'epic_name': update.parsed_data.epic_name,
                    'status': update.parsed_data.status,
                    'progress': update.parsed_data.progress,
                    'what_happened': update.parsed_data.what_happened,
                    'scope_changes': update.parsed_data.scope_changes,
                    'risks_blockers': update.parsed_data.risks_blockers,
                    'next_steps': update.parsed_data.next_steps,
                    'metrics_deliverables': update.parsed_data.metrics_deliverables
                }
            
            updates_data.append(update_data)
        
        return {
            'total_updates': len(updates_data),
            'repo': repo,
            'issue_number': issue_number,
            'issue_url': issue_url,
            'target_date': target_date,
            'updates': updates_data
        }
    
    except Exception as e:
        return f"Error extracting EPIC updates from issue: {str(e)}"

@mcp.tool()
def generate_board_report(epic_updates_data: str, format_type: str = "executive") -> str:
    """
    Generate a board of directors report from EPIC updates.
    
    Args:
        epic_updates_data: JSON string containing EPIC updates from crawl_epic_updates
        format_type: Report format - 'executive', 'detailed', or 'summary'
    
    Returns:
        Formatted board report
    """
    try:
        import json
        data = json.loads(epic_updates_data) if isinstance(epic_updates_data, str) else epic_updates_data
        
        if not data.get('updates'):
            return "No EPIC updates found for the specified period."
        
        report = f"#EPIC Update Report\n\n"
        report += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        report += f"**Repository:** {data['repo']}\n"
        report += f"**Period:** Last {data['days_back']} days\n"
        report += f"**Total Updates:** {data['total_updates']}\n\n"
        
        if format_type == "summary":
            # Summary format - just key metrics
            report += "## Executive Summary\n\n"
            report += f"- **Total EPIC Updates:** {data['total_updates']}\n"
            report += f"- **Active Issues:** {len(set(u['issue_number'] for u in data['updates']))}\n"
            report += f"- **Contributors:** {len(set(u['author'] for u in data['updates']))}\n\n"
            
        elif format_type == "executive":
            # Executive format - high-level overview with structured EPIC data
            report += "## Key EPIC Updates\n\n"
            
            # Group by issue
            issues = {}
            for update in data['updates']:
                issue_num = update['issue_number']
                if issue_num not in issues:
                    issues[issue_num] = []
                issues[issue_num].append(update)
            
            for issue_num, updates in issues.items():
                latest_update = max(updates, key=lambda x: x['created_at'])
                report += f"### Issue #{issue_num}: {latest_update['issue_title']}\n"
                report += f"**Latest Update:** {latest_update['created_at'][:10]} by @{latest_update['author']}\n\n"
                
                # Use structured EPIC data if available
                if 'parsed_data' in latest_update and latest_update['parsed_data']:
                    parsed = latest_update['parsed_data']
                    report += f"**Epic:** {parsed.get('epic_name', 'N/A')}\n"
                    report += f"**Owner:** {parsed.get('owner', 'N/A')}\n"
                    report += f"**Status:** {parsed.get('status', 'N/A')}\n"
                    report += f"**Progress:** {parsed.get('progress', 'N/A')}\n\n"
                    
                    # Add key sections
                    if parsed.get('what_happened'):
                        report += "**Recent Progress:**\n"
                        for item in parsed['what_happened'][:3]:  # Limit to 3 items
                            report += f"- {item}\n"
                        report += "\n"
                    
                    if parsed.get('risks_blockers'):
                        report += "**Risks/Blockers:**\n"
                        for item in parsed['risks_blockers'][:2]:  # Limit to 2 items
                            report += f"- {item}\n"
                        report += "\n"
                    
                    if parsed.get('next_steps'):
                        report += "**Next Steps:**\n"
                        for item in parsed['next_steps'][:3]:  # Limit to 3 items
                            report += f"- {item}\n"
                        report += "\n"
                else:
                    # Fallback to raw content extraction
                    lines = latest_update['comment_body'].split('\n')
                    epic_content = []
                    in_epic_section = False
                    
                    for line in lines[:10]:  # Limit to first 10 lines
                        if any(pattern in line.upper() for pattern in ['EPIC UPDATE', 'BOARD UPDATE', 'EXECUTIVE UPDATE']):
                            in_epic_section = True
                            epic_content.append(line)
                        elif in_epic_section and line.strip():
                            epic_content.append(line)
                        elif in_epic_section and not line.strip():
                            break
                    
                    if epic_content:
                        report += "**Update Summary:**\n"
                        report += "```\n" + '\n'.join(epic_content) + "\n```\n\n"
                
        else:  # detailed format
            report += "## Detailed EPIC Updates\n\n"
            
            for update in data['updates']:
                report += f"### Issue #{update['issue_number']}: {update['issue_title']}\n"
                report += f"**Author:** @{update['author']}\n"
                report += f"**Date:** {update['created_at']}\n\n"
                report += "**Full Update:**\n"
                report += "```\n" + update['comment_body'] + "\n```\n\n"
                report += "---\n\n"
        
        return report
        
    except Exception as e:
        return f"Error generating board report: {str(e)}"

@mcp.tool()
def analyze_epic_trends(epic_updates_data: str) -> str:
    """
    Analyze trends in EPIC updates for strategic insights.
    
    Args:
        epic_updates_data: JSON string containing EPIC updates from crawl_epic_updates
    
    Returns:
        Analysis of EPIC update trends
    """
    try:
        import json
        from collections import Counter, defaultdict
        
        data = json.loads(epic_updates_data) if isinstance(epic_updates_data, str) else epic_updates_data
        
        if not data.get('updates'):
            return "No EPIC updates found for analysis."
        
        updates = data['updates']
        
        # Analyze trends
        author_counts = Counter(update['author'] for update in updates)
        issue_counts = Counter(update['issue_number'] for update in updates)
        
        # Date analysis
        dates = [update['created_at'][:10] for update in updates]
        date_counts = Counter(dates)
        
        # Content analysis
        total_updates = len(updates)
        unique_issues = len(set(update['issue_number'] for update in updates))
        unique_authors = len(author_counts)
        
        analysis = f"# EPIC Updates Trend Analysis\n\n"
        analysis += f"**Analysis Period:** Last {data['days_back']} days\n"
        analysis += f"**Repository:** {data['repo']}\n\n"
        
        analysis += "## Key Metrics\n\n"
        analysis += f"- **Total EPIC Updates:** {total_updates}\n"
        analysis += f"- **Unique Issues with Updates:** {unique_issues}\n"
        analysis += f"- **Active Contributors:** {unique_authors}\n"
        analysis += f"- **Average Updates per Issue:** {total_updates/unique_issues:.1f}\n\n"
        
        analysis += "## Top Contributors\n\n"
        for author, count in author_counts.most_common(5):
            analysis += f"- **@{author}:** {count} updates\n"
        
        analysis += "\n## Most Active Issues\n\n"
        for issue_num, count in issue_counts.most_common(5):
            issue_title = next(u['issue_title'] for u in updates if u['issue_number'] == issue_num)
            analysis += f"- **Issue #{issue_num}:** {count} updates - {issue_title}\n"
        
        analysis += "\n## Update Frequency\n\n"
        if date_counts:
            avg_daily = total_updates / len(date_counts)
            analysis += f"- **Average daily updates:** {avg_daily:.1f}\n"
            analysis += f"- **Busiest day:** {max(date_counts, key=date_counts.get)} ({max(date_counts.values())} updates)\n"
        
        return analysis
        
    except Exception as e:
        return f"Error analyzing EPIC trends: {str(e)}"

@mcp.tool()
def generate_epic_status_summary(epic_updates_data: str) -> str:
    """
    Generate a structured EPIC status summary for board reporting.
    
    Args:
        epic_updates_data: JSON string containing EPIC updates from crawl_epic_updates
    
    Returns:
        Structured EPIC status summary
    """
    try:
        import json
        from collections import Counter
        
        data = json.loads(epic_updates_data) if isinstance(epic_updates_data, str) else epic_updates_data
        
        if not data.get('updates'):
            return "No EPIC updates found for the specified period."
        
        updates = data['updates']
        
        # Collect structured data
        status_counts = Counter()
        progress_data = []
        epics_with_risks = []
        epics_with_scope_changes = []
        
        for update in updates:
            if 'parsed_data' in update and update['parsed_data']:
                parsed = update['parsed_data']
                
                # Count statuses
                if parsed.get('status'):
                    status_counts[parsed['status']] += 1
                
                # Collect progress data
                if parsed.get('progress'):
                    progress_data.append({
                        'epic': parsed.get('epic_name', f"Issue #{update['issue_number']}"),
                        'progress': parsed['progress'],
                        'status': parsed.get('status', 'Unknown')
                    })
                
                # Collect epics with risks
                if parsed.get('risks_blockers'):
                    epics_with_risks.append({
                        'epic': parsed.get('epic_name', f"Issue #{update['issue_number']}"),
                        'owner': parsed.get('owner', 'Unknown'),
                        'risks': parsed['risks_blockers']
                    })
                
                # Collect epics with scope changes
                if parsed.get('scope_changes'):
                    epics_with_scope_changes.append({
                        'epic': parsed.get('epic_name', f"Issue #{update['issue_number']}"),
                        'owner': parsed.get('owner', 'Unknown'),
                        'changes': parsed['scope_changes']
                    })
        
        # Generate summary report
        summary = f"# EPIC Status Summary\n\n"
        summary += f"**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}\n"
        summary += f"**Repository:** {data['repo']}\n"
        summary += f"**Period:** Last {data['days_back']} days\n"
        summary += f"**Total EPIC Updates:** {data['total_updates']}\n\n"
        
        # Status breakdown
        if status_counts:
            summary += "## Status Breakdown\n\n"
            for status, count in status_counts.most_common():
                summary += f"- **{status}:** {count} epics\n"
            summary += "\n"
        
        # Progress overview
        if progress_data:
            summary += "## Progress Overview\n\n"
            for item in progress_data[:10]:  # Show top 10
                summary += f"- **{item['epic']}:** {item['progress']} ({item['status']})\n"
            summary += "\n"
        
        # Risks and blockers
        if epics_with_risks:
            summary += "## Epics with Risks/Blockers\n\n"
            for epic in epics_with_risks[:5]:  # Show top 5
                summary += f"### {epic['epic']} (Owner: {epic['owner']})\n"
                for risk in epic['risks'][:3]:  # Show top 3 risks
                    summary += f"- {risk}\n"
                summary += "\n"
        
        # Scope changes
        if epics_with_scope_changes:
            summary += "## Epics with Scope Changes\n\n"
            for epic in epics_with_scope_changes[:5]:  # Show top 5
                summary += f"### {epic['epic']} (Owner: {epic['owner']})\n"
                for change in epic['changes'][:3]:  # Show top 3 changes
                    summary += f"- {change}\n"
                summary += "\n"
        
        return summary
        
    except Exception as e:
        return f"Error generating EPIC status summary: {str(e)}"

@mcp.tool()
def process_dated_epic_update(issue_url: str, target_date: str, output_format: str = "board_report") -> str:
    """
    Process a specific dated EPIC update and generate the requested output format.
    
    Args:
        issue_url: Full GitHub issue URL (e.g., 'https://github.com/LDFLK/launch/issues/151')
        target_date: Specific date in YYYY-MM-DD format for the EPIC update
        output_format: Output format - 'board_report', 'summary', 'detailed', 'raw_data'
    
    Returns:
        Processed EPIC update in the requested format
    """
    try:
        # Get EPIC updates from the specific issue and date
        epic_data = get_epic_updates_from_issue(issue_url, target_date)
        
        if isinstance(epic_data, str) and epic_data.startswith("Error"):
            return epic_data
        
        if epic_data['total_updates'] == 0:
            return f"No EPIC updates found for issue {issue_url} on {target_date}"
        
        # Process based on output format
        if output_format == "raw_data":
            return epic_data
        elif output_format == "summary":
            return generate_epic_status_summary(epic_data)
        elif output_format == "detailed":
            return generate_board_report(epic_data, "detailed")
        else:  # board_report (default)
            return generate_board_report(epic_data, "executive")
    
    except Exception as e:
        return f"Error processing dated EPIC update: {str(e)}"

@mcp.tool()
def get_epic_update_by_date_range(repo: str, start_date: str, end_date: str, output_format: str = "board_report") -> str:
    """
    Get EPIC updates from a repository within a specific date range.
    
    Args:
        repo: Repository name in format 'owner/repo' (e.g., 'LDFLK/launch')
        start_date: Start date in YYYY-MM-DD format
        end_date: End date in YYYY-MM-DD format
        output_format: Output format - 'board_report', 'summary', 'detailed', 'raw_data'
    
    Returns:
        Processed EPIC updates in the requested format
    """
    try:
        # Get EPIC updates from the date range
        epic_data = crawl_epic_updates(repo, start_date=start_date, end_date=end_date)
        
        if isinstance(epic_data, str) and epic_data.startswith("Error"):
            return epic_data
        
        if epic_data['total_updates'] == 0:
            return f"No EPIC updates found for {repo} between {start_date} and {end_date}"
        
        # Process based on output format
        if output_format == "raw_data":
            return epic_data
        elif output_format == "summary":
            return generate_epic_status_summary(epic_data)
        elif output_format == "detailed":
            return generate_board_report(epic_data, "detailed")
        else:  # board_report (default)
            return generate_board_report(epic_data, "executive")
    
    except Exception as e:
        return f"Error processing EPIC updates by date range: {str(e)}"
