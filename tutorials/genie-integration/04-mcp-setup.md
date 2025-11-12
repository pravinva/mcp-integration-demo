# Setting Up Genie MCP Server

This guide walks you through configuring and testing the Genie MCP Server connection.

## Understanding Genie MCP Server

The Genie MCP Server is a **managed service** provided by Databricks. You don't need to deploy or maintain it - it's automatically available in your workspace.

### MCP Server Endpoint

**Format:**
```
https://<workspace-hostname>/api/2.0/mcp/genie/{space_id}
```

**Example:**
```
https://your-workspace.cloud.databricks.com/api/2.0/mcp/genie/01f0be3dcc771e60ada71b6ec9f61870
```

### How It Works

1. **MCP Server exposes tools** - Each Genie Space has a tool named `query_space_{space_id}`
2. **Client connects** - Your application connects using Databricks authentication
3. **Tool discovery** - Client can discover available tools
4. **Tool execution** - Client calls the tool with a query
5. **Response** - Genie processes the query and returns results

## Step 1: Get Your Workspace Hostname

Your workspace hostname is the base URL of your Databricks workspace.

**Examples:**
- `https://your-workspace.cloud.databricks.com`
- `https://adb-1234567890123456.7.azuredatabricks.net`
- `https://your-workspace.gcp.databricks.com`

**Find it:**
- Look at your browser URL when logged into Databricks
- Or check your `~/.databrickscfg` file:
  ```ini
  [DEFAULT]
  host = https://your-workspace.cloud.databricks.com
  ```

## Step 2: Get Your Genie Space ID

See [Prerequisites](03-prerequisites.md) for detailed instructions.

**Quick method:**
1. Go to Databricks → SQL → Genie
2. Open your Genie Space
3. Check URL: `space_id=01f0be3dcc771e60ada71b6ec9f61870`
4. Copy the space ID

## Step 3: Configure Authentication

The MCP client uses Databricks Workspace Client for authentication. Choose one method:

### Option A: Personal Access Token (Development)

**In `.env`:**
```bash
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=your-pat-token
GENIE_SPACE_ID=01f0be3dcc771e60ada71b6ec9f61870
```

### Option B: OAuth 2.0 (Production)

**In `.env`:**
```bash
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_CLIENT_ID=your-client-id
DATABRICKS_CLIENT_SECRET=your-client-secret
GENIE_SPACE_ID=01f0be3dcc771e60ada71b6ec9f61870
```

### Option C: Databricks CLI Profile (Easiest)

If you have `~/.databrickscfg` configured, just set:

**In `.env`:**
```bash
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
GENIE_SPACE_ID=01f0be3dcc771e60ada71b6ec9f61870
# Leave DATABRICKS_TOKEN empty - SDK will use ~/.databrickscfg
```

## Step 4: Create the MCP Client

Create `shared/mcp_client.py` (or use the existing one from the codebase):

```python
"""
Universal Databricks MCP Client

This ONE file talks to ALL Databricks MCP servers!
"""

from typing import Optional, Dict, Any
from databricks.sdk import WorkspaceClient
from databricks_mcp import DatabricksMCPClient
import logging
import asyncio

logger = logging.getLogger(__name__)


class UniversalMCPClient:
    """
    Universal MCP Client - works with ALL Databricks MCP servers.
    
    Supports:
    - Genie (analytics)
    - Vector Search (RAG)
    - Unity Catalog Functions (actions)
    """
    
    def __init__(self, workspace_client: WorkspaceClient):
        """Initialize with authenticated workspace client."""
        self.workspace_client = workspace_client
        logger.info("Universal MCP Client initialized")
    
    async def query(
        self, 
        server_url: str, 
        tool_name: str, 
        arguments: Dict[str, Any]
    ) -> str:
        """
        Universal query method - works with ANY MCP server!
        
        Args:
            server_url: MCP server endpoint
            tool_name: Tool to call
            arguments: Tool-specific arguments
            
        Returns:
            Response text from MCP server
        """
        try:
            logger.info(f"Querying {tool_name} on {server_url}")
            
            # Create MCP client for this server
            mcp_client = DatabricksMCPClient(
                server_url=server_url,
                workspace_client=self.workspace_client
            )
            
            # Discover tool name if needed
            if tool_name.startswith("query_space") or tool_name == "ask_question":
                try:
                    tools = mcp_client.list_tools()
                    query_tool = next((t for t in tools if t.name.startswith("query_space")), None)
                    if query_tool:
                        tool_name = query_tool.name
                        logger.info(f"Discovered tool name: {tool_name}")
                except Exception:
                    # Fallback: construct from space_id in URL
                    if "/mcp/genie/" in server_url:
                        space_id = server_url.split("/mcp/genie/")[-1]
                        tool_name = f"query_space_{space_id}"
            
            # Execute query via MCP protocol
            result = await asyncio.to_thread(mcp_client.call_tool, tool_name, arguments)
            
            # Extract response
            if result.content and len(result.content) > 0:
                response_text = result.content[0].text
                logger.info(f"Got response ({len(response_text)} chars)")
                return response_text
            else:
                logger.warning("Empty response from MCP server")
                return "No response received"
                    
        except Exception as e:
            error_msg = str(e)
            logger.error(f"MCP query failed: {error_msg}")
            return f"Error: {error_msg}"
    
    async def ask_genie(
        self, 
        space_id: str, 
        question: str, 
        conversation_id: Optional[str] = None
    ) -> tuple[str, str]:
        """
        Query Genie for analytics.
        
        Args:
            space_id: Genie space ID
            question: Natural language question
            conversation_id: Optional conversation ID for multi-turn context
            
        Returns:
            (response_text, conversation_id)
        """
        from shared.config import DATABRICKS_HOST
        
        server_url = f"{DATABRICKS_HOST}/api/2.0/mcp/genie/{space_id}"
        tool_name = f"query_space_{space_id}"
        
        # Genie MCP uses "query" parameter
        arguments = {"query": question}
        if conversation_id:
            arguments["conversation_id"] = conversation_id
        
        response = await self.query(server_url, tool_name, arguments)
        
        # Generate conversation ID (in production, extract from result metadata)
        new_conv_id = conversation_id or f"conv-{hash(question)}"
        
        return response, new_conv_id


def create_mcp_client() -> UniversalMCPClient:
    """Factory function to create MCP client with proper auth."""
    from shared.config import get_workspace_client
    
    workspace_client = get_workspace_client()
    return UniversalMCPClient(workspace_client)
```

