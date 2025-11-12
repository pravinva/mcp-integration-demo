# Demo Script: Databricks MCP Integration Showcase

This script guides you through demonstrating the M×N → M+N transformation using Model Context Protocol.

## Pre-Demo Setup

### 1. Environment Check

```bash
# Verify virtual environment is activated
which python  # Should show venv path

# Verify dependencies installed
pip list | grep databricks-mcp

# Check configuration
cat .env | grep GENIE_SPACE_ID
```

### 2. Mock Mode (Recommended for Demos)

For reliable demos without Databricks connection:

```bash
echo "USE_MOCK_MCP=true" >> .env
echo "GENIE_SPACE_ID=mock-space-id" >> .env
```

---

## Demo Flow: 5-Minute Overview

### Part 1: The Problem (1 minute)

**Show:** `comparison/without-mcp/README.md`

**Key Points:**
- Traditional approach: **4 platforms × 3 data sources = 12 integrations**
- Each integration is custom code
- Bug fixes = 12 implementations
- New features = 12 implementations
- **~2,100 lines of code**

**Visual:**
```
Platforms:     CLI    Claude   Slack   Teams
Data Sources:  Genie  Vector   UC Func
                ↓       ↓        ↓
            [12 separate integrations]
```

---

### Part 2: The Solution (2 minutes)

**Show:** `shared/mcp_client.py`

**Key Points:**
- **ONE universal client** (`shared/mcp_client.py`)
- **ONE `query()` method** works for ALL data sources
- Same protocol, different URLs
- **80% code reuse**

**Code Highlight:**
```python
# This ONE method works for Genie, Vector Search, AND UC Functions!
async def query(self, server_url, tool_name, arguments):
    mcp_client = DatabricksMCPClient(server_url, workspace_client)
    result = await mcp_client.call_tool(tool_name, arguments)
    return result.content.text
```

**Visual:**
```
Platforms:     CLI    Claude   Slack   Teams
                ↓       ↓        ↓       ↓
            [ONE shared/mcp_client.py]
                ↓       ↓        ↓
Data Sources:  Genie  Vector   UC Func
```

**Result:** 4 platforms + 3 servers = **7 components** (not 12!)

---

### Part 3: Live Demo (2 minutes)

#### Demo 1: CLI - One Client, Three Data Sources

```bash
cd demos/01-cli
python genie_cli_full.py
```

**Commands to run:**
1. `/demo` - Shows all 3 data sources working

**What to highlight:**
- Same `create_mcp_client()` imported
- Same `ask_genie()`, `search_docs()`, `call_function()` methods
- All use the same underlying `query()` method

#### Demo 2: Code Reuse Across Platforms

**Show:** Compare Slack and Teams bots

```bash
# Show Slack bot
head -50 demos/02-slack/slack_bot.py | grep -A 5 "from shared"

# Show Teams bot  
head -50 demos/03-teams/teams_bot.py | grep -A 5 "from shared"
```

**Key Point:** Both import `from shared.mcp_client import create_mcp_client`

**Show:** Similar routing logic (80% same code)

```python
# Slack bot (lines 57-91)
if question.lower().startswith("search "):
    response = await mcp_client.search_docs(...)
elif question.lower().startswith("calculate "):
    response = await mcp_client.call_function(...)
else:
    response, _ = await mcp_client.ask_genie(...)

# Teams bot (lines 98-132) - SAME PATTERN!
if user_message.lower().startswith("search "):
    response = await mcp_client.search_docs(...)
elif user_message.lower().startswith("calculate "):
    response = await mcp_client.call_function(...)
else:
    response, _ = await mcp_client.ask_genie(...)
```

---

## Extended Demo: Full Platform Tour (10 minutes)

### Step 1: CLI Demo (2 min)

```bash
cd demos/01-cli
python genie_cli.py
```

**Try:**
- "What was Q4 revenue?"
- "Show me top 5 customers"
- "reset" (new conversation)

**Highlight:**
- Natural language queries
- Conversation context maintained
- Uses `shared/mcp_client.py`

### Step 2: Full Multi-Source Demo (2 min)

```bash
python genie_cli_full.py
```

**Try:**
- `/demo` - Full sequence
- `/genie What was revenue?`
- `/search How to use MCP?`
- `/function 50000 Enterprise`

**Highlight:**
- ONE client, THREE data sources
- Same `query()` method underneath

### Step 3: Claude Desktop Integration (2 min)

