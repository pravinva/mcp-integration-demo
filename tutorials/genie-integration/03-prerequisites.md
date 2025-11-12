# Prerequisites

Before starting the integration, ensure you have the following set up.

## Required Accounts and Access

### 1. Databricks Workspace

- Access to a Databricks workspace
- Genie feature enabled (verify with workspace administrator)
- Genie Space created (instructions provided below)
- Permissions to create Personal Access Tokens or OAuth applications

### 2. Slack Workspace (for Slack integration)

- Administrator access to a Slack workspace
- Capability to create applications at https://api.slack.com/apps

### 3. Microsoft Account (for Teams integration)

- Microsoft account (personal or organizational)
- Development: Free Agents Playground access (no Azure subscription required)
- Production: Azure subscription (free tier available)

## Development Environment

### Python Environment

**Python Version:** 3.9 or higher (3.11 recommended)

**Check your version:**
```bash
python3 --version
```

**Create virtual environment:**
```bash
python3 -m venv venv
source venv/bin/activate  # On Windows: venv\Scripts\activate
```

### Required Python Packages

Create `requirements.txt`:

```txt
databricks-sdk>=0.20.0
databricks-mcp>=0.1.0
slack-bolt>=1.18.0
aiohttp>=3.9.0
botbuilder-core>=4.20.0
python-dotenv>=1.0.0
```

**Install dependencies:**
```bash
pip install -r requirements.txt
```

### Node.js (for Teams Agents Playground)

**Required for:** Microsoft 365 Agents Playground (local Teams testing)

**Install Node.js:**
- Download from: https://nodejs.org/
- Version: 18.x or higher (LTS recommended)

**Verify installation:**
```bash
node --version
npm --version
```

**Install Agents Playground:**
```bash
npm install -g @microsoft/m365agentsplayground
```

## Databricks Configuration

### Option 1: Personal Access Token (Development)

1. **Go to:** Databricks workspace → User Settings → Access Tokens
2. **Generate new token:**
   - Description: "Genie MCP Integration"
   - Lifetime: 90 days (or as needed)
3. **Save the token** securely (you won't see it again!)

### Option 2: OAuth 2.0 (Production)

1. **Create OAuth app** in Databricks workspace
2. **Configure redirect URIs**
3. **Get Client ID and Client Secret**

### Option 3: Databricks CLI Profile (Easiest for Development)

If you have `databricks-cli` configured:

```bash
databricks configure --token
```

This creates `~/.databrickscfg` which the SDK can use automatically.

## Find Your Genie Space ID

### Method 1: From Databricks UI

1. **Go to:** Databricks workspace → SQL → Genie
2. **Open your Genie Space**
3. **Check the URL:** It contains `space_id=...`
   - Example: `https://workspace.cloud.databricks.com/sql/genie?space_id=01f0be3dcc771e60ada71b6ec9f61870`
4. **Copy the space ID**

### Method 2: Using Python Script

Create `find_genie_space.py`:

```python
from databricks.sdk import WorkspaceClient

workspace_client = WorkspaceClient()

# List all Genie spaces
spaces = workspace_client.genie.spaces.list()

print("Available Genie Spaces:")
for space in spaces:
    print(f"  - {space.name}: {space.space_id}")
```

Run:
```bash
python find_genie_space.py
```

### Method 3: Create a New Space

If you don't have a Genie Space:

1. **Go to:** Databricks workspace → SQL → Genie
2. **Click:** "Create Space"
3. **Configure:**
   - Name: "Analytics Space" (or your choice)
   - Select schemas/tables to include
   - Add instructions/context
4. **Save** and note the Space ID

## Environment Variables

Create a `.env` file in your project root:

```bash
# Databricks Configuration
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
GENIE_SPACE_ID=01f0be3dcc771e60ada71b6ec9f61870

# Authentication (choose one method)
# Option 1: Personal Access Token
DATABRICKS_TOKEN=your-pat-token

# Option 2: OAuth (for production)
# DATABRICKS_CLIENT_ID=your-client-id
# DATABRICKS_CLIENT_SECRET=your-client-secret

# Option 3: Use ~/.databrickscfg (leave these empty)
# DATABRICKS_TOKEN=
# DATABRICKS_CLIENT_ID=
# DATABRICKS_CLIENT_SECRET=

# Slack Configuration (for Slack integration)
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token

# Teams Configuration (for Teams integration)
MICROSOFT_APP_ID=your-app-id  # Empty for local testing
MICROSOFT_APP_PASSWORD=your-app-password  # Empty for local testing
```

**Important:** Add `.env` to `.gitignore` to keep credentials secure!

## Verify Setup

### Test Databricks Connection

Create `test_connection.py`:

```python
from databricks.sdk import WorkspaceClient
import os
from dotenv import load_dotenv

load_dotenv()

workspace_client = WorkspaceClient()

# Test connection
try:
    current_user = workspace_client.current_user.me()
    print(f"Connected as: {current_user.user_name}")
    print(f"Workspace: {workspace_client.config.host}")
except Exception as e:
    print(f"Connection failed: {e}")
```

Run:
```bash
python test_connection.py
```

### Test Genie Space Access

Create `test_genie_space.py`:

```python
from databricks.sdk import WorkspaceClient
from shared.mcp_client import create_mcp_client
import asyncio
import os
from dotenv import load_dotenv

load_dotenv()

async def test_genie():
    mcp_client = create_mcp_client()
    space_id = os.getenv("GENIE_SPACE_ID")
    
    if not space_id:
        print("GENIE_SPACE_ID not set in .env")
        return
    
    print(f"Testing Genie Space: {space_id}")
    
    try:
        response, _ = await mcp_client.ask_genie(
            space_id=space_id,
            question="What tables are available?"
        )
        print(f"Genie response received: {response[:200]}...")
    except Exception as e:
        print(f"Genie test failed: {e}")

asyncio.run(test_genie())
```

Run:
```bash
python test_genie_space.py
```

## Platform-Specific Prerequisites

### For Slack Integration

See: [05-slack-integration/README.md](05-slack-integration/README.md)

**Quick checklist:**
- Slack workspace admin access
- Ability to create Slack applications
- SLACK_BOT_TOKEN and SLACK_APP_TOKEN (obtained during setup)

### For Teams Integration

See: [06-teams-integration/README.md](06-teams-integration/README.md)

**Quick checklist:**
- Microsoft account
- Node.js installed (for Agents Playground)
- Agents Playground installed (for local testing)
- Azure subscription (required only for production deployment)

## Troubleshooting Prerequisites

### "Module not found" errors

```bash
# Make sure virtual environment is activated
source venv/bin/activate  # or venv\Scripts\activate on Windows

# Reinstall dependencies
pip install -r requirements.txt
```

### "Authentication failed" errors

- Check your `.env` file has correct credentials
- Verify token hasn't expired
- Check `~/.databrickscfg` if using CLI profile

### "Genie Space not found" errors

- Verify `GENIE_SPACE_ID` is correct
- Check you have access to the Genie Space
- Try listing spaces with the script above

## Next Steps

Once prerequisites are met:

- [MCP Setup](04-mcp-setup.md) - Configure Genie MCP Server
- [Slack Integration](05-slack-integration/) - Build Slack bot
- [Teams Integration](06-teams-integration/) - Build Teams bot

