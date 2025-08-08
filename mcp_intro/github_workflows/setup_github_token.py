#!/usr/bin/env python3
"""
Helper script to set up GitHub token for testing.
This script provides guidance on creating and configuring a GitHub Personal Access Token.
"""

import os
import sys


def print_setup_instructions():
    """Print step-by-step instructions for setting up GitHub token"""
    print("🚀 GitHub Token Setup Guide")
    print("=" * 50)
    print()
    print("To access private repositories and test full functionality, you need a GitHub Personal Access Token.")
    print()
    print("📋 Step-by-step instructions:")
    print()
    print("1. Go to GitHub.com and sign in to your account")
    print("2. Click your profile picture → Settings")
    print("3. Scroll down to 'Developer settings' in the left sidebar")
    print("4. Click 'Personal access tokens' → 'Tokens (classic)'")
    print("5. Click 'Generate new token' → 'Generate new token (classic)'")
    print("6. Configure the token:")
    print("   • Note: 'MCP GitHub Tools' (or any descriptive name)")
    print("   • Expiration: Choose 30 days, 90 days, or custom")
    print("   • Scopes: Select these checkboxes:")
    print("     ✅ repo (Full control of private repositories)")
    print("     ✅ read:org (Read organization data)")
    print("     ✅ read:user (Read user data)")
    print("7. Click 'Generate token'")
    print("8. Copy the token (you won't see it again!)")
    print()
    print("🔧 Setting the token:")
    print()
    print("Option A - Temporary (current session only):")
    print("   export GITHUB_TOKEN='your-token-here'")
    print()
    print("Option B - Permanent (add to shell profile):")
    print("   echo 'export GITHUB_TOKEN=\"your-token-here\"' >> ~/.zshrc")
    print("   source ~/.zshrc")
    print()
    print("Option C - Project-specific (.env file):")
    print("   echo 'GITHUB_TOKEN=your-token-here' > .env")
    print()
    print("🧪 Testing the setup:")
    print("   python -m pytest tests/test_github_setup.py -v")
    print()


def check_current_token():
    """Check if GitHub token is currently set"""
    token = os.getenv('GITHUB_TOKEN')
    
    if token:
        print("✅ GitHub token is currently set")
        print(f"   Token: {token[:8]}...{token[-4:] if len(token) > 12 else '***'}")
        return True
    else:
        print("❌ GitHub token is not set")
        print("   Set GITHUB_TOKEN environment variable to enable full testing")
        return False


def main():
    """Main function"""
    print_setup_instructions()
    
    print("🔍 Current status:")
    has_token = check_current_token()
    
    if has_token:
        print("\n💡 You can now run tests with full functionality:")
        print("   python -m pytest tests/ -v")
        print("\n💡 Or test specific functionality:")
        print("   python -m pytest tests/test_github_setup.py::TestPrivateRepositoryAccess -v")
    else:
        print("\n💡 For now, you can run tests that work without a token:")
        print("   python -m pytest tests/test_github_setup.py::TestPublicRepositoryAccess -v")
        print("\n💡 Set up a token to test private repository access and full functionality.")


if __name__ == "__main__":
    main()
