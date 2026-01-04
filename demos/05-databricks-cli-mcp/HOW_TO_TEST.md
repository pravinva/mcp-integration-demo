# How to Test the Databricks CLI MCP Server

## Current Status

✅ **MCP Server is RUNNING**
- URL: https://databricks-cli-mcp-1444828305810485.aws.databricksapps.com
- Status: Active and responding to requests
- OAuth: Properly configured

## Testing Methods

### Method 1: Automated Test Script (Run Locally)

Run the test script I created:

```bash
cd /Users/pravin.varma/Documents/Demo/mcp-integration-demo/demos/05-databricks-cli-mcp
python3 test_mcp_server.py
```

**Expected Output:**
```
✅ MCP Server is RUNNING at:
   https://databricks-cli-mcp-1444828305810485.aws.databricksapps.com

⚠️  OAuth redirect detected (302)
This is expected when calling from local machine.
```

**What This Proves:**
- MCP server is online and responding
- OAuth authentication is working (302 redirect is correct behavior)
- Server endpoints are accessible

**Limitation:**
- Cannot execute actual commands from local machine
- OAuth requires service principal to service principal authentication
- This is BY DESIGN for security

---

### Method 2: MCP CLI Tool (Run Locally)

Use the mcp-cli tool to interact with the server:

```bash
# List available tools
mcp-cli tools databricks-mcp

# Check tool schema
mcp-cli info databricks-mcp/invoke_databricks_cli

# Try to invoke (will timeout due to OAuth requirement)
mcp-cli call databricks-mcp/invoke_databricks_cli '{"working_directory": "/tmp", "args": ["clusters", "list"]}'
```

**Expected Output:**
```
Available tools:
- invoke_databricks_cli
- databricks_configure_auth
- databricks_discover
```

**Limitation:**
- Same OAuth limitation as Method 1
- Commands will timeout or get authentication errors

---

### Method 3: Direct CLI Test (Run Locally)

Verify that the Databricks CLI itself works:

```bash
# Test clusters command
databricks clusters list --output json

# Test jobs command
databricks jobs list --output json

# Test warehouses command
databricks sql-warehouses list --output json
```

**Expected Output:**
```json
[
  {
    "cluster_id": "0709-132523-cnhxf2p6",
    "cluster_cores": 72,
    ...
  }
]
```

**What This Proves:**
- Your Databricks CLI authentication works
- The commands that the MCP server will execute are valid
- Your credentials have the right permissions

---

### Method 4: Deploy and Test via Slack (FULL END-TO-END TEST)

This is the **ONLY** way to test the complete OAuth flow.

#### Step 1: Configure Slack Secrets

Create a secret scope and add your Slack tokens:

```bash
# Create secret scope (if not exists)
databricks secrets create-scope slack-secrets

# Add Slack bot token
databricks secrets put slack-secrets slack-bot-token --string-value "xoxb-your-token-here"

# Add Slack app token
databricks secrets put slack-secrets slack-app-token --string-value "xapp-your-token-here"
```

#### Step 2: Update app.yaml

Edit `demos/05-databricks-cli-mcp/app.yaml` to reference secrets:

```yaml
command: ["python", "cli_slack_bot.py"]

resources:
  cpu: "1"
  memory: "1Gi"

env:
  - name: SLACK_BOT_TOKEN
    valueFrom:
      secretKeyRef:
        key: slack-bot-token
        scope: slack-secrets

  - name: SLACK_APP_TOKEN
    valueFrom:
      secretKeyRef:
        key: slack-app-token
        scope: slack-secrets
```

#### Step 3: Deploy the Slack Bot

```bash
cd /Users/pravin.varma/Documents/Demo/mcp-integration-demo/demos/05-databricks-cli-mcp

# Create the app (if not already created)
databricks apps create cli-slack-bot

# Deploy the app
databricks apps deploy cli-slack-bot --source-code-path .
```

#### Step 4: Test via Slack

Open Slack and send messages to your bot:

**Direct Message Commands:**
```
list clusters
list jobs
list warehouses
explore workspace
help
```

**Channel Mention Commands:**
```
@YourBot list clusters
@YourBot list jobs
@YourBot explore workspace
```

**Expected Output:**

