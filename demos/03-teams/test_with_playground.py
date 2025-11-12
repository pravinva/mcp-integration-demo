"""
Quick test script for Teams bot with Agents Playground.

This script:
1. Checks configuration
2. Starts the bot
3. Provides instructions for Agents Playground
"""

import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from shared.config import (
    GENIE_SPACE_ID,
    DATABRICKS_HOST,
    get_workspace_client
)

def check_config():
    """Check if configuration is valid"""
    print("=" * 60)
    print("🔍 Checking Configuration...")
    print("=" * 60)
    
    issues = []
    
    # Check Genie Space ID
    if not GENIE_SPACE_ID:
        issues.append("❌ GENIE_SPACE_ID not set in .env")
    else:
        print(f"✅ Genie Space ID: {GENIE_SPACE_ID}")
    
    # Check Databricks host
    if not DATABRICKS_HOST:
        issues.append("❌ DATABRICKS_HOST not set in .env")
    else:
        print(f"✅ Databricks Host: {DATABRICKS_HOST}")
    
    # Check authentication
    try:
        workspace_client = get_workspace_client()
        current_user = workspace_client.current_user.me()
        print(f"✅ Authenticated as: {current_user.user_name}")
    except Exception as e:
        issues.append(f"❌ Authentication failed: {e}")
    
    print()
    
    if issues:
        print("⚠️ Configuration Issues:")
        for issue in issues:
            print(f"  {issue}")
        print()
        print("Please fix these issues in your .env file:")
        print("  DATABRICKS_HOST=https://your-workspace.cloud.databricks.com")
        print("  GENIE_SPACE_ID=01f0be3dcc771e60ada71b6ec9f61870")
        print("  DATABRICKS_TOKEN=your-token")
        return False
    
    print("✅ All configuration checks passed!")
    print()
    return True


def print_instructions():
    """Print instructions for using Agents Playground"""
    print("=" * 60)
    print("🚀 Teams Bot Ready for Agents Playground!")
    print("=" * 60)
    print()
    print("📋 Next Steps:")
    print()
    print("1. Make sure Agents Playground is installed:")
    print("   npm install -g @microsoft/m365agentsplayground")
    print()
    print("2. In ANOTHER terminal, launch Agents Playground:")
    print("   agentsplayground -e \"http://localhost:3978/api/messages\" -c \"emulator\"")
    print()
    print("3. The browser will open automatically!")
    print()
    print("4. Start chatting with your bot!")
    print()
    print("=" * 60)
    print("🤖 Starting Teams Bot...")
    print("=" * 60)
    print()
    print("📍 Bot will listen on: http://localhost:3978/api/messages")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60)
    print()


if __name__ == "__main__":
    if not check_config():
        sys.exit(1)
    
    print_instructions()
    
    # Import and run the bot
    from teams_bot import init_func
    from aiohttp import web
    
    app = init_func()
    port = 3978
    
    web.run_app(app, port=port)

