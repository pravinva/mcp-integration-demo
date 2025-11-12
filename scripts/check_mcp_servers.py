#!/usr/bin/env python3
"""
Check MCP server availability and configuration
"""

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from shared.config import get_workspace_client, GENIE_SPACE_ID, VECTOR_SEARCH_INDEX_ID, UC_FUNCTION_NAME, DATABRICKS_HOST
from databricks_mcp import DatabricksMCPClient

def check_mcp_server(name, url):
    """Check if MCP server is accessible"""
    try:
        client = get_workspace_client()
        mcp = DatabricksMCPClient(server_url=url, workspace_client=client)
        tools = mcp.list_tools()
        print(f'✅ {name}: Accessible')
        print(f'   Found {len(tools)} tools')
        return True
    except Exception as e:
        print(f'❌ {name}: Not accessible')
        print(f'   Error: {str(e)[:100]}')
        return False

print('🔍 Checking MCP Server Availability...')
print('=' * 60)

workspace_host = DATABRICKS_HOST or get_workspace_client().config.host

# Check Genie
genie_url = f'{workspace_host}/api/2.0/mcp/genie/{GENIE_SPACE_ID}'
check_mcp_server('Genie MCP', genie_url)

# Check Vector Search
# URL format: /api/2.0/mcp/vector-search/{catalog}/{schema}
vs_parts = VECTOR_SEARCH_INDEX_ID.split('.')
if len(vs_parts) >= 2:
    vs_url = f'{workspace_host}/api/2.0/mcp/vector-search/{vs_parts[0]}/{vs_parts[1]}'
    check_mcp_server('Vector Search MCP', vs_url)
else:
    print(f'❌ Vector Search MCP: Invalid index_id format: {VECTOR_SEARCH_INDEX_ID}')

# Check UC Functions
# URL format: /api/2.0/mcp/functions/{catalog}/{schema}
uc_parts = UC_FUNCTION_NAME.split('.')
if len(uc_parts) >= 2:
    uc_url = f'{workspace_host}/api/2.0/mcp/functions/{uc_parts[0]}/{uc_parts[1]}'
    check_mcp_server('UC Functions MCP', uc_url)
else:
    print(f'❌ UC Functions MCP: Invalid function_name format: {UC_FUNCTION_NAME}')

print('\n💡 If Vector Search or UC Functions show errors:')
print('   - They may need to be enabled in workspace settings')
print('   - Or resources may need to be created')
print('   - See MCP_SERVER_CONFIG.md for details')
