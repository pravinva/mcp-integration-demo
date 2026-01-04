# Integrating Databricks CLI MCP with Slack Bot

This guide shows you how to integrate the deployed Databricks CLI MCP server with your Slack bot from `demos/02-slack`.

## Deployed App Details

**App Name:** `databricks-cli-mcp`
**App URL:** `https://databricks-cli-mcp-1444828305810485.aws.databricksapps.com`
**Status:** RUNNING ✓
**Deployment ID:** 01f0e967309511ad8535c43b43c6dc3d

## Integration Steps

### 1. Add MCP Endpoint to Shared Config

Edit `shared/config.py` to add the MCP endpoint:

```python
# Add to shared/config.py

# Databricks CLI MCP Server
DATABRICKS_CLI_MCP_URL = os.getenv(
    "DATABRICKS_CLI_MCP_URL",
    "https://databricks-cli-mcp-1444828305810485.aws.databricksapps.com"
)
```

### 2. Extend MCP Client with CLI Methods

Edit `shared/mcp_client.py` to add CLI-specific methods:

```python
# Add to shared/mcp_client.py

async def explore_workspace(self):
    """Explore Databricks workspace resources."""
    response = await self.session.post(
        f"{DATABRICKS_CLI_MCP_URL}/mcp/explore",
        json={}
    )
    return await response.json()

async def invoke_databricks_cli(self, command: str, args: list[str]):
    """Execute Databricks CLI command via MCP."""
    response = await self.session.post(
        f"{DATABRICKS_CLI_MCP_URL}/mcp/invoke",
        json={"command": command, "args": args}
    )
    return await response.json()

async def query_sql(self, warehouse_id: str, query: str):
    """Execute SQL query via MCP."""
    response = await self.session.post(
        f"{DATABRICKS_CLI_MCP_URL}/mcp/query",
        json={"warehouse_id": warehouse_id, "query": query}
    )
    return await response.json()
```

### 3. Add CLI Command Handlers to Slack Bot

Edit `demos/02-slack/slack_bot.py` to handle CLI commands:

```python
# Add to slack_bot.py

@app.message("list clusters")
async def handle_list_clusters(message, say):
    """Handle 'list clusters' command."""
    try:
        result = await mcp_client.invoke_databricks_cli("clusters", ["list", "--output", "json"])

        if result.get("status") == "success":
            clusters = result.get("data", [])
            if clusters:
                response = "*Running Clusters:*\n"
                for cluster in clusters[:5]:  # Show first 5
                    name = cluster.get("cluster_name", "Unnamed")
                    state = cluster.get("state", "UNKNOWN")
                    response += f"• {name} - {state}\n"
                await say(response)
            else:
                await say("No clusters found.")
        else:
            await say(f"Error: {result.get('error', 'Unknown error')}")

    except Exception as e:
        await say(f"Failed to list clusters: {str(e)}")


@app.message("list jobs")
async def handle_list_jobs(message, say):
    """Handle 'list jobs' command."""
    try:
        result = await mcp_client.invoke_databricks_cli("jobs", ["list", "--limit", "5", "--output", "json"])

        if result.get("status") == "success":
            jobs = result.get("data", [])
            if jobs:
                response = "*Recent Jobs:*\n"
                for job in jobs:
                    job_id = job.get("job_id")
                    name = job.get("name", "Unnamed")
                    response += f"• [{job_id}] {name}\n"
                await say(response)
            else:
                await say("No jobs found.")
        else:
            await say(f"Error: {result.get('error', 'Unknown error')}")

    except Exception as e:
        await say(f"Failed to list jobs: {str(e)}")


@app.message("explore workspace")
async def handle_explore(message, say):
    """Handle 'explore workspace' command."""
    try:
        result = await mcp_client.explore_workspace()

        workspace_info = result.get("workspace", {})
        resources = result.get("resources", {})

        response = f"*Workspace:* {workspace_info.get('host')}\n"
        response += f"*User:* {workspace_info.get('user')}\n\n"

        response += f"*Catalogs:* {len(resources.get('catalogs', []))}\n"
        response += f"*Warehouses:* {len(resources.get('warehouses', []))}\n"
        response += f"*Clusters:* {len(resources.get('clusters', []))}\n"

        await say(response)

    except Exception as e:
        await say(f"Failed to explore workspace: {str(e)}")
```

### 4. Add Natural Language Processing

For more advanced integration, add NLP to detect CLI-related queries:

