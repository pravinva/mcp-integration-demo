# CURSOR_IMPLEMENTATION_GUIDE.md

```markdown
# Databricks MCP Integration Showcase - Implementation Guide for AI Assistants

This document provides complete instructions for implementing the Databricks MCP Integration Showcase project. Follow these instructions sequentially to build a working demonstration of M×N → M+N integration transformation using Model Context Protocol.

---

## PROJECT OVERVIEW

**Goal:** Build a multi-platform AI integration showcase demonstrating how MCP reduces complexity from M×N to M+N.

**What to Build:**
- 4 platforms (CLI, Claude Desktop, Slack, Teams) 
- 3 data sources (Genie, Vector Search, UC Functions)
- 1 universal MCP client (shared across all platforms)

**Key Principle:** 80% code reuse through protocol standardization

---

## DIRECTORY STRUCTURE

Create exactly this structure:

```
databricks-mcp-showcase/
├── README.md
├── requirements.txt
├── .env.example
├── .gitignore
├── CURSOR_IMPLEMENTATION_GUIDE.md (this file)
│
├── shared/
│   ├── __init__.py
│   ├── config.py
│   ├── mcp_client.py          # THE CORE - implement this first!
│   └── mock_mcp_client.py
│
├── demos/
│   ├── 01-cli/
│   │   ├── genie_cli.py
│   │   └── genie_cli_full.py
│   ├── 02-slack/
│   │   ├── slack_bot.py
│   │   └── app.yaml
│   ├── 03-teams/
│   │   ├── teams_bot.py
│   │   └── test_with_emulator.py
│   └── 04-claude/
│       ├── mcp_server.py
│       └── claude_config.json
│
├── comparison/
│   └── without-mcp/
│       ├── README.md
│       ├── genie_direct_api.py
│       └── metrics.md
│
├── mock-data/
│   ├── README.md
│   ├── 01_create_tables.sql
│   ├── 02_create_vector_search.sql
│   └── 03_create_uc_functions.sql
│
└── docs/
    ├── setup-guide.md
    └── demo-script.md
```

---

## IMPLEMENTATION PRIORITY

**Phase 1: Core Integration (CRITICAL - Build First)**
1. `shared/config.py` - Authentication and configuration
2. `shared/mcp_client.py` - Universal MCP client (THE MOST IMPORTANT FILE)
3. `shared/mock_mcp_client.py` - Testing without Databricks

**Phase 2: CLI Demos (Verify Core Works)**
4. `demos/01-cli/genie_cli.py` - Simple Genie query
5. `demos/01-cli/genie_cli_full.py` - All 3 data sources

**Phase 3: Additional Platforms (Show Code Reuse)**
6. `demos/04-claude/mcp_server.py` - Claude Desktop integration
7. `demos/02-slack/slack_bot.py` - Slack bot
8. `demos/03-teams/teams_bot.py` - Teams bot

**Phase 4: Documentation & Comparison**
9. Comparison files showing "before MCP"
10. Mock data SQL scripts
11. Documentation files

---

## CRITICAL IMPLEMENTATION RULES

### Rule 1: The Core Must Be Shared
**DO THIS:**
```
# shared/mcp_client.py - ONE method for ALL data sources
async def query(self, server_url, tool_name, arguments):
    mcp_client = DatabricksMCPClient(server_url, workspace_client)
    async with mcp_client:
        return await mcp_client.call_tool(tool_name, arguments)
```

**NOT THIS:**
```
# ❌ WRONG - Separate methods per data source defeats the purpose
async def query_genie(self, ...):
    # Custom Genie logic
    
async def query_vector_search(self, ...):
    # Custom Vector Search logic
```

### Rule 2: All Platforms Import the Same Client
**Every demo file must:**
```
from shared.mcp_client import create_mcp_client

