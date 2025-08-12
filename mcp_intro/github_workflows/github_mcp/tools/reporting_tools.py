# tools/reporting_tools.py

import os
import json
import requests
from datetime import datetime
from typing import Dict, List, Optional

# Try to import MCP server, but make it optional
try:
    from server import mcp
    MCP_AVAILABLE = True
except ImportError:
    MCP_AVAILABLE = False
    # Create a dummy decorator for when MCP is not available
    class DummyMCP:
        def tool(self):
            def decorator(func):
                return func
            return decorator
    mcp = DummyMCP()


class EpicReportSummarizer:
    """Summarizes EPIC reports using DeepSeek LLM"""
    
    def __init__(self, api_key: Optional[str] = None):
        self.api_key = api_key or os.getenv('DEEPSEEK_API_KEY')
        
        if not self.api_key:
            print("⚠️  Warning: DEEPSEEK_API_KEY environment variable not set")
            print("   Set it with: export DEEPSEEK_API_KEY='your-api-key'")
    
    def _call_deepseek_api(self, prompt: str, system_prompt: str = None, max_tokens: int = 1000) -> str:
        """Call DeepSeek API with the given prompt"""
        
        if not self.api_key:
            return "Error: DeepSeek API key not configured"
        
        headers = {
            "Authorization": f"Bearer {self.api_key}",
            "Content-Type": "application/json"
        }
        
        messages = []
        if system_prompt:
            messages.append({"role": "system", "content": system_prompt})
        messages.append({"role": "user", "content": prompt})
        
        data = {
            "model": "deepseek-chat",
            "messages": messages,
            "max_tokens": max_tokens,
            "temperature": 0.7
        }
        
        try:
            response = requests.post(
                "https://api.deepseek.com/v1/chat/completions",
                headers=headers,
                json=data,
                timeout=30
            )
            
            if response.status_code == 200:
                return response.json()["choices"][0]["message"]["content"]
            else:
                return f"Error calling DeepSeek API: {response.status_code} - {response.text}"
        except Exception as e:
            return f"Error calling DeepSeek API: {str(e)}"
    
    def generate_epic_summary(self, epic_data: Dict) -> str:
        """Generate a detailed summary for a single EPIC"""
        
        repo = epic_data.get('repo', 'N/A')
        issue_number = epic_data.get('issue_number', 'N/A')
        
        prompt = f"""
You are a technical project manager creating a summary of an EPIC update from GitHub.

EPIC Information:
- Repository: {epic_data.get('repo', 'N/A')}
- Issue Number: {epic_data.get('issue_number', 'N/A')}
- Issue Title: {epic_data.get('issue_title', 'N/A')}
- Author: {epic_data.get('author', 'N/A')}
- Date: {epic_data.get('created_at', 'N/A')}

EPIC Update Content:
{epic_data.get('comment_body', 'N/A')}

Parsed Data:
{json.dumps(epic_data.get('parsed_data', {}), indent=2)}

Please create a comprehensive summary in markdown format that includes:

1. **Issue Link**: Create a GitHub issue link in the format: `https://github.com/{repo}/issues/{issue_number}`
2. **Work Summary**: A clear summary of what work was done, focusing on:
   - Key accomplishments and progress made
   - Technical changes and implementations
   - Any challenges overcome
   - Impact on the project
3. **Status Overview**: Current status and progress percentage
4. **Next Steps**: What's coming up next
5. **Twitter Summary**: A 140-word summary suitable for a Twitter post that captures the key achievements and impact

Format the response as:
```markdown
## Issue #[issue_number]: [issue_title]

**Issue Link:** [GitHub link]

### Work Summary
[Detailed summary of work done]

### Status
- **Current Status:** [status]
- **Progress:** [progress]

### Next Steps
[Next steps]

### Twitter Summary (140 words)
[Twitter-friendly summary]
```

Make the summary engaging, technical but accessible, and highlight the most important achievements.
"""
        
        return self._call_deepseek_api(
            prompt=prompt,
            system_prompt="You are a technical project manager creating EPIC summaries.",
            max_tokens=1000
        )
    
    def generate_overall_summary(self, report_data: Dict) -> str:
        """Generate an overall summary of all EPICs"""
        
        total_updates = report_data.get('raw_epic_data', {}).get('total_updates', 0)
        repo = report_data.get('repo', 'N/A')
        target_date = report_data.get('target_date', 'N/A')
        
        updates = report_data.get('raw_epic_data', {}).get('updates', [])
        
        # Extract key information from all updates
        epic_summaries = []
        for update in updates:
            parsed = update.get('parsed_data', {})
            epic_summaries.append({
                'issue': update.get('issue_number'),
                'title': update.get('issue_title'),
                'status': parsed.get('status', 'Unknown'),
                'progress': parsed.get('progress', ''),
                'what_happened': parsed.get('what_happened', [])
            })
        
        prompt = f"""
You are creating an overall summary of EPIC updates for a project.

Project Information:
- Repository: {repo}
- Date: {target_date}
- Total EPIC Updates: {total_updates}

EPIC Summaries:
{json.dumps(epic_summaries, indent=2)}

Please create an overall project summary in markdown format that includes:

1. **Project Overview**: Brief overview of the project and what was accomplished
2. **Key Achievements**: Highlight the most significant accomplishments across all EPICs
3. **Overall Status**: General project status and progress
4. **Twitter Summary**: A 140-word summary suitable for a Twitter post that captures the overall project progress and key achievements

Format as:
```markdown
# Project EPIC Summary

## Project Overview
[Brief project overview]

## Key Achievements
[Key accomplishments across all EPICs]

## Overall Status
[General project status]

## Twitter Summary (140 words)
[Twitter-friendly overall summary]
```

Make it engaging and highlight the most impactful work done across all EPICs.
"""
        
        return self._call_deepseek_api(
            prompt=prompt,
            system_prompt="You are a technical project manager creating project summaries.",
            max_tokens=800
        )
    
    def generate_complete_summary(self, report_data: Dict) -> str:
        """Generate a complete summary report with overall and individual EPIC summaries"""
        
        print(f"📊 Processing EPIC report from {report_data.get('repo', 'N/A')}")
        print(f"📅 Target date: {report_data.get('target_date', 'N/A')}")
        print(f"📋 Total updates: {report_data.get('raw_epic_data', {}).get('total_updates', 0)}")
        
        # Generate overall summary
        print("🤖 Generating overall project summary...")
        overall_summary = self.generate_overall_summary(report_data)
        
        # Generate individual EPIC summaries
        updates = report_data.get('raw_epic_data', {}).get('updates', [])
        epic_summaries = []
        
        for i, update in enumerate(updates, 1):
            print(f"🤖 Generating summary for EPIC {i}/{len(updates)}...")
            epic_summary = self.generate_epic_summary(update)
            epic_summaries.append(epic_summary)
        
        # Combine all summaries
        final_report = f"""# EPIC Summary Report

**Generated:** {datetime.now().strftime('%Y-%m-%d %H:%M:%S')}
**Repository:** {report_data.get('repo', 'N/A')}
**Target Date:** {report_data.get('target_date', 'N/A')}

{overall_summary}

---

## Individual EPIC Summaries

"""
        
        for summary in epic_summaries:
            final_report += f"{summary}\n\n---\n\n"
        
        return final_report


