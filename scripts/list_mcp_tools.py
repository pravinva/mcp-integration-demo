#!/usr/bin/env python3
"""
List available tools for each MCP server
"""

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from shared.config import get_workspace_client, GENIE_SPACE_ID, VECTOR_SEARCH_INDEX_ID, UC_FUNCTION_NAME, DATABRICKS_HOST
from databricks_mcp import DatabricksMCPClient

def list_tools(name, url):
    """List tools available on an MCP server"""
    try:
        client = get_workspace_client()
        mcp = DatabricksMCPClient(server_url=url, workspace_client=client)
        tools = mcp.list_tools()
        print(f'\n✅ {name}:')
        print(f'   URL: {url}')
        print(f'   Tools ({len(tools)}):')
        for tool in tools:
            print(f'      - {tool.name}: {tool.description or "No description"}')
            if hasattr(tool, 'inputSchema') and tool.inputSchema:
                print(f'        Parameters: {tool.inputSchema}')
        return tools
    except Exception as e:
        print(f'\n❌ {name}: Error listing tools')
        print(f'   Error: {str(e)}')
        import traceback
        traceback.print_exc()
        return []

print('🔍 Listing MCP Server Tools...')
print('=' * 70)

workspace_host = DATABRICKS_HOST or get_workspace_client().config.host

# List Genie tools
genie_url = f'{workspace_host}/api/2.0/mcp/genie/{GENIE_SPACE_ID}'
list_tools('Genie MCP', genie_url)

# List Vector Search tools
vs_parts = VECTOR_SEARCH_INDEX_ID.split('.')
if len(vs_parts) >= 2:
    vs_url = f'{workspace_host}/api/2.0/mcp/vector-search/{vs_parts[0]}/{vs_parts[1]}'
    list_tools('Vector Search MCP', vs_url)

# List UC Functions tools
uc_parts = UC_FUNCTION_NAME.split('.')
if len(uc_parts) >= 2:
    uc_url = f'{workspace_host}/api/2.0/mcp/functions/{uc_parts[0]}/{uc_parts[1]}'
    list_tools('UC Functions MCP', uc_url)

print('\n' + '=' * 70)