```python
# Add to slack_bot.py

@app.event("app_mention")
async def handle_mention(event, say):
    """Handle @ mentions with CLI awareness."""
    text = event.get("text", "").lower()

    # CLI command detection
    if "cluster" in text and "list" in text:
        await handle_list_clusters(event, say)
    elif "job" in text and ("list" in text or "show" in text):
        await handle_list_jobs(event, say)
    elif "explore" in text or "workspace" in text:
        await handle_explore(event, say)
    elif "query" in text or "sql" in text:
        # Extract SQL from message and execute
        # TODO: Add SQL extraction logic
        await say("SQL query support coming soon!")
    else:
        # Fall back to Genie for general questions
        await handle_genie_query(event, say)
```

## Testing the Integration

### Test 1: List Clusters
In Slack: `@bot list clusters`

Expected response:
```
*Running Clusters:*
• Field Eng Shared UC LTS Cluster - RUNNING
• Analytics Cluster - TERMINATED
```

### Test 2: List Jobs
In Slack: `@bot list jobs`

Expected response:
```
*Recent Jobs:*
• [566534517317334] exporium test
• [702649985056714] Playground kick job
```

### Test 3: Explore Workspace
In Slack: `@bot explore workspace`

Expected response:
```
*Workspace:* https://e2-demo-field-eng.cloud.databricks.com
*User:* pravin.varma@databricks.com

*Catalogs:* 150
*Warehouses:* 50
*Clusters:* 35
```

## Example Use Cases

### Admin Queries
- "Show me all running clusters"
- "List recent jobs"
- "What SQL warehouses are available?"
- "Explore the workspace"

### Data Queries
- "Query system.information_schema.tables for table list"
- "Show me all tables in the osipi catalog"
- "Execute SELECT COUNT(*) FROM main.sales.orders"

### Resource Management (Future)
- "Start the analytics warehouse"
- "Terminate cluster xyz-123"
- "Run job 12345"

## Authentication Notes

The MCP server requires OAuth authentication for public access. However, when called from:
- **Databricks Apps** (like the Slack bot) - Uses app-to-app authentication automatically
- **Local testing** - Requires DATABRICKS_TOKEN environment variable
- **External services** - Requires OAuth flow or service principal

## Deployment Checklist

- [x] MCP server deployed and running
- [x] App URL configured: `https://databricks-cli-mcp-1444828305810485.aws.databricksapps.com`
- [ ] Update `shared/config.py` with MCP URL
- [ ] Add CLI methods to `shared/mcp_client.py`
- [ ] Add command handlers to `demos/02-slack/slack_bot.py`
- [ ] Test with Slack workspace
- [ ] Deploy updated Slack bot

## Next Steps

1. **Update Config** - Add DATABRICKS_CLI_MCP_URL to config
2. **Extend MCP Client** - Add CLI methods to shared client
3. **Add Handlers** - Implement command handlers in Slack bot
4. **Test Locally** - Test with mock data first
5. **Deploy** - Re-deploy Slack bot with new functionality
6. **Monitor** - Watch app logs for errors

## Troubleshooting

**Error: "Connection refused"**
- Check app is running: `databricks apps get databricks-cli-mcp`
- Verify URL is correct
- Check network connectivity

**Error: "Authentication failed"**
- Ensure Slack bot has proper service principal permissions
- Check app-to-app communication is enabled

**Error: "Command timeout"**
- CLI commands have 60s timeout
- Long-running queries may need async handling
- Consider breaking large operations into smaller chunks

## Architecture Diagram

```
┌──────────────┐
│ Slack User   │
│ "list jobs"  │
└──────┬───────┘
       │
       │ WebSocket
       ▼
┌──────────────────────┐
│ Slack Bot            │
│ (demos/02-slack)     │
│ - Parse message      │
│ - Route to handler   │
└──────┬───────────────┘
       │
       │ HTTP POST /mcp/invoke
       ▼
┌──────────────────────┐
│ Databricks CLI MCP   │
│ (demos/05-...)       │
│ - Validate request   │
│ - Execute CLI cmd    │
└──────┬───────────────┘
       │
       │ subprocess.run()
       ▼
┌──────────────────────┐
│ Databricks CLI       │
│ - databricks jobs    │
│   list --output json │
└──────┬───────────────┘
       │
       │ REST API
       ▼
┌──────────────────────┐
│ Databricks Workspace │
│ - Jobs API           │
│ - Returns JSON       │
└──────────────────────┘
```

## Summary

You now have:
1. ✅ Deployed MCP server exposing Databricks CLI
2. ✅ HTTP endpoints for admin operations
3. ✅ Ready-to-integrate API for Slack bot
4. ✅ Example handlers and test cases
5. ✅ Complete integration guide

Update your Slack bot code following the steps above, and you'll have full Databricks CLI access through natural language in Slack!
