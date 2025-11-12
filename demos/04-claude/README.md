# Claude Desktop MCP Setup Guide

This guide shows how to connect Databricks MCP servers to Claude Desktop.

## Prerequisites

1. **Claude Desktop installed**
   - Download from: https://claude.ai/download
   - Mac, Windows, or Linux

2. **Python environment**
   - Python 3.8+ with virtual environment activated
   - All dependencies installed (`pip install -r requirements.txt`)

3. **Databricks credentials**
   - Option A: `~/.databrickscfg` configured (easiest)
   - Option B: OAuth credentials

## Quick Setup

### Step 1: Find Claude Desktop Config Location

**Mac:**
```bash
~/Library/Application Support/Claude/claude_desktop_config.json
```

**Windows:**
```
%APPDATA%\Claude\claude_desktop_config.json
```

**Linux:**
```bash
~/.config/Claude/claude_desktop_config.json
```

### Step 2: Get Absolute Path to MCP Server

```bash
# From project root
cd demos/04-claude
pwd  # Copy this full path
```

Or use Python:
```python
from pathlib import Path
print(Path(__file__).parent.absolute())
```

### Step 3: Update Config File

1. Copy `claude_config.json` to Claude Desktop config location
2. Update the `args` path to your absolute path:
   ```json
   "args": [
     "/Users/yourname/Documents/Demo/mcp-integration-blog/demos/04-claude/mcp_server.py"
   ]
   ```
3. Update `GENIE_SPACE_ID` with your actual space ID
4. (Optional) If using OAuth, uncomment and fill `_oauth_env` section

### Step 4: Restart Claude Desktop

Close and reopen Claude Desktop. The MCP server will be available!

## Testing Without Claude Desktop

Test the MCP server directly:

```bash
cd demos/04-claude
python test_mcp_server.py
```

This will:
- ✅ Validate configuration
- ✅ List available tools
- ✅ Test all three tools (Genie, Vector Search, UC Functions)

## Using in Claude Desktop

Once configured, Claude Desktop will automatically discover the tools. You can:

1. **Ask Genie questions:**
   ```
   "What was our Q4 revenue?"
   "Show me top 5 customers"
   ```

2. **Search documentation:**
   ```
   "Search for how to create a Genie space"
   ```

3. **Calculate discounts:**
   ```
   "Calculate discount for $50,000 Enterprise order"
   ```

Claude will automatically choose the right tool based on your question!

## Troubleshooting

### Error: "Cannot find Python"

**Solution:** Use full path to Python:
```json
"command": "/path/to/venv/bin/python",
```

Or use the venv Python:
```json
"command": "/path/to/mcp-integration-blog/venv/bin/python",
```

### Error: "Module not found"

**Solution:** Make sure virtual environment is activated or use venv Python path.

### Error: "GENIE_SPACE_ID not set"

**Solution:** Update `GENIE_SPACE_ID` in the config file's `env` section.

### MCP Server Not Appearing

1. Check Claude Desktop logs:
   - Mac: `~/Library/Logs/Claude/`
   - Windows: `%APPDATA%\Claude\logs\`

2. Verify path is absolute (not relative)

3. Test server manually: `python demos/04-claude/test_mcp_server.py`

## Configuration Options

### Option 1: Using ~/.databrickscfg (Recommended)

```json
"env": {
  "DATABRICKS_PROFILE": "DEFAULT",
  "GENIE_SPACE_ID": "your-space-id"
}
```

### Option 2: Using OAuth

```json
"env": {
  "DATABRICKS_HOST": "https://your-workspace.cloud.databricks.com",
  "DATABRICKS_OAUTH_CLIENT_ID": "your-client-id",
  "DATABRICKS_OAUTH_CLIENT_SECRET": "your-client-secret",
  "GENIE_SPACE_ID": "your-space-id"
}
```

### Option 3: Mock Mode (Testing)

```json
"env": {
  "USE_MOCK_MCP": "true",
  "GENIE_SPACE_ID": "mock-space-id"
}
```

## Next Steps

Once Claude Desktop is connected:

1. ✅ Try asking Genie questions
2. ✅ Test Vector Search
3. ✅ Test UC Functions
4. ✅ See how Claude automatically chooses the right tool!

## Example Claude Conversation

**You:** "What was our Q4 revenue?"

**Claude:** *[Uses ask_genie tool automatically]*
"Based on the data, your Q4 2024 revenue was $155,300..."

**You:** "Search for documentation on creating Genie spaces"

**Claude:** *[Uses search_docs tool automatically]*
"I found documentation on creating Genie spaces..."

That's the power of MCP - Claude automatically discovers and uses the right tools!

