#!/usr/bin/env python3
"""
Test Genie query locally to debug the TaskGroup error.
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from shared.mcp_client import create_mcp_client
from shared.config import GENIE_SPACE_ID
from shared.genie_formatter import format_genie_response

async def test_genie_query():
    """Test Genie query directly"""
    print("=" * 60)
    print("🧪 Testing Genie Query Locally")
    print("=" * 60)
    print()
    
    if not GENIE_SPACE_ID:
        print("❌ GENIE_SPACE_ID not set in .env")
        return
    
    print(f"📊 Genie Space ID: {GENIE_SPACE_ID}")
    print()
    
    try:
        # Create MCP client
        print("1. Creating MCP client...")
        mcp_client = create_mcp_client()
        print("   ✅ MCP client created")
        print()
        
        # Test query
        print("2. Querying Genie: 'What was Q4 revenue?'")
        question = "What was Q4 revenue?"
        
        raw_response, conv_id = await mcp_client.ask_genie(
            GENIE_SPACE_ID,
            question,
            None
        )
        
        print(f"   ✅ Got raw response ({len(raw_response)} chars)")
        print(f"   Conversation ID: {conv_id}")
        print()
        
        # Check if it's an error
        if raw_response.startswith("Error:"):
            print("❌ Genie returned an error:")
            print(raw_response)
            return
        
        # Format response
        print("3. Formatting response...")
        formatted = format_genie_response(raw_response, platform="teams")
        print("   ✅ Response formatted")
        print()
        
        print("4. Formatted Response:")
        print("-" * 60)
        print(formatted)
        print("-" * 60)
        print()
        
        print("✅ Test PASSED!")
        
    except Exception as e:
        print(f"❌ Test FAILED: {str(e)}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_genie_query())