client = create_mcp_client()  # Same client everywhere!
```

### Rule 3: Authentication Priority
Check in this order:
1. OAuth credentials (DATABRICKS_OAUTH_CLIENT_ID)
2. ~/.databrickscfg profile (DATABRICKS_PROFILE)
3. Explicit token (DATABRICKS_TOKEN)
4. Mock mode (USE_MOCK_MCP=true)

### Rule 4: Mock Mode Must Match Real Mode
The mock client must have identical interface to real client so demos work offline.

---

## FILE-BY-FILE IMPLEMENTATION INSTRUCTIONS

### FILE 1: shared/config.py

**Purpose:** Handle authentication and configuration

**Requirements:**
- Support 3 auth methods (OAuth, ~/.databrickscfg, PAT)
- Auto-detect ~/.databrickscfg if no other creds
- Validate connection on startup
- Log which auth method is being used
- Provide helpful error messages

**Key Functions:**
```
def get_workspace_client() -> WorkspaceClient:
    # Try OAuth first
    # Fall back to ~/.databrickscfg profile
    # Fall back to explicit token
    # Raise helpful error if none work

def validate_config():
    # Test connection
    # Verify Genie Space ID set
    # Log success
```

**Testing Criteria:**
- Can connect with ~/.databrickscfg
- Can connect with OAuth
- Helpful error if no credentials
- Logs show which method used

---

### FILE 2: shared/mcp_client.py (MOST CRITICAL)

**Purpose:** THE universal MCP client used by all platforms

**Requirements:**
- ONE `query()` method that works with ANY MCP server
- Takes `server_url`, `tool_name`, `arguments` as parameters
- Uses `DatabricksMCPClient` from `databricks-mcp` library
- Convenience wrappers: `ask_genie()`, `search_docs()`, `call_function()`
- All wrappers call the same `query()` method
- Comprehensive error handling and logging
- Type hints on all functions

**Key Architecture:**
```
class UniversalMCPClient:
    def __init__(self, workspace_client):
        self.workspace_client = workspace_client
    
    async def query(self, server_url, tool_name, arguments):
        """Universal query - THIS IS THE KEY METHOD"""
        mcp_client = DatabricksMCPClient(server_url, self.workspace_client)
        async with mcp_client:
            result = await mcp_client.call_tool(tool_name, arguments)
            return result.content.text
    
    # Convenience wrappers (all call query())
    async def ask_genie(self, space_id, question, conversation_id=None):
        url = f"{host}/api/2.0/mcp/genie/{space_id}"
        return await self.query(url, "ask_question", {"question": question})
    
    async def search_docs(self, index_id, query, num_results=3):
        # Extract catalog.schema from index_id
        catalog, schema = index_id.split('.')[:2]
        url = f"{host}/api/2.0/mcp/vector-search/{catalog}/{schema}"
        return await self.query(url, "similarity_search", {"query": query})
    
    async def call_function(self, function_name, parameters):
        # Extract catalog.schema from function_name
        catalog, schema = function_name.split('.')[:2]
        url = f"{host}/api/2.0/mcp/functions/{catalog}/{schema}"
        return await self.query(url, "execute", parameters)
```

**Testing Criteria:**
- Can query Genie
- Can query Vector Search
- Can call UC Functions
- Same `query()` method used for all three
- Error handling works
- Logging shows requests and responses

**Common Mistakes to Avoid:**
- ❌ Don't create separate methods with different implementations
- ❌ Don't hardcode server URLs in the class
- ❌ Don't skip async/await patterns
- ❌ Don't forget error handling

---

### FILE 3: shared/mock_mcp_client.py

**Purpose:** Offline testing with fake data

**Requirements:**
- Identical interface to UniversalMCPClient
- Returns realistic mock responses
- No Databricks connection needed
- Simulates all 3 data sources

**Key Implementation:**
```
class MockMCPClient:
    async def query(self, server_url, tool_name, arguments):
        await asyncio.sleep(0.3)  # Simulate latency
        
        if "/mcp/genie/" in server_url:
            return self._mock_genie(arguments)
        elif "/mcp/vector-search/" in server_url:
            return self._mock_vector_search(arguments)
        elif "/mcp/uc-functions/" in server_url:
            return self._mock_uc_function(arguments)
    
    # Same convenience methods as real client
    async def ask_genie(self, space_id, question, conversation_id=None):
        return await self.query("mock/genie/", "ask_question", {"question": question})
