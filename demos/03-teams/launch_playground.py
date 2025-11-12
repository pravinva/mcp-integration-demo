#!/usr/bin/env python3
"""
Quick script to install and launch Agents Playground
"""

import subprocess
import sys
import os

def check_npm():
    """Check if npm is installed"""
    try:
        result = subprocess.run(['npm', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ npm found (version {result.stdout.strip()})")
            return True
    except:
        pass
    print("❌ npm not found")
    print("   Install Node.js from: https://nodejs.org/")
    return False

def check_agents_playground():
    """Check if Agents Playground is installed"""
    try:
        result = subprocess.run(['agentsplayground', '--version'], capture_output=True, text=True)
        if result.returncode == 0:
            print(f"✅ Agents Playground installed")
            return True
    except:
        pass
    print("⚠️  Agents Playground not installed")
    return False

def install_agents_playground():
    """Install Agents Playground"""
    print("📥 Installing Agents Playground...")
    print("   This may take a minute...")
    print()
    
    try:
        result = subprocess.run(
            ['npm', 'install', '-g', '@microsoft/m365agentsplayground'],
            capture_output=True,
            text=True
        )
        
        if result.returncode == 0:
            print("✅ Agents Playground installed successfully!")
            return True
        else:
            print("❌ Installation failed:")
            print(result.stderr)
            return False
    except Exception as e:
        print(f"❌ Error: {e}")
        return False

def launch_playground(endpoint="http://localhost:3978/api/messages", channel="emulator"):
    """Launch Agents Playground"""
    cmd = [
        'agentsplayground',
        '-e', endpoint,
        '-c', channel
    ]
    
    print("🚀 Launching Agents Playground...")
    print(f"   Endpoint: {endpoint}")
    print(f"   Channel: {channel}")
    print()
    
    try:
        subprocess.run(cmd)
    except KeyboardInterrupt:
        print("\n\n👋 Agents Playground stopped")
    except Exception as e:
        print(f"❌ Error launching: {e}")

def main():
    print("=" * 70)
    print("🎮 Microsoft 365 Agents Playground Setup")
    print("=" * 70)
    print()
    
    # Check npm
    if not check_npm():
        sys.exit(1)
    
    print()
    
    # Check Agents Playground
    if not check_agents_playground():
        print()
        response = input("Install Agents Playground now? (y/n): ")
        if response.lower() == 'y':
            if not install_agents_playground():
                sys.exit(1)
        else:
            print("\n💡 Install manually:")
            print("   npm install -g @microsoft/m365agentsplayground")
            sys.exit(0)
    
    print()
    print("=" * 70)
    print("🚀 Ready to Launch!")
    print("=" * 70)
    print()
    print("Make sure your bot is running:")
    print("   cd demos/03-teams")
    print("   python test_teams_bot.py")
    print()
    
    response = input("Launch Agents Playground now? (y/n): ")
    if response.lower() == 'y':
        print()
        launch_playground()
    else:
        print()
        print("💡 Launch manually:")
        print("   agentsplayground -e \"http://localhost:3978/api/messages\" -c \"emulator\"")

if __name__ == "__main__":
    main()

