#!/usr/bin/env python3
"""
Test Teams bot with Bot Framework Emulator

Requirements:
1. Download Bot Framework Emulator:
   https://github.com/Microsoft/BotFramework-Emulator/releases
2. No Azure credentials needed for local testing!
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from shared.config import validate_config

def check_teams_config():
    """Check configuration and print instructions"""
    print("=" * 70)
    print("🧪 Teams Bot - Emulator Test Setup")
    print("=" * 70)
    print()
    
    try:
        validate_config()
        print("✅ Databricks configuration valid")
    except Exception as e:
        print(f"⚠️  Databricks config: {str(e)[:100]}")
        print("   Bot will use mock mode if USE_MOCK_MCP=true")
    
    print()
    print("=" * 70)
    print("📥 Setup Instructions:")
    print("=" * 70)
    print()
    print("1. Install Microsoft 365 Agents Playground:")
    print("   npm install -g @microsoft/m365agentsplayground")
    print("   (Bot Framework Emulator is deprecated - use Agents Playground instead)")
    print()
    print("2. Start this bot (will run on port 3978)")
    print()
    print("3. Launch Agents Playground:")
    print("   agentsplayground -e \"http://localhost:3978/api/messages\" -c \"emulator\"")
    print()
    print("4. Browser will open automatically")
    print()
    print("5. Start chatting!")
    print()
    print("=" * 70)
    print("💡 Test Commands:")
    print("=" * 70)
    print()
    print("📊 Analytics (Genie):")
    print("   'What was Q4 revenue?'")
    print("   'Show me top 5 customers'")
    print()
    print("🔍 Search Docs (Vector Search):")
    print("   'search how to create Genie space'")
    print("   'search MCP tutorial'")
    print()
    print("💰 Calculate (UC Functions):")
    print("   'calculate 50000 Enterprise'")
    print("   'calculate 25000 SMB'")
    print()
    print("⚙️ Commands:")
    print("   '/help' - Show help")
    print("   '/reset' - Reset conversation")
    print()
    print("=" * 70)
    print("🚀 Starting Teams bot...")
    print("=" * 70)
    print()
    print("📍 Bot running on: http://localhost:3978/api/messages")
    print()
    print("Press Ctrl+C to stop")
    print()
    
    return True


if __name__ == "__main__":
    if not check_teams_config():
        sys.exit(1)
    
    # Import and run the bot
    sys.path.insert(0, str(Path(__file__).parent))
    from teams_bot import init_func
    from aiohttp import web
    
    app = init_func()
    web.run_app(app, port=3978)