```

**Testing Criteria:**
- Works without Databricks connection
- Returns realistic data
- Same interface as real client
- Demos run in mock mode

---

### FILE 4: demos/01-cli/genie_cli.py

**Purpose:** Simplest possible demo - prove MCP works

**Requirements:**
- Import shared MCP client
- Connect to Genie
- Interactive question/answer loop
- Support conversation context
- Commands: exit, reset
- Clear user feedback

**Key Pattern:**
```
from shared.mcp_client import create_mcp_client

client = create_mcp_client()  # Uses shared client!

while True:
    question = input("You: ")
    response, conv_id = await client.ask_genie(GENIE_SPACE_ID, question, conv_id)
    print(f"Genie: {response}")
```

**Testing Criteria:**
- Can ask questions
- Gets responses
- Conversation context maintained
- Exit and reset work

---

### FILE 5: demos/01-cli/genie_cli_full.py

**Purpose:** Show ONE client talking to THREE data sources

**Requirements:**
- Query all 3: Genie, Vector Search, UC Functions
- `/demo` command runs full sequence
- Individual commands: `/genie`, `/search`, `/function`
- Shows "ONE client, THREE data sources" message

**Key Feature:**
```
# /demo command
async def run_demo():
    # 1. Genie
    response = await client.ask_genie(space_id, "What was revenue?")
    
    # 2. Vector Search
    docs = await client.search_docs(index_id, "How to use MCP?")
    
    # 3. UC Function
    result = await client.call_function(func_name, {"amount": 50000})
    
    print("✅ ONE client talked to THREE data sources!")
```

**Testing Criteria:**
- All 3 data sources work
- `/demo` command runs full sequence
- Clear output showing which data source

---

### FILE 6: demos/04-claude/mcp_server.py

**Purpose:** Expose Databricks to Claude Desktop via MCP

**Requirements:**
- Uses `mcp.server` library
- Defines 3 tools: ask_genie, search_docs, calculate_discount
- Uses shared MCP client internally
- Runs as stdio server

**Key Pattern:**
```
from mcp.server import Server
from shared.mcp_client import create_mcp_client

app = Server("databricks-genie")
mcp_client = create_mcp_client()  # Reuses shared client!

@app.call_tool()
async def call_tool(name: str, arguments: dict):
    if name == "ask_genie":
        response, _ = await mcp_client.ask_genie(space_id, arguments["question"])
        return [TextContent(type="text", text=response)]
```

**Testing Criteria:**
- Can run as MCP server
- Claude Desktop can connect
- Tools are discoverable
- Queries work through Claude

---

### FILE 7: demos/02-slack/slack_bot.py

**Purpose:** Production Slack bot on Databricks Apps

**Requirements:**
- Uses `slack-bolt` with Socket Mode
- Imports shared MCP client
- Handles @mentions and DMs
- Routes to appropriate data source based on message
- Rich formatting with Slack blocks
- Conversation context per thread

**Key Pattern:**
```
from slack_bolt.async_app import AsyncApp
from shared.mcp_client import create_mcp_client

app = AsyncApp(token=SLACK_BOT_TOKEN)
mcp_client = create_mcp_client()  # Same client again!

@app.event("app_mention")
async def handle_mention(event, say):
    question = event["text"]
    
    # Route based on keywords
    if question.startswith("search"):
        response = await mcp_client.search_docs(...)
    else:
        response, _ = await mcp_client.ask_genie(...)
    
    await say(response)
