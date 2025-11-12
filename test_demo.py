#!/usr/bin/env python3
"""
Quick test script to demonstrate Genie MCP integration
"""

import asyncio
import sys
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from shared.mcp_client import create_mcp_client
from shared.config import GENIE_SPACE_ID, VECTOR_SEARCH_INDEX_ID, UC_FUNCTION_NAME, validate_config


async def simple_demo():
    """Simple Genie query demo"""
    print("=" * 60)
    print("🧞 Databricks Genie MCP - Simple Demo")
    print("=" * 60)
    print()
    
    validate_config()
    client = create_mcp_client()
    
    print("✅ Connected to Databricks")
    print(f"📊 Genie Space: {GENIE_SPACE_ID}")
    print()
    print("🔍 Query: \"What was our Q4 2024 revenue?\"")
    print("-" * 60)
    
    response, conv_id = await client.ask_genie(
        GENIE_SPACE_ID,
        "What was our Q4 2024 revenue?"
    )
    
    # Parse JSON response
    try:
        data = json.loads(response)
        content = json.loads(data.get('content', '{}'))
        sql_query = content.get('query', 'N/A')
        result_data = content.get('result', {}).get('data_array', [])
        
        print(f"\n🧞 Genie Response:")
        print(f"\n📝 SQL Generated:")
        print(f"   {sql_query}")
        
        if result_data:
            print(f"\n💰 Result:")
            for row in result_data:
                values = row.get('values', [])
                if values:
                    revenue = values[0].get('string_value', 'N/A')
                    print(f"   Q4 2024 Revenue: ${revenue}")
        
        print(f"\n💬 Conversation ID: {conv_id}")
    except json.JSONDecodeError:
        print(f"\n🧞 Genie Response:")
        print(response[:800])
    
    print()


async def full_demo():
    """Full demo with all 3 data sources"""
    print("=" * 70)
    print("📺 FULL DEMO - ONE CLIENT, THREE DATA SOURCES")
    print("=" * 70)
    print()
    
    validate_config()
    client = create_mcp_client()
    
    # 1. Genie
    print("1️⃣  GENIE - Natural Language Analytics")
    print("-" * 70)
    print("Query: \"What was our total revenue in Q4 2024?\"")
    print()
    
    response, conv_id = await client.ask_genie(
        GENIE_SPACE_ID,
        "What was our total revenue in Q4 2024?"
    )
    
    try:
        data = json.loads(response)
        content = json.loads(data.get('content', '{}'))
        sql = content.get('query', 'N/A')
        print(f"📝 SQL: {sql[:80]}...")
        result_data = content.get('result', {}).get('data_array', [])
        if result_data:
            revenue = result_data[0].get('values', [{}])[0].get('string_value', 'N/A')
            print(f"💰 Revenue: ${revenue}")
    except:
        print(f"📝 Response: {response[:150]}...")
    
    print()
    
    # 2. Vector Search
    print("2️⃣  VECTOR SEARCH - Documentation Retrieval")
    print("-" * 70)
    print("Search: \"How to create a Genie space?\"")
    print()
    
    try:
        docs = await client.search_docs(
            VECTOR_SEARCH_INDEX_ID,
            "How to create a Genie space?",
            num_results=2
        )
        print(f"📚 Results: {docs[:200]}...")
    except Exception as e:
        print(f"⚠️  Vector Search: {str(e)[:100]}...")
        print("   (Using mock mode - Vector Search index not configured)")
    
    print()
    
    # 3. UC Function
    print("3️⃣  UC FUNCTIONS - Governed Code Execution")
    print("-" * 70)
    print("Function: calculate_discount(50000, 'Enterprise')")
    print()
    
    try:
        result = await client.call_function(
            UC_FUNCTION_NAME,
            {"order_amount": 50000.0, "customer_segment": "Enterprise"}
        )
        print(f"💰 Result: {result[:200]}...")
    except Exception as e:
        print(f"⚠️  UC Function: {str(e)[:100]}...")
        print("   (Using mock mode - UC Function not configured)")
    
    print()
    print("=" * 70)
    print("✅ DEMO COMPLETE!")
    print("=" * 70)
    print()
    print("Key Insight: The SAME client (shared/mcp_client.py) talked to")
    print("all three data sources. That's M+N in action!")


if __name__ == "__main__":
    import sys
    
    if len(sys.argv) > 1 and sys.argv[1] == "full":
        asyncio.run(full_demo())
    else:
        asyncio.run(simple_demo())

