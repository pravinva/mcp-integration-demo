#!/usr/bin/env python3
"""
Quick script to help download Bot Framework Emulator for Mac
"""

import webbrowser
import subprocess
import sys

print("=" * 70)
print("📥 Bot Framework Emulator - Mac Download Helper")
print("=" * 70)
print()

# Check for Homebrew
try:
    result = subprocess.run(['which', 'brew'], capture_output=True, text=True)
    if result.returncode == 0:
        print("✅ Homebrew detected!")
        print()
        print("🚀 Quick Install Option:")
        print("   brew install --cask botframework-emulator")
        print()
        response = input("Install via Homebrew now? (y/n): ")
        if response.lower() == 'y':
            print()
            print("Running: brew install --cask botframework-emulator")
            subprocess.run(['brew', 'install', '--cask', 'botframework-emulator'])
            print()
            print("✅ Installation complete!")
            print("   Launch Bot Framework Emulator from Applications")
            sys.exit(0)
except:
    pass

print("📥 Opening GitHub Releases page...")
print()
print("On the page that opens:")
print("1. Scroll down to 'Assets' section")
print("2. Download the file ending in '.dmg'")
print("3. Open the .dmg file")
print("4. Drag Bot Framework Emulator to Applications")
print()

# Open browser
url = "https://github.com/microsoft/BotFramework-Emulator/releases/latest"
webbrowser.open(url)

print("✅ Browser opened!")
print()
print("💡 After downloading:")
print("   1. Open the .dmg file")
print("   2. Drag to Applications")
print("   3. Launch Bot Framework Emulator")
print("   4. Connect to: http://localhost:3978/api/messages")
print()

