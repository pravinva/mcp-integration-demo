#!/usr/bin/env python3
"""
Start Everything Script - Teams Bot + Agents Playground
"""

import subprocess
import sys
import time
import os
from pathlib import Path

def check_bot_running():
    """Check if bot is running on port 3978"""
    import socket
    sock = socket.socket(socket.AF_INET, socket.SOCK_STREAM)
    result = sock.connect_ex(('localhost', 3978))
    sock.close()
    return result == 0

def start_bot():
    """Start the Teams bot"""
    project_root = Path(__file__).parent.parent.parent
    bot_dir = project_root / "demos" / "03-teams"
    
    print("🚀 Starting Teams bot...")
    
    # Start bot in background
    import subprocess
    process = subprocess.Popen(
        [
            sys.executable, 
            str(bot_dir / "test_teams_bot.py")
        ],
        cwd=str(bot_dir),
        stdout=subprocess.PIPE,
        stderr=subprocess.PIPE
    )
    
    # Wait for bot to start
    for i in range(10):
        if check_bot_running():
            print("✅ Bot is running on port 3978")
            return process
        time.sleep(1)
    
    print("⚠️  Bot may still be starting...")
    return process

def launch_playground():
    """Launch Agents Playground"""
    print()
    print("🎮 Launching Agents Playground...")
    print("   Endpoint: http://localhost:3978/api/messages")
    print("   Channel: emulator")
    print()
    
    try:
        # Launch Agents Playground
        subprocess.Popen([
            'agentsplayground',
            '-e', 'http://localhost:3978/api/messages',
            '-c', 'emulator'
        ])
        print("✅ Agents Playground launched!")
        print("   Browser should open automatically")
        return True
    except FileNotFoundError:
        print("❌ Agents Playground not found")
        print("   Install: npm install -g @microsoft/m365agentsplayground")
        return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def main():
    print("=" * 70)
    print("🚀 Starting Teams Bot + Agents Playground")
    print("=" * 70)
    print()
    
    # Check Agents Playground
    try:
        result = subprocess.run(['which', 'agentsplayground'], capture_output=True, text=True)
        if result.returncode != 0:
            print("❌ Agents Playground not installed")
            print("   Install: npm install -g @microsoft/m365agentsplayground")
            sys.exit(1)
    except:
        print("❌ Cannot check Agents Playground")
        sys.exit(1)
    
    # Start bot
    bot_process = start_bot()
    
    # Wait a moment
    time.sleep(2)
    
    # Launch playground
    if launch_playground():
        print()
        print("=" * 70)
        print("✅ Everything Started!")
        print("=" * 70)
        print()
        print("💬 Agents Playground should open in your browser")
        print("   If not, open manually:")
        print("   agentsplayground -e \"http://localhost:3978/api/messages\" -c \"emulator\"")
        print()
        print("💡 Try these commands:")
        print("   - What was Q4 revenue?")
        print("   - search MCP tutorial")
        print("   - calculate 50000 Enterprise")
        print("   - /help")
        print()
        print("⚠️  Keep this terminal open!")
        print("   Press Ctrl+C to stop everything")
        print("=" * 70)
        
        try:
            # Keep running
            bot_process.wait()
        except KeyboardInterrupt:
            print("\n\n👋 Stopping...")
            bot_process.terminate()
    else:
        print("\n❌ Failed to launch Agents Playground")
        bot_process.terminate()
        sys.exit(1)

if __name__ == "__main__":
    main()

