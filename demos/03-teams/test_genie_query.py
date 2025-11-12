#!/usr/bin/env python3
"""
Quick test script to debug Genie query issues
"""

import sys
from pathlib import Path
import asyncio
import logging

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

# Enable detailed logging
logging.basicConfig(
    level=logging.DEBUG,
    format='%(asctime)s - %(name)s - %(levelname)s - %(message)s'
)

from shared.mcp_client import create_mcp_client
from shared.config import GENIE_SPACE_ID

async def test_genie():
    """Test a simple Genie query"""
    print("=" * 70)
    print("🧪 Testing Genie Query")
    print("=" * 70)
    print()

    if not GENIE_SPACE_ID:
        print("❌ GENIE_SPACE_ID not set in environment")
        print("Set it in .env file or export GENIE_SPACE_ID=your_space_id")
        return

    print(f"📊 Genie Space ID: {GENIE_SPACE_ID}")
    print()

    # Create MCP client
    print("Creating MCP client...")
    try:
        mcp_client = create_mcp_client()
        print("✅ MCP client created")
    except Exception as e:
        print(f"❌ Failed to create MCP client: {e}")
        import traceback
        traceback.print_exc()
        return

    # Test query
    test_question = "What tables are available?"
    print(f"\n🔍 Testing query: '{test_question}'")
    print()

    try:
        print("Calling ask_genie()...")
        response, conv_id = await mcp_client.ask_genie(
            GENIE_SPACE_ID,
            test_question,
            None
        )

        print()
        print("=" * 70)
        print("✅ SUCCESS!")
        print("=" * 70)
        print()
        print(f"Response: {response[:200]}...")
        print(f"Conversation ID: {conv_id}")

    except Exception as e:
        print()
        print("=" * 70)
        print("❌ ERROR!")
        print("=" * 70)
        print()
        print(f"Error: {e}")
        print()
        print("Full traceback:")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_genie())
