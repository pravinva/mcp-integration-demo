#!/usr/bin/env python3
"""
Quick Start Script for Teams Bot with Emulator

This script:
1. Checks if Bot Framework Emulator is installed
2. Verifies configuration
3. Starts the bot
4. Provides connection instructions
"""

import sys
import os
import subprocess
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

def check_port_available(port=3978):
    """Check if port is available"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', port))
    sock.close()
    return result != 0

def check_emulator_installed():
    """Check if Bot Framework Emulator might be installed"""
    # Common installation locations
    possible_paths = [
        "/Applications/Bot Framework Emulator.app",  # Mac
        os.path.expanduser("~/AppData/Local/Microsoft/Bot Framework Emulator"),  # Windows
        os.path.expanduser("~/.local/share/Bot Framework Emulator"),  # Linux
    ]
    
    for path in possible_paths:
        if os.path.exists(path):
            return True, path
    
    return False, None

def print_instructions():
    """Print connection instructions"""
    print()
    print("=" * 70)
    print("📥 Connection Instructions")
    print("=" * 70)
    print()
    print("1. Launch Agents Playground:")
    print("   agentsplayground -e \"http://localhost:3978/api/messages\" -c \"emulator\"")
    print()
    print("2. Browser will open automatically")
    print()
    print("3. Start chatting!")
    print()
    print("=" * 70)
    print("💡 Try these commands:")
    print("=" * 70)
    print()
    print("📊 Analytics:")
    print("   'What was Q4 revenue?'")
    print()
    print("🔍 Search:")
    print("   'search MCP tutorial'")
    print()
    print("💰 Calculate:")
    print("   'calculate 50000 Enterprise'")
    print()
    print("⚙️ Commands:")
    print("   '/help' or '/reset'")
    print()
    print("=" * 70)

def main():
    print("=" * 70)
    print("🤖 Teams Bot - Quick Start")
    print("=" * 70)
    print()
    
    # Check configuration
    try:
        from shared.config import validate_config, GENIE_SPACE_ID
        validate_config()
        print("✅ Databricks configuration valid")
        print(f"   Genie Space: {GENIE_SPACE_ID}")
    except Exception as e:
        print(f"⚠️  Databricks config: {str(e)[:100]}")
        print("   Bot will use mock mode if USE_MOCK_MCP=true")
        print("   Or set GENIE_SPACE_ID in .env")
    
    print()
    
    # Check port
    if not check_port_available():
        print("⚠️  Port 3978 is already in use!")
        print("   Another bot might be running, or another app is using this port")
        print("   You can:")
        print("   1. Stop the other app")
        print("   2. Or modify teams_bot.py to use a different port")
        response = input("\n   Continue anyway? (y/n): ")
        if response.lower() != 'y':
            return
    else:
        print("✅ Port 3978 is available")
    
    print()
    
    # Check Agents Playground
    try:
        result = subprocess.run(['which', 'agentsplayground'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Agents Playground found")
        else:
            print("⚠️  Agents Playground not installed")
            print("   Install: npm install -g @microsoft/m365agentsplayground")
            print("   (Bot Framework Emulator is deprecated - use Agents Playground)")
    except:
        print("⚠️  Agents Playground not detected")
        print("   Install: npm install -g @microsoft/m365agentsplayground")
    
    print()
    print("=" * 70)
    print("🚀 Starting Teams bot...")
    print("=" * 70)
    print()
    print("📍 Bot will run on: http://localhost:3978/api/messages")
    print()
    print("⚠️  Keep this window open!")
    print("   The bot needs to keep running to receive messages.")
    print()
    print("Press Ctrl+C to stop the bot")
    print()
    
    print_instructions()
    
    print()
    print("=" * 70)
    print("Starting bot server...")
    print("=" * 70)
    print()
    
    # Import and run
    sys.path.insert(0, str(Path(__file__).parent))
    from teams_bot import init_func
    from aiohttp import web
    
    app = init_func()
    
    try:
        web.run_app(app, port=3978)
    except KeyboardInterrupt:
        print("\n\n👋 Bot stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    main()

