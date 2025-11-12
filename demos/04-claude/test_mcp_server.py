#!/usr/bin/env python3
"""
Test Claude MCP Server locally (without Claude Desktop)

This simulates what Claude Desktop would do - useful for debugging.
"""

import sys
import asyncio
import json
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from shared.mcp_client import create_mcp_client
from shared.config import GENIE_SPACE_ID, VECTOR_SEARCH_INDEX_ID, UC_FUNCTION_NAME, validate_config

# Create MCP server (same as mcp_server.py)
app = Server("databricks-genie")
mcp_client = create_mcp_client()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """List available tools"""
    return [
        Tool(
            name="ask_genie",
            description="Query Databricks Genie for data analytics. Use for questions about revenue, customers, orders, and business metrics.",
            inputSchema={
                "type": "object",
                "properties": {
                    "question": {
                        "type": "string",
                        "description": "Natural language question about the data"
                    }
                },
                "required": ["question"]
            }
        ),
        Tool(
            name="search_docs",
            description="Search documentation using Vector Search. Use for finding guides, tutorials, and technical documentation.",
            inputSchema={
                "type": "object",
                "properties": {
                    "query": {
                        "type": "string",
                        "description": "Search query"
                    },
                    "num_results": {
                        "type": "integer",
                        "description": "Number of results to return",
                        "default": 3
                    }
                },
                "required": ["query"]
            }
        ),
        Tool(
            name="calculate_discount",
            description="Calculate customer discount based on order amount and segment. Segments: Enterprise, Mid-Market, SMB.",
            inputSchema={
                "type": "object",
                "properties": {
                    "order_amount": {
                        "type": "number",
                        "description": "Order amount in dollars"
                    },
                    "customer_segment": {
                        "type": "string",
                        "description": "Customer segment: Enterprise, Mid-Market, or SMB"
                    }
                },
                "required": ["order_amount", "customer_segment"]
            }
        )
    ]


@app.call_tool()
async def call_tool(name: str, arguments: dict) -> list[TextContent]:
    """Execute tool calls"""
    try:
        if name == "ask_genie":
            response, _ = await mcp_client.ask_genie(
                GENIE_SPACE_ID,
                arguments["question"]
            )
            return [TextContent(type="text", text=response)]
        
        elif name == "search_docs":
            response = await mcp_client.search_docs(
                VECTOR_SEARCH_INDEX_ID,
                arguments["query"],
                arguments.get("num_results", 3)
            )
            return [TextContent(type="text", text=response)]
        
        elif name == "calculate_discount":
            response = await mcp_client.call_function(
                UC_FUNCTION_NAME,
                {
                    "order_amount": arguments["order_amount"],
                    "customer_segment": arguments["customer_segment"]
                }
            )
            return [TextContent(type="text", text=response)]
        
        else:
            return [TextContent(type="text", text=f"Unknown tool: {name}")]
    
    except Exception as e:
        import traceback
        error_msg = f"Error: {str(e)}\n{traceback.format_exc()}"
        return [TextContent(type="text", text=error_msg)]


async def test_tools():
    """Test all tools manually"""
    print("=" * 70)
    print("🧪 Testing Claude MCP Server Tools")
    print("=" * 70)
    print()
    
    # Validate config
    try:
        validate_config()
        print("✅ Configuration valid")
    except Exception as e:
        print(f"❌ Configuration error: {e}")
        return
    
    print()
    
    # Test 1: List tools
    print("1️⃣  Listing available tools...")
    tools = await list_tools()
    for tool in tools:
        print(f"   ✅ {tool.name}: {tool.description[:60]}...")
    print()
    
    # Test 2: Ask Genie
    print("2️⃣  Testing ask_genie...")
    try:
        result = await call_tool("ask_genie", {"question": "What was Q4 revenue?"})
        print(f"   ✅ Response: {result[0].text[:100]}...")
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
    print()
    
    # Test 3: Search docs
    print("3️⃣  Testing search_docs...")
    try:
        result = await call_tool("search_docs", {"query": "How to create Genie space?", "num_results": 2})
        print(f"   ✅ Response: {result[0].text[:100]}...")
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
    print()
    
    # Test 4: Calculate discount
    print("4️⃣  Testing calculate_discount...")
    try:
        result = await call_tool("calculate_discount", {"order_amount": 50000, "customer_segment": "Enterprise"})
        print(f"   ✅ Response: {result[0].text[:100]}...")
    except Exception as e:
        print(f"   ❌ Error: {str(e)[:100]}")
    print()
    
    print("=" * 70)
    print("✅ All tests complete!")
    print("=" * 70)
    print()
    print("💡 To use with Claude Desktop:")
    print("   1. Copy claude_config.json to Claude Desktop config location")
    print("   2. Update the path in 'args' to your actual path")
    print("   3. Update GENIE_SPACE_ID in 'env'")
    print("   4. Restart Claude Desktop")


if __name__ == "__main__":
    asyncio.run(test_tools())

