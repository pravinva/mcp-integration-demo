"""
Simplified Teams bot for testing with Bot Framework Emulator.
No authentication needed for local testing.

Download Bot Framework Emulator:
https://github.com/Microsoft/BotFramework-Emulator/releases
"""

import sys
sys.path.append('../..')

# Just import and run the main bot
from teams_bot import init_func, web

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Teams Bot - Emulator Test Mode")
    print("=" * 60)
    print()
    print("✅ No Azure credentials needed for testing!")
    print()
    print("Steps to test:")
    print("1. Open Bot Framework Emulator")
    print("2. Click 'Open Bot'")
    print("3. Enter: http://localhost:3978/api/messages")
    print("4. Leave App ID and Password empty")
    print("5. Click 'Connect'")
    print("6. Start chatting!")
    print()
    print("=" * 60)
    
    app = init_func()
    web.run_app(app, port=3978)