**Show:** `demos/04-claude/mcp_server.py`

**Key Points:**
- Uses `mcp.server` library
- Exposes 3 tools to Claude
- Internally uses `shared/mcp_client.py`

**Configuration:**
```json
{
  "mcpServers": {
    "databricks-genie": {
      "command": "python",
      "args": ["/path/to/demos/04-claude/mcp_server.py"]
    }
  }
}
```

**Highlight:** Claude automatically discovers tools and uses them!

### Step 4: Slack Bot (2 min)

**Show:** `demos/02-slack/slack_bot.py`

**Key Points:**
- Production-ready (Databricks Apps)
- Socket Mode for local testing
- Rich formatting with Slack blocks
- Thread-based conversation context

**Demo Commands:**
- `@Genie Bot what was Q4 revenue?`
- `@Genie Bot search MCP documentation`
- `@Genie Bot calculate 50000 Enterprise`

**Highlight:** Same `mcp_client` as CLI!

### Step 5: Teams Bot (2 min)

**Show:** `demos/03-teams/teams_bot.py`

**Key Points:**
- Bot Framework for enterprise
- Same routing logic as Slack (80% code reuse!)
- Adaptive cards for rich UI

**Demo:** Run with Bot Framework Emulator

**Highlight:** Compare with Slack - nearly identical code!

---

## Key Talking Points

### 1. Code Reuse

**Show:** `grep -r "from shared.mcp_client import" demos/`

**Result:** All 4 platforms import the same client!

### 2. Single Point of Maintenance

**Show:** `shared/mcp_client.py` (260 lines)

**Point:** Bug fix here = fixed everywhere!

### 3. Protocol Standardization

**Show:** The `query()` method signature

**Point:** Same protocol for Genie, Vector Search, UC Functions

### 4. Metrics

**Show:** `comparison/without-mcp/metrics.md`

**Numbers:**
- Without MCP: ~2,100 lines
- With MCP: ~430 lines
- **79% reduction**
- **80% code reuse**

---

## Troubleshooting During Demo

### Issue: "No authentication available"

**Quick Fix:**
```bash
echo "USE_MOCK_MCP=true" >> .env
```

### Issue: "GENIE_SPACE_ID not set"

**Quick Fix:**
```bash
echo "GENIE_SPACE_ID=mock-space-id" >> .env
```

### Issue: Import errors

**Quick Fix:**
```bash
# Make sure you're in project root
cd /path/to/mcp-integration-blog
source venv/bin/activate
pip install -r requirements.txt
```

---

## Demo Checklist

Before starting:
- [ ] Virtual environment activated
- [ ] Dependencies installed
- [ ] `.env` file configured (or USE_MOCK_MCP=true)
- [ ] Test CLI works: `python demos/01-cli/genie_cli.py`
- [ ] Test full demo: `python demos/01-cli/genie_cli_full.py`

During demo:
- [ ] Show the problem (comparison/without-mcp/)
- [ ] Show the solution (shared/mcp_client.py)
- [ ] Demo CLI with `/demo` command
- [ ] Show code reuse (grep for imports)
- [ ] Compare Slack vs Teams code
- [ ] Highlight metrics (79% reduction, 80% reuse)

After demo:
- [ ] Q&A
- [ ] Point to documentation
- [ ] Share GitHub repo

---

## Closing Statement

**"MCP transforms enterprise AI integration from M×N complexity to M+N simplicity through protocol standardization. One universal client, multiple platforms, multiple data sources - that's the power of Model Context Protocol."**

---

## Next Steps for Audience

1. **Try it yourself:**
   ```bash
   git clone <repo-url>
   cd mcp-integration-blog
   python -m venv venv
   source venv/bin/activate
   pip install -r requirements.txt
   echo "USE_MOCK_MCP=true" > .env
   cd demos/01-cli && python genie_cli.py
   ```

2. **Read the docs:**
   - `docs/setup-guide.md` - Detailed setup
   - `docs/CURSOR_IMPLEMENTATION_GUIDE.md` - Implementation guide
   - `comparison/without-mcp/README.md` - Before/after comparison

3. **Deploy your own:**
   - Use your Databricks workspace
   - Create Genie Space
   - Deploy Slack bot to Databricks Apps
   - Configure Claude Desktop

---

**Duration:** 5-10 minutes  
**Audience:** Developers, architects, data engineers  
**Level:** Intermediate  
**Prerequisites:** Python, basic Databricks knowledge