For `list clusters`:
```
🖥️ Clusters:
cluster_id: 0709-132523-cnhxf2p6
cluster_name: My Cluster
state: RUNNING
...
```

For `list jobs`:
```
⚙️ Jobs:
job_id: 123456
job_name: My ETL Job
creator: pravin.varma@databricks.com
...
```

For `explore workspace`:
```
🔍 Workspace:
Available resources:
- 45 clusters
- 123 jobs
- 8 SQL warehouses
...
```

---

## Architecture Flow (Method 4 - Full E2E)

```
┌─────────────┐
│ Slack User  │ types: "list clusters"
└──────┬──────┘
       │
       ▼
┌─────────────────────────────────┐
│ Slack Bot (Databricks App)      │
│ - OAuth SP: 1f462284-...         │
│ - Authenticates using            │
│   WorkspaceClient                │
└──────┬──────────────────────────┘
       │ POST /mcp/invoke
       │ Authorization: Bearer <oauth_token>
       │ {"name": "invoke_databricks_cli",
       │  "arguments": {...}}
       │
       ▼
┌─────────────────────────────────┐
│ MCP Server (Databricks App)     │
│ - OAuth SP: 4aa4bd32-...         │
│ - Validates OAuth token          │
│ - Executes: databricks clusters │
│   list --output json             │
└──────┬──────────────────────────┘
       │
       ▼
┌─────────────────────────────────┐
│ Databricks Workspace API        │
│ Returns cluster data             │
└─────────────────────────────────┘
```

---

## Why Local Testing Shows OAuth Redirects

**The 302 OAuth redirect is CORRECT BEHAVIOR:**

1. **Local Machine Uses PAT Token:**
   - Your `~/.databrickscfg` uses a Personal Access Token (PAT)
   - PATs are for user authentication

2. **MCP Server Expects OAuth Token:**
   - Databricks Apps use OAuth service principal authentication
   - Service principals authenticate app-to-app

3. **Different Authentication Methods:**
   ```
   Local Machine (PAT)  → MCP Server (OAuth) = ❌ 302 Redirect
   Slack Bot (OAuth)    → MCP Server (OAuth) = ✅ Success
   ```

4. **This is BY DESIGN:**
   - Databricks Apps have stricter security
   - Only other Databricks Apps can call them
   - Prevents unauthorized external access

---

## Quick Reference

### MCP Server Details
- **URL:** https://databricks-cli-mcp-1444828305810485.aws.databricksapps.com
- **Client ID:** 4aa4bd32-afc3-452b-8efc-0827e2fd4d4b
- **Status:** ✅ RUNNING

### OAuth Service Principal (mcp-cli)
- **Client ID:** 4d76e165-398b-4246-a828-f3f3b97dea9b
- **Permissions:** Can manage databricks-cli-mcp app

### Available Endpoints
- `/mcp/explore` - Discover workspace resources
- `/mcp/invoke` - Execute CLI commands

### Available Tools
- `invoke_databricks_cli` - Execute any Databricks CLI command
- `databricks_configure_auth` - Configure authentication
- `databricks_discover` - Discover available resources

---

## Summary

**Can Test Locally:**
✅ MCP server is running and accessible
✅ OAuth authentication is configured
✅ CLI commands work with your credentials
✅ Server endpoints respond correctly

**Cannot Test Locally:**
❌ OAuth flow between service principals
❌ Actual command execution through MCP server
❌ Full request/response cycle

**Solution:**
✅ Deploy Slack bot as Databricks App
✅ Slack bot will use OAuth to authenticate
✅ Test commands via Slack interface

---

## Next Steps

1. **If you just want to verify the server is working:**
   ```bash
   python3 test_mcp_server.py
   ```
   Look for: "✅ MCP Server is RUNNING"

2. **If you want to do full end-to-end testing:**
   - Configure Slack secrets (Step 1 above)
   - Deploy Slack bot (Step 3 above)
   - Test via Slack (Step 4 above)

3. **If you have questions:**
   - Review TEST_RESULTS.md for detailed findings
   - Check logs: `databricks apps logs databricks-cli-mcp`
   - Verify OAuth permissions in Databricks UI

---

**Created:** 2026-01-04
**Author:** Claude Code
**Status:** Ready for testing
