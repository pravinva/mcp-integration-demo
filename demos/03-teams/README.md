# Teams Bot Setup Guide

## 🎯 Want Real Microsoft Teams? 

**👉 Start here:** [`REAL_TEAMS_COMPLETE.md`](REAL_TEAMS_COMPLETE.md) - Complete step-by-step guide to deploy to real Teams!

**Quick path:** Deploy to Azure → Add to Teams → Start chatting in real Teams! (~30 minutes)

---

## 📚 Deployment Options

### Option 1: Real Microsoft Teams (Recommended) ⭐

**Deploy to Azure for real Teams experience:**

📖 **Complete Guide:** [`REAL_TEAMS_COMPLETE.md`](REAL_TEAMS_COMPLETE.md)  
📖 **Quick Guide:** [`REAL_TEAMS_QUICK.md`](REAL_TEAMS_QUICK.md)  
📦 **Deployment Package:** Run `python prepare_deployment.py`

**What you get:**
- ✅ Real Teams integration
- ✅ Production-ready deployment
- ✅ Free tier available ($0/month)
- ✅ ~30 minutes setup

### Option 2: Local Testing (Agents Playground)

**Test locally before deploying:**

> **Note:** Bot Framework Emulator is deprecated (retiring end of 2025). Use Agents Playground instead!

Reference: https://learn.microsoft.com/en-us/microsoft-365/agents-sdk/test-with-toolkit-project

## Local Testing (Agents Playground)

### Prerequisites

1. **Install Node.js** (if not already installed)
   - Download from: https://nodejs.org/
   - Verify: `node --version`

2. **Install Microsoft 365 Agents Playground**
   ```bash
   npm install -g @microsoft/m365agentsplayground
   ```

3. **Python Environment**
   - Virtual environment activated
   - Dependencies installed

### Quick Start

```bash
cd demos/03-teams
python test_teams_bot.py
```

This will:
- ✅ Check configuration
- ✅ Start bot on port 3978
- ✅ Print connection instructions

### Launch Agents Playground

**Option 1: Use the helper script**
```bash
python launch_playground.py
```

**Option 2: Manual launch**
```bash
agentsplayground -e "http://localhost:3978/api/messages" -c "emulator"
```

The browser will open automatically! Start chatting!

### Test Commands

**Analytics (Genie):**
- "What was Q4 revenue?"
- "Show me top 5 customers"
- "Compare Q3 vs Q4"

**Search Docs (Vector Search):**
- "search how to create Genie space"
- "search MCP tutorial"

**Calculate (UC Functions):**
- "calculate 50000 Enterprise"
- "calculate 25000 SMB"

**Commands:**
- `/help` - Show help
- `/reset` - Reset conversation

## Azure Deployment (Real Teams)

**👉 For complete step-by-step guide, see:** [`REAL_TEAMS_COMPLETE.md`](REAL_TEAMS_COMPLETE.md)

**Quick summary:**

1. **Create Azure Bot** → Get App ID/Password
2. **Create App Service** → Python 3.11 runtime
3. **Deploy code** → Upload `bot-deploy.zip` (run `python prepare_deployment.py`)
4. **Set environment variables** → App ID, Password, Genie Space ID
5. **Configure messaging endpoint** → Point to your App Service
6. **Enable Teams channel** → Add bot to Teams
7. **Start chatting!** → Real Teams experience!

**📚 Detailed guides:**
- [`REAL_TEAMS_COMPLETE.md`](REAL_TEAMS_COMPLETE.md) - Full step-by-step
- [`REAL_TEAMS_QUICK.md`](REAL_TEAMS_QUICK.md) - Quick reference
- [`DEPLOY_TO_TEAMS.md`](DEPLOY_TO_TEAMS.md) - Fast track
- [`AZURE_DEPLOYMENT.md`](AZURE_DEPLOYMENT.md) - Detailed Azure guide

## Features

### 1. Natural Language Analytics (Genie)

Ask questions naturally:
- "What was Q4 revenue?"
- "Show me top customers"
- "Compare quarters"

### 2. Documentation Search (Vector Search)

Start with "search":
- "search how to create Genie space"
- "search MCP integration"

### 3. Calculations (UC Functions)

Start with "calculate":
- "calculate 50000 Enterprise"
- "calculate 25000 SMB"

### 4. Rich Formatting

- Typing indicators
- Adaptive cards (can be added)
- Thread-based conversations

## Code Comparison: Slack vs Teams

Notice how similar the code is! Both use `shared/mcp_client.py`:

**Slack Bot** (`demos/02-slack/slack_bot.py`):
```python
from shared.mcp_client import create_mcp_client
mcp_client = create_mcp_client()

if question.startswith("search "):
    response = await mcp_client.search_docs(...)
elif question.startswith("calculate "):
    response = await mcp_client.call_function(...)
else:
    response, _ = await mcp_client.ask_genie(...)
```

**Teams Bot** (`demos/03-teams/teams_bot.py`):
```python
from shared.mcp_client import create_mcp_client
mcp_client = create_mcp_client()

if user_message.startswith("search "):
    response = await mcp_client.search_docs(...)
elif user_message.startswith("calculate "):
    response = await mcp_client.call_function(...)
else:
    response, _ = await mcp_client.ask_genie(...)
```

**80% code reuse!** That's the M+N pattern! 🎉

## Troubleshooting

### Agents Playground Won't Launch

1. **Runtime Error:** If you see TypeError:
   - Update Node.js to latest LTS: `brew upgrade node` or download from nodejs.org
   - Reinstall: `npm uninstall -g @microsoft/m365agentsplayground && npm install -g @microsoft/m365agentsplayground`
   - Check Node version: `node --version` (should be 18+)

2. **Not Found:** If `agentsplayground` command not found:
   - Verify installation: `npm list -g @microsoft/m365agentsplayground`
   - Reinstall: `npm install -g @microsoft/m365agentsplayground`

### Bot Not Responding

1. Check console for errors
2. Verify Databricks config is valid
3. Check `.env` file has `GENIE_SPACE_ID`

### Connection Failed

1. Verify bot is running: `python test_teams_bot.py`
2. Check port 3978 is not in use: `lsof -i :3978`
3. Verify endpoint URL is correct: `http://localhost:3978/api/messages`

### Azure Deployment Issues

1. Verify Azure Functions Core Tools installed
2. Check function app name is correct
3. Verify App ID and Password in Azure Bot resource

## Next Steps

1. ✅ Test locally with Agents Playground
2. ✅ Deploy to Azure Functions
3. ✅ Configure Azure Bot
4. ✅ Add to Teams workspace
5. ✅ Start using!

## Architecture

```
Teams User
    ↓
Microsoft Teams
    ↓
Azure Bot Service (or Agents Playground for testing)
    ↓
Teams Bot (teams_bot.py)
    ↓
shared/mcp_client.py ← THE SHARED INTEGRATION!
    ↓
Databricks MCP Servers
    ↓
Genie / Vector Search / UC Functions
```

Same architecture as Slack bot - just different UI layer!

