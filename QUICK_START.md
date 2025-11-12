# Quick Start Guide - All Platforms

## 🚀 Quick Test Commands

### 1. CLI (Simplest)
```bash
cd demos/01-cli
python genie_cli.py
# Or full demo:
python genie_cli_full.py
# Type: /demo
```

### 2. Claude Desktop MCP
```bash
# Test MCP server
cd demos/04-claude
python test_mcp_server.py

# Then configure Claude Desktop:
# 1. Copy claude_config.json to Claude config location
# 2. Update path and GENIE_SPACE_ID
# 3. Restart Claude Desktop
```

### 3. Slack Bot
```bash
# Test locally (requires Slack app setup)
cd demos/02-slack
python test_slack_bot.py
# Or:
python slack_bot.py
```

### 4. Teams Bot
```bash
# Test with Bot Framework Emulator
cd demos/03-teams
python test_teams_bot.py

# Then:
# 1. Open Bot Framework Emulator
# 2. Connect to: http://localhost:3978/api/messages
# 3. Leave App ID/Password empty
# 4. Start chatting!
```

## 📋 Prerequisites Checklist

### All Platforms Need:
- ✅ Python virtual environment activated
- ✅ Dependencies installed: `pip install -r requirements.txt`
- ✅ `.env` file with `GENIE_SPACE_ID`
- ✅ `~/.databrickscfg` configured (or OAuth credentials)

### Platform-Specific:

**Claude Desktop:**
- ✅ Claude Desktop installed
- ✅ Python path accessible

**Slack:**
- ✅ Slack app created
- ✅ Socket Mode enabled
- ✅ `SLACK_BOT_TOKEN` and `SLACK_APP_TOKEN` in `.env`

**Teams:**
- ✅ Bot Framework Emulator downloaded (for testing)
- ✅ Azure Bot resource (for production)

## 🎯 What Each Platform Demonstrates

| Platform | What It Shows | Key Feature |
|----------|---------------|-------------|
| **CLI** | Core MCP integration | Simplest demo, all 3 data sources |
| **Claude** | Native MCP protocol | Automatic tool discovery |
| **Slack** | Production deployment | Socket Mode, Databricks Apps |
| **Teams** | Enterprise integration | Bot Framework, Azure |

## 🔗 Common Patterns

All platforms use the **same** code:

```python
from shared.mcp_client import create_mcp_client

mcp_client = create_mcp_client()

# Genie
response, _ = await mcp_client.ask_genie(space_id, "What was revenue?")

# Vector Search
docs = await mcp_client.search_docs(index_id, "How to use MCP?")

# UC Functions
result = await mcp_client.call_function(func_name, {"param": "value"})
```

**That's the M+N pattern!** 🎉

## 📚 Detailed Guides

- **CLI**: See main `README.md`
- **Claude**: `demos/04-claude/README.md`
- **Slack**: `demos/02-slack/README.md`
- **Teams**: `demos/03-teams/README.md`

## 🐛 Troubleshooting

### "Module not found"
```bash
source venv/bin/activate
pip install -r requirements.txt
```

### "GENIE_SPACE_ID not set"
```bash
echo "GENIE_SPACE_ID=your-space-id" >> .env
```

### "Cannot connect to Databricks"
```bash
# Check ~/.databrickscfg exists
cat ~/.databrickscfg

# Or use mock mode:
echo "USE_MOCK_MCP=true" >> .env
```

## ✅ Success Indicators

**CLI:** Can ask questions and get responses  
**Claude:** Tools appear in Claude Desktop  
**Slack:** Bot responds to DMs and @mentions  
**Teams:** Bot responds in Emulator  

All using the **same** `shared/mcp_client.py`! 🚀