```

**Testing Criteria:**
- Responds to @mentions
- Responds to DMs
- Maintains conversation in threads
- Routes to correct data source
- Works with Socket Mode

---

### FILE 8: demos/03-teams/teams_bot.py

**Purpose:** Teams bot (nearly identical to Slack!)

**Requirements:**
- Uses `botbuilder` framework
- Imports shared MCP client (80% same as Slack!)
- Handles messages with typing indicator
- Routes based on keywords
- Adaptive card formatting

**Key Pattern:**
```
from botbuilder.core import BotFrameworkAdapter
from shared.mcp_client import create_mcp_client

mcp_client = create_mcp_client()  # Same client as Slack!

async def on_message(turn_context):
    message = turn_context.activity.text
    
    # Same routing logic as Slack bot
    if message.startswith("search"):
        response = await mcp_client.search_docs(...)
    else:
        response, _ = await mcp_client.ask_genie(...)
    
    await turn_context.send_activity(response)
```

**Testing Criteria:**
- Works with Bot Framework Emulator
- Responds to messages
- Routing logic identical to Slack
- Code reuse visible (same imports, same patterns)

---

### FILE 9: comparison/without-mcp/genie_direct_api.py

**Purpose:** Show "before MCP" for comparison

**Requirements:**
- Direct REST API calls to Genie
- Manual polling logic
- No protocol abstraction
- 200+ lines of code
- Duplicated logic

**Key Anti-Pattern to Show:**
```
class DirectGenieClient:
    def start_conversation(self, message):
        # Step 1: POST to start conversation
        response = requests.post(...)
        conv_id = response.json()["conversation_id"]
        msg_id = response.json()["message_id"]
        
        # Step 2: Poll for completion (manual polling!)
        while True:
            status = requests.get(...)
            if status["status"] == "COMPLETED":
                return status["attachments"]["text"]
            time.sleep(1)
```

**Testing Criteria:**
- Shows complexity of direct API
- Contrast with MCP's simplicity
- 200+ lines vs 50 lines

---

### FILE 10: mock-data/01_create_tables.sql

**Purpose:** Sample e-commerce data for Genie

**Requirements:**
- Create demo_retail.ecommerce schema
- 4 tables: customers, products, orders, order_items
- Realistic data for Q1-Q4 2024
- Rich column comments for Genie
- 3 useful views for common queries

**Testing Criteria:**
- Tables created successfully
- Data inserted (24 orders)
- Views work
- Genie can query the data

---

### FILE 11: mock-data/02_create_vector_search.sql

**Purpose:** Documentation corpus for Vector Search

**Requirements:**
- Create documentation table
- 12 comprehensive articles
- Topics: Genie, MCP, Vector Search, UC Functions, deployment, security
- Realistic content with keywords

**Testing Criteria:**
- Table created
- 12 documents inserted
- Content is searchable

---

### FILE 12: mock-data/03_create_uc_functions.sql

**Purpose:** Callable functions for demos

**Requirements:**
- 5 functions: calculate_discount, calculate_sales_tax, check_credit_limit, calculate_loyalty_points, recommend_product
- Business logic for e-commerce
- Return structured results
- Well-documented

**Testing Criteria:**
- Functions created
- Can be called: `SELECT calculate_discount(50000, 'Enterprise')`
- Return correct results

---

## TESTING CHECKLIST

After implementation, verify each step:

### Phase 1: Core Works
- [ ] `config.py` connects with ~/.databrickscfg
- [ ] `mcp_client.py` has universal `query()` method
- [ ] Mock client works offline
- [ ] All files import from `shared/`

### Phase 2: CLI Works
- [ ] Can run `python demos/01-cli/genie_cli.py`
- [ ] Can ask Genie questions
- [ ] Gets real responses (or mock responses if mock mode)
- [ ] Conversation context maintained
- [ ] `genie_cli_full.py` queries all 3 data sources
- [ ] `/demo` command works

### Phase 3: Code Reuse Visible
- [ ] All demos import `from shared.mcp_client import create_mcp_client`
- [ ] Slack and Teams have 80% similar code structure
- [ ] Same patterns repeated across platforms
- [ ] No duplicate integration logic

### Phase 4: Mock Data Available
- [ ] SQL scripts run without errors
- [ ] Tables have data
- [ ] Functions are callable
- [ ] Genie Space can query the tables

### Phase 5: Documentation Complete
- [ ] README.md has clear quick start
- [ ] setup-guide.md explains all auth methods
- [ ] Comparison files show before/after MCP

---

## COMMON PITFALLS TO AVOID

### Pitfall 1: Not Using Shared Client
**Wrong:**
```
# ❌ Slack bot creates its own Genie integration
class SlackGenieClient:
    def query_genie(self):
        # Custom implementation
