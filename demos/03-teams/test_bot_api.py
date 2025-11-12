#!/usr/bin/env python3
"""
Test Teams Bot - Simulates Bot Framework Emulator requests
"""

import asyncio
import json
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import aiohttp
from aiohttp import web


async def test_bot():
    """Test the Teams bot with sample messages"""
    print("=" * 70)
    print("🧪 Testing Teams Bot")
    print("=" * 70)
    print()
    
    bot_url = "http://localhost:3978/api/messages"
    
    # Test messages
    test_cases = [
        {
            "name": "Help Command",
            "message": {
                "type": "message",
                "text": "/help",
                "from": {"id": "test-user-1", "name": "Test User"},
                "conversation": {"id": "test-conv-1"},
                "recipient": {"id": "bot", "name": "Genie Bot"},
                "channelId": "emulator"
            }
        },
        {
            "name": "Genie Query",
            "message": {
                "type": "message",
                "text": "What was Q4 revenue?",
                "from": {"id": "test-user-2", "name": "Test User"},
                "conversation": {"id": "test-conv-2"},
                "recipient": {"id": "bot", "name": "Genie Bot"},
                "channelId": "emulator"
            }
        }
    ]
    
    async with aiohttp.ClientSession() as session:
        for i, test_case in enumerate(test_cases, 1):
            print(f"{i}. Testing: {test_case['name']}")
            print(f"   Message: {test_case['message']['text']}")
            
            try:
                async with session.post(
                    bot_url,
                    json=test_case['message'],
                    headers={"Content-Type": "application/json"},
                    timeout=aiohttp.ClientTimeout(total=30)
                ) as response:
                    status = response.status
                    print(f"   Status: {status}")
                    
                    if status == 200:
                        print("   ✅ Bot responded successfully!")
                    else:
                        text = await response.text()
                        print(f"   ⚠️  Response: {text[:100]}")
                    
            except aiohttp.ClientConnectorError:
                print("   ❌ Could not connect to bot")
                print("   Make sure bot is running: python test_teams_bot.py")
                return False
            except Exception as e:
                print(f"   ❌ Error: {str(e)[:100]}")
            
            print()
    
    print("=" * 70)
    print("✅ Test complete!")
    print("=" * 70)
    print()
    print("💡 Note: Bot Framework Emulator uses proper authentication")
    print("   This test verifies the bot is running and accepting requests")
    print()
    print("🚀 To test fully:")
    print("   1. Keep bot running: python test_teams_bot.py")
    print("   2. Open Bot Framework Emulator")
    print("   3. Connect to: http://localhost:3978/api/messages")
    print("   4. Start chatting!")
    
    return True


if __name__ == "__main__":
    try:
        asyncio.run(test_bot())
    except KeyboardInterrupt:
        print("\n\n👋 Test stopped")
    except Exception as e:
        print(f"\n❌ Error: {e}")
        import traceback
        traceback.print_exc()

