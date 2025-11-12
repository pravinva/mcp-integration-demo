#!/usr/bin/env python3
"""
Simple test script for Teams bot when Agents Playground has issues.
Tests the bot directly via HTTP requests.
"""

import requests
import json
import sys

BOT_URL = "http://localhost:3978/api/messages"

def test_bot(question):
    """Send a test message to the bot"""
    payload = {
        "type": "message",
        "text": question,
        "from": {
            "id": "test-user-123",
            "name": "Test User"
        },
        "conversation": {
            "id": "test-conversation-123"
        },
        "recipient": {
            "id": "bot-id",
            "name": "Genie Bot"
        },
        "channelId": "emulator"
    }
    
    try:
        response = requests.post(
            BOT_URL,
            json=payload,
            headers={"Content-Type": "application/json"}
        )
        
        print(f"Status: {response.status_code}")
        if response.status_code == 200:
            print("✅ Bot responded successfully!")
        else:
            print(f"Response: {response.text}")
            
    except Exception as e:
        print(f"❌ Error: {e}")

if __name__ == "__main__":
    print("=" * 60)
    print("🧪 Testing Teams Bot (Direct HTTP)")
    print("=" * 60)
    print()
    
    if len(sys.argv) > 1:
        question = " ".join(sys.argv[1:])
    else:
        question = "What tables are available?"
    
    print(f"Question: {question}")
    print()
    test_bot(question)
    print()
    print("=" * 60)
    print("💡 Note: Agents Playground has Node.js 25 compatibility issues.")
    print("   You can test the bot via:")
    print("   1. Direct HTTP requests (this script)")
    print("   2. Bot Framework Emulator (if installed)")
    print("   3. Deploy to Azure and test in real Teams")
    print("=" * 60)