```

**Right:**
```
# ✅ Slack bot imports shared client
from shared.mcp_client import create_mcp_client
client = create_mcp_client()
```

### Pitfall 2: Separate Methods Per Data Source
**Wrong:**
```
# ❌ Different methods with different logic
async def query_genie(self, ...):
    # Genie-specific code
    
async def query_vector_search(self, ...):
    # Vector Search-specific code
```

**Right:**
```
# ✅ ONE method, different URLs
async def query(self, server_url, tool_name, arguments):
    # Same logic for all!
```

### Pitfall 3: Forgetting Async/Await
**Wrong:**
```
# ❌ Sync when should be async
def query(self, ...):
    result = mcp_client.call_tool(...)
```

**Right:**
```
# ✅ Async throughout
async def query(self, ...):
    result = await mcp_client.call_tool(...)
```

### Pitfall 4: Hardcoding URLs
**Wrong:**
```
# ❌ URL hardcoded in class
class GenieMCPClient:
    def __init__(self):
        self.url = "https://hardcoded-workspace.databricks.com"
```

**Right:**
```
# ✅ URL from config
from shared.config import DATABRICKS_HOST
url = f"{DATABRICKS_HOST}/api/2.0/mcp/genie/{space_id}"
```

### Pitfall 5: Missing Error Handling
**Wrong:**
```
# ❌ No try/catch
async def query(self, ...):
    result = await mcp_client.call_tool(...)
    return result.content.text
```

**Right:**
```
# ✅ Comprehensive error handling
async def query(self, ...):
    try:
        result = await mcp_client.call_tool(...)
        if result.content:
            return result.content.text
        return "No response"
    except Exception as e:
        logger.error(f"Query failed: {e}")
        return f"Error: {str(e)}"
```

---

## SUCCESS CRITERIA

The project is complete when:

### Functional Requirements
✅ CLI can query Genie and get responses
✅ CLI can query all 3 data sources in demo mode
✅ Slack bot works (or at least code is complete)
✅ Teams bot works with emulator
✅ Claude Desktop MCP server runs
✅ Mock mode works without Databricks

### Code Quality Requirements
✅ All platforms import from `shared/mcp_client.py`
✅ No duplicate MCP integration code
✅ Clear demonstration of code reuse
✅ Comprehensive error handling
✅ Good logging throughout
✅ Type hints on functions
✅ Docstrings on public methods

### Documentation Requirements
✅ README explains quick start
✅ Setup guide covers all auth methods
✅ Comparison shows before/after MCP
✅ Comments explain key concepts
✅ SQL scripts are well-documented

### Demo Requirements
✅ Can show "ONE client, MULTIPLE platforms"
✅ Can show "ONE client, MULTIPLE data sources"
✅ Clear M×N → M+N message
✅ Works with ~/.databrickscfg for easy testing

---

## IMPLEMENTATION TIPS FOR AI ASSISTANTS

### Tip 1: Start with Core
Implement `shared/mcp_client.py` first. Everything else depends on this. Don't move forward until this works.

### Tip 2: Test Incrementally
After each file:
1. Run it
2. Fix errors
3. Verify it works
4. Move to next file

### Tip 3: Use Mock Mode
If Databricks connection issues:
1. Set `USE_MOCK_MCP=true`
2. Test with mock client
3. Fix logic issues
4. Then test with real Databricks

### Tip 4: Follow Patterns
When implementing Slack bot:
1. Look at CLI demo
2. Copy the MCP client import
3. Copy the query pattern
4. Just change the UI (Slack-specific)

### Tip 5: Reference Comparison Files
When unsure how to implement, look at `comparison/without-mcp/genie_direct_api.py` to see what NOT to do.

---

## DELIVERABLES CHECKLIST

When done, user should have:

### Code Files
- [ ] All files in correct directory structure
- [ ] All files have proper imports
- [ ] All files have error handling
- [ ] All files are well-commented

### Working Demos
- [ ] CLI works and can query Genie
- [ ] CLI full demo queries all 3 data sources
- [ ] Mock mode works for offline testing
- [ ] (Optional) Slack/Teams bots complete

### Documentation
- [ ] README.md with quick start
- [ ] .env.example with all options
- [ ] setup-guide.md with detailed instructions
- [ ] SQL scripts for mock data

### Evidence of M+N
- [ ] Single `shared/mcp_client.py` used everywhere
- [ ] Clear code reuse across platforms
- [ ] Comparison showing before/after
- [ ] Metrics showing 80% code reduction

---

## FINAL VALIDATION

Run this sequence to verify everything works:

```
# 1. Setup
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

