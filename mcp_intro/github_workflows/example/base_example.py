#!/usr/bin/env python3
"""
Base class for GitHub MCP EPIC examples.
Contains common utilities and configuration used across all examples.
"""

import os
import json
from typing import Dict, Any, Optional


class BaseExample:
    """Base class for all GitHub MCP EPIC examples"""
    
    def __init__(self, repo_name: str = None, github_url: str = None):
        """
        Initialize the base example class
        
        Args:
            repo_name: Repository name in format 'owner/repo'
            github_url: Example GitHub issue URL
        """
        # Default configuration
        self.repo_name = repo_name or "LDFLK/launch"
        self.github_url = github_url or "https://github.com/LDFLK/launch/issues/151"
        self.github_token = os.getenv('GITHUB_TOKEN')
    
    def setup_github_token(self) -> bool:
        """Set up GitHub token for API access"""
        if not self.github_token:
            print("⚠️  Warning: GITHUB_TOKEN environment variable not set")
            print("   Set it with: export GITHUB_TOKEN='your-github-token'")
            print("   Or set it in the script: os.environ['GITHUB_TOKEN'] = 'your-token'")
            print("\n💡 To create a GitHub token:")
            print("   1. Go to GitHub.com → Settings → Developer settings → Personal access tokens")
            print("   2. Generate new token (classic)")
            print("   3. Select scopes: repo, read:org, read:user")
            print("   4. Copy the token and set: export GITHUB_TOKEN='your-token'")
            return False
        
        os.environ['GITHUB_TOKEN'] = self.github_token
        print("✅ GitHub token configured")
        return True
    
    def print_header(self, title: str):
        """Print a formatted header for examples"""
        print("\n" + "="*60)
        print(title)
        print("="*60)
    
    def print_result_summary(self, result: Any, title: str = "Result Summary"):
        """Print a formatted result summary"""
        print(f"\n📊 {title}")
        print("-" * 40)
        
        if isinstance(result, str):
            print(f"Result: {result}")
        elif isinstance(result, dict):
            self._print_dict_summary(result)
        else:
            print(f"Unexpected result type: {type(result)}")
            print(f"Result: {result}")
    
    def _print_dict_summary(self, data: Dict[str, Any]):
        """Print a formatted dictionary summary"""
        if 'total_updates' in data:
            print(f"📊 Found {data.get('total_updates', 0)} EPIC updates")
        
        if 'repo' in data:
            print(f"📁 Repository: {data.get('repo', 'N/A')}")
        
        if 'days_back' in data:
            print(f"📅 Period: Last {data.get('days_back', 0)} days")
        
        if 'issue_numbers' in data:
            print(f"🔢 Issues checked: {data.get('issue_numbers', [])}")
        
        if 'updates' in data:
            self._print_updates_summary(data['updates'])
    
    def _print_updates_summary(self, updates: list):
        """Print a summary of EPIC updates"""
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
    
    def handle_result(self, result: Any, success_message: str = None) -> Optional[Dict]:
        """Handle and validate a result from API calls"""
        if isinstance(result, str):
            print(f"❌ Error: {result}")
            
            # Provide helpful guidance for common errors
            if "403" in result or "rate limit" in result.lower():
                print("\n💡 Rate limit or permission error detected:")
                print("   - Set GITHUB_TOKEN environment variable")
                print("   - Wait for rate limit to reset (usually 1 hour)")
                print("   - Use a public repository for testing")
                print("   - Check repository permissions")
            
            return None
        
        if isinstance(result, dict):
            if success_message:
                print(f"✅ {success_message}")
            return result
        
        print(f"❌ Unexpected result type: {type(result)}")
        print(f"Result: {result}")
        return None
    
    def print_tips(self):
        """Print helpful tips for users"""
        print("\n💡 Tips:")
        print("   - Adjust dates in the examples to match your data")
        print("   - Set GITHUB_TOKEN for full functionality")
        print("   - Check the github_mcp.tools.github_tools module for more functions")
        print("   - Use the MCP server for integration with MCP clients")
    
    def run(self):
        """Base run method - should be overridden by subclasses"""
        raise NotImplementedError("Subclasses must implement the run() method")
