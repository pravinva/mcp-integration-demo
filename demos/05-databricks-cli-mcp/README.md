# Databricks CLI MCP Server (Databricks App)

HTTP-accessible MCP server exposing the full power of Databricks CLI for AI agents.

## Features

### Full CLI Access
Execute ANY Databricks CLI command through HTTP endpoints:
- `databricks catalogs list`
- `databricks jobs run-now --job-id 123`
- `databricks clusters create --json-file config.json`
- `databricks bundles deploy -t prod`
- `databricks apps deploy my-app`
- And 100+ other commands

### Core Endpoints

**GET `/health`** - Health check
**POST `/mcp/explore`** - Discover workspace resources
**POST `/mcp/invoke`** - Execute Databricks CLI command
**POST `/mcp/query`** - Execute SQL query
**GET `/mcp/tools`** - List available tools

## Deployment

### Step 1: Deploy to Databricks Apps

```bash
cd demos/05-databricks-cli-mcp
databricks apps deploy databricks-cli-mcp
```

### Step 2: Get App URL

```bash
databricks apps get databricks-cli-mcp
```

Example URL: `https://databricks-cli-mcp-<id>.<region>.azuredatabricksapps.com`

### Step 3: Test the Endpoint

```bash
# Health check
curl https://<app-url>/health

# Explore workspace
curl -X POST https://<app-url>/mcp/explore \
  -H "Content-Type: application/json" \
  -d '{}'

# List catalogs
curl -X POST https://<app-url>/mcp/invoke \
  -H "Content-Type: application/json" \
  -d '{"command": "catalogs", "args": ["list"]}'

# Query data
curl -X POST "https://<app-url>/mcp/query?warehouse_id=<id>&query=SELECT%20*%20FROM%20catalog.schema.table%20LIMIT%2010"
```

## Integration with Slack Bot

Once deployed, add this to your `shared/mcp_client.py`:

```python
# Add Databricks CLI MCP endpoint
DATABRICKS_CLI_MCP_URL = "https://<app-url>"

async def invoke_databricks_cli(self, command: str, args: list[str]):
    """Execute Databricks CLI command via MCP."""
    response = await self.session.post(
        f"{DATABRICKS_CLI_MCP_URL}/mcp/invoke",
        json={"command": command, "args": args}
    )
    return await response.json()
```

## Example Slack Bot Queries

Once integrated, users can ask:

**Admin Operations:**
- "Show me all running clusters"
- "List jobs that ran today"
- "What SQL warehouses are available?"

**Data Queries:**
- "Query the osipi.telemetry.sensor_data table for last hour"
- "Show me schema of system.information_schema.tables"
- "List all tables in the osipi catalog"

**Resource Management:**
- "Create a new cluster with config X"
- "Start the analytics warehouse"
- "Deploy my bundle to production"

## API Examples

### Explore Workspace
```bash
curl -X POST https://<app-url>/mcp/explore \
  -H "Content-Type: application/json" \
  -d '{}'
```

Response:
```json
{
  "workspace": {
    "host": "https://e2-demo-field-eng.cloud.databricks.com",
    "user": "pravin.varma@databricks.com"
  },
  "resources": {
    "catalogs": [{"name": "main", "comment": "Main catalog"}],
    "warehouses": [{"id": "abc123", "name": "Shared Warehouse", "state": "RUNNING"}],
    "clusters": [{"id": "xyz789", "name": "Field Eng Cluster", "state": "RUNNING"}]
  }
}
```

### Invoke CLI Command
```bash
curl -X POST https://<app-url>/mcp/invoke \
  -H "Content-Type: application/json" \
  -d '{
    "command": "jobs",
    "args": ["list", "--limit", "5"]
  }'
```

### Execute SQL Query
```bash
curl -X POST "https://<app-url>/mcp/query" \
  -H "Content-Type: application/json" \
  -d '{
    "warehouse_id": "abc123",
    "query": "SELECT * FROM system.information_schema.tables LIMIT 10"
  }'
```

## Security Notes

- App runs with the service principal permissions
- CLI commands execute with app identity
- Consider implementing command allowlisting for production
- Add authentication layer for external access

## Local Testing

```bash
# Set credentials
export DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
export DATABRICKS_TOKEN=dapi...

# Install dependencies
pip install -r requirements.txt

# Run locally
python mcp_server.py

# Test endpoints
curl http://localhost:8000/health
curl -X POST http://localhost:8000/mcp/explore \
  -H "Content-Type: application/json" \
  -d '{}'
```

## Architecture

```
┌─────────────────┐
│   Slack Bot     │
│  (Natural Lang) │
└────────┬────────┘
         │
         │ HTTP POST /mcp/invoke
         ▼
┌─────────────────────────┐
│  Databricks CLI MCP     │
│  (FastAPI Server)       │
│  - /mcp/explore         │
│  - /mcp/invoke          │
│  - /mcp/query           │
└────────┬────────────────┘
         │
         │ subprocess.run()
         ▼
┌─────────────────────────┐
│  Databricks CLI         │
│  (databricks catalogs   │
│   jobs clusters ...)    │
└────────┬────────────────┘
         │
         │ REST API
         ▼
┌─────────────────────────┐
│  Databricks Workspace   │
│  (Unity Catalog, Jobs,  │
│   Clusters, etc.)       │
└─────────────────────────┘
```

## Troubleshooting

**App won't start:**
- Check app logs: `databricks apps logs databricks-cli-mcp`
- Verify Python 3.11 runtime in app.yaml
- Ensure all dependencies in requirements.txt

**CLI commands fail:**
- Verify app has proper workspace permissions
- Check Databricks CLI is installed in container
- Review command syntax with `databricks <command> --help`

**Query endpoint errors:**
- Ensure SQL warehouse is running
- Verify warehouse_id is correct
- Check query syntax for SQL errors

## Next Steps

1. **Deploy the app** - Follow deployment steps above
2. **Test endpoints** - Use curl examples to verify
3. **Integrate with Slack** - Add to your bot's MCP client
4. **Monitor usage** - Check app logs and metrics
5. **Enhance security** - Add auth, rate limiting, command filtering
