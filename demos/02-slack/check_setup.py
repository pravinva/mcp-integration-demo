#!/usr/bin/env python3
"""
Slack App Setup Verification Script

This script helps verify your Slack app is configured correctly.
Run this BEFORE starting the bot to catch configuration issues early.
"""

import sys
import os
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def check_env_file():
    """Check if .env file exists and has required variables"""
    print("=" * 70)
    print("🔍 Slack App Configuration Checker")
    print("=" * 70)
    print()
    
    env_file = project_root / ".env"
    
    if not env_file.exists():
        print("❌ .env file not found!")
        print()
        print("📝 Create .env file in project root:")
        print(f"   {env_file}")
        print()
        print("Add these lines:")
        print("   SLACK_BOT_TOKEN=xoxb-your-token")
        print("   SLACK_APP_TOKEN=xapp-your-token")
        print("   GENIE_SPACE_ID=your-space-id")
        return False
    
    print("✅ .env file found")
    
    # Load .env
    from dotenv import load_dotenv
    load_dotenv(env_file)
    
    # Check tokens
    bot_token = os.getenv("SLACK_BOT_TOKEN")
    app_token = os.getenv("SLACK_APP_TOKEN")
    genie_space = os.getenv("GENIE_SPACE_ID")
    
    print()
    print("Checking tokens...")
    print("-" * 70)
    
    # Check Bot Token
    if not bot_token:
        print("❌ SLACK_BOT_TOKEN not set")
        print("   Get it from: https://api.slack.com/apps → Your App → OAuth & Permissions")
    elif not bot_token.startswith("xoxb-"):
        print(f"⚠️  SLACK_BOT_TOKEN format looks wrong (starts with: {bot_token[:5]})")
        print("   Bot tokens should start with 'xoxb-'")
    else:
        print(f"✅ SLACK_BOT_TOKEN: {bot_token[:20]}...")
    
    # Check App Token
    if not app_token:
        print("❌ SLACK_APP_TOKEN not set")
        print("   Get it from: https://api.slack.com/apps → Your App → Socket Mode")
    elif not app_token.startswith("xapp-"):
        print(f"⚠️  SLACK_APP_TOKEN format looks wrong (starts with: {app_token[:5]})")
        print("   App tokens should start with 'xapp-'")
    else:
        print(f"✅ SLACK_APP_TOKEN: {app_token[:20]}...")
    
    # Check Genie Space
    if not genie_space:
        print("⚠️  GENIE_SPACE_ID not set")
        print("   Bot will use mock mode if USE_MOCK_MCP=true")
    else:
        print(f"✅ GENIE_SPACE_ID: {genie_space}")
    
    print()
    print("=" * 70)
    
    # Summary
    all_good = (
        bot_token and bot_token.startswith("xoxb-") and
        app_token and app_token.startswith("xapp-")
    )
    
    if all_good:
        print("✅ Configuration looks good!")
        print()
        print("🚀 Ready to start bot:")
        print("   python demos/02-slack/slack_bot.py")
        print()
        print("Or use test script:")
        print("   python demos/02-slack/test_slack_bot.py")
    else:
        print("❌ Configuration incomplete")
        print()
        print("📚 See setup guide:")
        print("   demos/02-slack/SLACK_SETUP.md")
        print()
        print("Or quick steps:")
        print("1. Go to https://api.slack.com/apps")
        print("2. Create app → Enable Socket Mode → Get tokens")
        print("3. Add tokens to .env file")
    
    print("=" * 70)
    
    return all_good


def print_setup_links():
    """Print helpful setup links"""
    print()
    print("🔗 Quick Links:")
    print("-" * 70)
    print("📱 Slack Apps:        https://api.slack.com/apps")
    print("📖 Socket Mode:       https://api.slack.com/apis/connections/socket")
    print("📚 OAuth Scopes:      https://api.slack.com/scopes")
    print("📝 Setup Guide:       demos/02-slack/SLACK_SETUP.md")
    print("-" * 70)


if __name__ == "__main__":
    try:
        check_env_file()
        print_setup_links()
    except ImportError as e:
        print("❌ Missing dependency:")
        print(f"   {e}")
        print()
        print("💡 Install dependencies:")
        print("   pip install python-dotenv")
        sys.exit(1)
    except Exception as e:
        print(f"❌ Error: {e}")
        import traceback
        traceback.print_exc()
        sys.exit(1)

