#!/usr/bin/env python3
"""
Test Slack bot locally using Socket Mode

Requirements:
1. Create Slack app at https://api.slack.com/apps
2. Enable Socket Mode
3. Get Bot Token (xoxb-...) and App-Level Token (xapp-...)
4. Add tokens to .env file:
   SLACK_BOT_TOKEN=xoxb-your-bot-token
   SLACK_APP_TOKEN=xapp-your-app-token
5. Install app to workspace
"""

import sys
import asyncio
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from shared.config import SLACK_BOT_TOKEN, SLACK_APP_TOKEN, validate_config

def check_slack_config():
    """Check if Slack is configured"""
    print("=" * 70)
    print("🧪 Slack Bot - Local Test Setup")
    print("=" * 70)
    print()
    
    if not SLACK_BOT_TOKEN:
        print("❌ SLACK_BOT_TOKEN not set in .env")
        print()
        print("📝 Setup Instructions:")
        print("1. Go to https://api.slack.com/apps")
        print("2. Create a new app or select existing")
        print("3. Go to 'OAuth & Permissions' → Add Bot Token Scopes:")
        print("   - app_mentions:read")
        print("   - chat:write")
        print("   - im:read")
        print("   - im:write")
        print("4. Go to 'Socket Mode' → Enable Socket Mode")
        print("5. Create App-Level Token with 'connections:write' scope")
        print("6. Install app to workspace")
        print("7. Copy Bot Token (xoxb-...) and App-Level Token (xapp-...)")
        print("8. Add to .env:")
        print("   SLACK_BOT_TOKEN=xoxb-your-token")
        print("   SLACK_APP_TOKEN=xapp-your-token")
        return False
    
    if not SLACK_APP_TOKEN:
        print("❌ SLACK_APP_TOKEN not set in .env")
        print("   See instructions above for Socket Mode setup")
        return False
    
    print("✅ Slack tokens configured")
    print(f"   Bot Token: {SLACK_BOT_TOKEN[:20]}...")
    print(f"   App Token: {SLACK_APP_TOKEN[:20]}...")
    print()
    
    try:
        validate_config()
        print("✅ Databricks configuration valid")
    except Exception as e:
        print(f"⚠️  Databricks config: {str(e)[:100]}")
        print("   Bot will use mock mode if USE_MOCK_MCP=true")
    
    print()
    print("=" * 70)
    print("🚀 Starting Slack bot...")
    print("=" * 70)
    print()
    print("💡 Test commands:")
    print("   - DM the bot: 'What was Q4 revenue?'")
    print("   - @mention in channel: '@Genie Bot search MCP documentation'")
    print("   - Calculate: '@Genie Bot calculate 50000 Enterprise'")
    print()
    print("Press Ctrl+C to stop")
    print()
    
    return True


if __name__ == "__main__":
    if not check_slack_config():
        sys.exit(1)
    
    # Import and run the bot
    import sys
    sys.path.insert(0, str(Path(__file__).parent))
    from slack_bot import main
    
    try:
        asyncio.run(main())
    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped")