Create `shared/config.py`:

```python
"""
Configuration management for MCP integration.
"""

import os
from dotenv import load_dotenv
from databricks.sdk import WorkspaceClient

load_dotenv()

# Databricks Configuration
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
GENIE_SPACE_ID = os.getenv("GENIE_SPACE_ID")

# Slack Configuration
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

# Teams Configuration
MICROSOFT_APP_ID = os.getenv("MICROSOFT_APP_ID", "")
MICROSOFT_APP_PASSWORD = os.getenv("MICROSOFT_APP_PASSWORD", "")


def get_workspace_client() -> WorkspaceClient:
    """Create authenticated WorkspaceClient."""
    config = {}
    
    if DATABRICKS_HOST:
        config["host"] = DATABRICKS_HOST
    
    # Try token first
    token = os.getenv("DATABRICKS_TOKEN")
    if token:
        config["token"] = token
    
    # Try OAuth
    client_id = os.getenv("DATABRICKS_CLIENT_ID")
    client_secret = os.getenv("DATABRICKS_CLIENT_SECRET")
    if client_id and client_secret:
        config["client_id"] = client_id
        config["client_secret"] = client_secret
    
    # If no explicit auth, SDK will use ~/.databrickscfg
    
    return WorkspaceClient(**config)
```

## Step 5: Test the MCP Connection

Create `test_mcp_connection.py`:

```python
"""
Test Genie MCP Server connection.
"""

import asyncio
import os
from dotenv import load_dotenv
from shared.mcp_client import create_mcp_client

load_dotenv()

async def test_genie_mcp():
    """Test connection to Genie MCP Server."""
    
    space_id = os.getenv("GENIE_SPACE_ID")
    if not space_id:
        print("GENIE_SPACE_ID not set in .env")
        return
    
    print("=" * 60)
    print("Testing Genie MCP Server Connection")
    print("=" * 60)
    print(f"Space ID: {space_id}")
    print()
    
    try:
        # Create MCP client
        print("1. Creating MCP client...")
        mcp_client = create_mcp_client()
        print("   MCP client created")
        print()
        
        # Test query
        print("2. Testing Genie query...")
        print("   Question: 'What tables are available?'")
        
        response, conv_id = await mcp_client.ask_genie(
            space_id=space_id,
            question="What tables are available?"
        )
        
        print("   Query successful!")
        print()
        print("3. Response:")
        print("-" * 60)
        print(response[:500])  # First 500 chars
        if len(response) > 500:
            print("...")
        print("-" * 60)
        print()
        print("MCP connection test PASSED!")
        
    except Exception as e:
        print(f"MCP connection test FAILED: {e}")
        import traceback
        traceback.print_exc()

if __name__ == "__main__":
    asyncio.run(test_genie_mcp())
```

**Run the test:**
```bash
python test_mcp_connection.py
```

**Expected output:**
```
============================================================
Testing Genie MCP Server Connection
============================================================
Space ID: 01f0be3dcc771e60ada71b6ec9f61870

1. Creating MCP client...
   MCP client created

2. Testing Genie query...
   Question: 'What tables are available?'
   Query successful!

3. Response:
------------------------------------------------------------
[Genie response with table information]
------------------------------------------------------------

MCP connection test PASSED!
```

## Troubleshooting

### "404 Not Found" Error

**Problem:** MCP server endpoint not found

**Solutions:**
1. Verify workspace hostname is correct
2. Verify Genie Space ID is correct
3. Check that Genie is enabled in your workspace
4. Ensure you have access to the Genie Space

### "401 Unauthorized" Error

**Problem:** Authentication failed

**Solutions:**
1. Check your `.env` file has correct credentials
2. Verify token hasn't expired
3. Check `~/.databrickscfg` if using CLI profile
4. Try regenerating your Personal Access Token

### "Tool not found" Error

**Problem:** Tool name doesn't match

**Solutions:**
1. The tool name should be `query_space_{space_id}`
2. Let the client auto-discover the tool name
3. Check that the space_id in the URL matches your Genie Space

### Empty Response

**Problem:** Genie returns empty response

**Solutions:**
1. Check that your Genie Space has tables configured
2. Verify the question is valid
3. Check Genie Space permissions
4. Try a simpler question first

## Next Steps

Once MCP connection is working:

- [Slack Integration](05-slack-integration/) - Build Slack bot
- [Teams Integration](06-teams-integration/) - Build Teams bot