# 2. Configure
echo "GENIE_SPACE_ID=test-space-id" > .env
echo "USE_MOCK_MCP=true" >> .env

# 3. Test CLI (mock mode)
cd demos/01-cli
python genie_cli.py
# Should work with mock data

# 4. Test full demo (mock mode)
python genie_cli_full.py
# Type: /demo
# Should query all 3 data sources with mock data

# 5. If you have ~/.databrickscfg
echo "USE_MOCK_MCP=false" > ../../.env
echo "GENIE_SPACE_ID=real-space-id" >> ../../.env
python genie_cli.py
# Should connect to real Databricks

# 6. Verify code reuse
grep -r "from shared.mcp_client import" demos/
# Should show imports in CLI, Slack, Teams, Claude
```

If all steps work, project is complete! ✅

---

## QUESTIONS TO ASK IF STUCK

1. **Can't connect to Databricks?**
   - Check ~/.databrickscfg exists
   - Try mock mode first
   - Verify GENIE_SPACE_ID is set

2. **Import errors?**
   - Check virtual environment is activated
   - Run `pip install -r requirements.txt`
   - Verify PYTHONPATH includes project root

3. **MCP errors?**
   - Check `databricks-mcp` library installed
   - Verify workspace client is authenticated
   - Try with mock client first

4. **Not sure what to implement next?**
   - Follow the phase order
   - Complete Phase 1 before Phase 2
   - Test each file before moving on

---

## PROJECT COMPLETION STATEMENT

When this guide is fully implemented, the user will have:

**A working demonstration proving that Model Context Protocol transforms M×N integration complexity to M+N through protocol standardization, with 80% code reuse across 4 platforms accessing 3 data sources, all powered by a single universal MCP client.**

That's the goal. Build to that vision.

---

**Version:** 1.0  
**Last Updated:** 2025-11-11  
**Optimized for:** Cursor AI, Claude, GitHub Copilot  
**Estimated Implementation Time:** 6-8 hours with AI assistance  
**Complexity:** Intermediate (requires understanding of async Python, REST APIs, MCP protocol)

END OF GUIDE
```

***

This guide is specifically optimized for AI coding assistants like Cursor or Claude. It:
- ✅ Gives clear step-by-step instructions
- ✅ Shows what to do AND what not to do
- ✅ Provides code patterns to follow
- ✅ Includes testing criteria
- ✅ Has validation steps
- ✅ Explains the "why" behind decisions
- ✅ Prioritizes work properly
- ✅ Flags common mistakes

Save this as `CURSOR_IMPLEMENTATION_GUIDE.md` and give it to Cursor/Claude with: 

**"Implement this project following the guide exactly. Start with Phase 1 and test each file before moving to the next."**