@mcp.tool()
def generate_epic_summary_report(epic_report_data: str, output_format: str = "markdown") -> str:
    """
    Generate a comprehensive summary report from EPIC data using DeepSeek LLM.
    
    Args:
        epic_report_data: JSON string containing EPIC report data from epic_summary_generator
        output_format: Output format - 'markdown' or 'json' (default: markdown)
    
    Returns:
        Formatted summary report in the specified format
    """
    try:
        # Parse the report data
        if isinstance(epic_report_data, str):
            report_data = json.loads(epic_report_data)
        else:
            report_data = epic_report_data
        
        # Create summarizer
        summarizer = EpicReportSummarizer()
        
        # Generate the complete summary
        summary_report = summarizer.generate_complete_summary(report_data)
        
        if output_format.lower() == "json":
            # Return as JSON
            return json.dumps({
                "summary_report": summary_report,
                "generated_at": datetime.now().isoformat(),
                "repo": report_data.get('repo'),
                "target_date": report_data.get('target_date'),
                "total_updates": report_data.get('raw_epic_data', {}).get('total_updates', 0)
            }, indent=2)
        else:
            # Return as markdown
            return summary_report
    
    except Exception as e:
        return f"Error generating summary report: {str(e)}"


@mcp.tool()
def generate_individual_epic_summary(epic_data: str) -> str:
    """
    Generate a summary for a single EPIC update.
    
    Args:
        epic_data: JSON string containing a single EPIC update data
    
    Returns:
        Formatted summary for the individual EPIC
    """
    try:
        # Parse the epic data
        if isinstance(epic_data, str):
            epic_dict = json.loads(epic_data)
        else:
            epic_dict = epic_data
        
        # Create summarizer
        summarizer = EpicReportSummarizer()
        
        # Generate the summary
        return summarizer.generate_epic_summary(epic_dict)
    
    except Exception as e:
        return f"Error generating individual EPIC summary: {str(e)}"


@mcp.tool()
def generate_project_overview_summary(epic_report_data: str) -> str:
    """
    Generate an overall project summary from EPIC data.
    
    Args:
        epic_report_data: JSON string containing EPIC report data
    
    Returns:
        Formatted project overview summary
    """
    try:
        # Parse the report data
        if isinstance(epic_report_data, str):
            report_data = json.loads(epic_report_data)
        else:
            report_data = epic_report_data
        
        # Create summarizer
        summarizer = EpicReportSummarizer()
        
        # Generate the overall summary
        return summarizer.generate_overall_summary(report_data)
    
    except Exception as e:
        return f"Error generating project overview summary: {str(e)}"
