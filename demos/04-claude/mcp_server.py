"""
MCP server for Claude Desktop.

This exposes Databricks services to Claude using MCP protocol.
Claude can automatically discover and use these tools!

Configure in Claude Desktop:
Mac: ~/Library/Application Support/Claude/claude_desktop_config.json
Windows: %APPDATA%\Claude\claude_desktop_config.json
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

import asyncio
from mcp.server import Server
from mcp.server.stdio import stdio_server
from mcp.types import Tool, TextContent

from shared.mcp_client import create_mcp_client
from shared.config import GENIE_SPACE_ID, VECTOR_SEARCH_INDEX_ID, UC_FUNCTION_NAME

# Create MCP server
app = Server("databricks-genie")

# Initialize our MCP client (reuses shared code!)
mcp_client = create_mcp_client()


@app.list_tools()
async def list_tools() -> list[Tool]:
    """
    Tell Claude what tools are available.
    Claude will automatically choose the right tool based on user's question!
    """
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
    """
    Execute tool calls from Claude.
    Uses our shared MCP client!
    """
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
        return [TextContent(type="text", text=f"Error: {str(e)}")]


async def main():
    """Run the MCP server"""
    async with stdio_server() as (read_stream, write_stream):
        await app.run(read_stream, write_stream, app.create_initialization_options())


if __name__ == "__main__":
    print("🚀 Starting Databricks MCP Server for Claude Desktop...")
    asyncio.run(main())

