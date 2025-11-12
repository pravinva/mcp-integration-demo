# Introduction to Genie and MCP

## What is Databricks Genie?

Databricks Genie is an AI-powered analytics assistant that allows users to query data using natural language. Instead of writing SQL queries, users can ask questions like:

- "What was our Q4 revenue?"
- "Show me the top 5 customers by sales"
- "Compare this quarter's performance to last quarter"

Genie understands the context of your data, generates SQL queries automatically, executes them, and returns results in a conversational format.

## What is Model Context Protocol (MCP)?

Model Context Protocol (MCP) is a standardized protocol developed by Anthropic (and adopted by Databricks) that enables AI applications to communicate with data sources and tools in a consistent way.

### Key Concepts

**MCP Servers:**
- Expose capabilities (tools, resources) through a standardized interface
- Databricks provides MCP servers for Genie, Vector Search, and Unity Catalog Functions
- Each server has a unique endpoint URL

**MCP Clients:**
- Applications that connect to MCP servers
- Use the same protocol regardless of which server they're connecting to
- Handle authentication, tool discovery, and execution

**The Protocol:**
- Standardized JSON-RPC over HTTP/2
- Tool discovery: clients can query available tools
- Tool execution: clients call tools with parameters
- Consistent error handling and response formats

## Why Use MCP for Multi-Platform Integration?

### The M×N Problem

Without MCP, integrating multiple platforms with multiple data sources creates exponential complexity:

```
Platforms: Slack, Teams, CLI, Claude
Data Sources: Genie, Vector Search, UC Functions

Traditional approach: 4 platforms × 3 sources = 12 custom integrations
```

Each integration requires:
- Custom authentication logic
- Custom API clients
- Custom error handling
- Custom response parsing
- Individual maintenance and updates

### The M+N Solution

With MCP, you build:

```
1 Universal MCP Client (works with all servers)
+ 3 MCP Servers (provided by Databricks)
+ 4 Platform Wrappers (thin UI adapters)
= 8 components total
```

**Benefits:**
- **Code Reuse:** One client works with all data sources
- **Consistency:** Same protocol, same error handling, same patterns
- **Maintainability:** Update once, works everywhere
- **Scalability:** Add new platforms or data sources easily

## How MCP Works with Genie

### Architecture Flow

```
1. User asks question in Slack/Teams
   ↓
2. Bot receives message
   ↓
3. Bot calls MCP client: ask_genie(space_id, question)
   ↓
4. MCP client connects to Genie MCP Server
   ↓
5. Genie MCP Server processes query
   ↓
6. Genie generates SQL and executes
   ↓
7. Results flow back through MCP protocol
   ↓
8. Bot formats and displays to user
```

### The MCP Endpoint

Genie MCP Server endpoint format:
```
https://<workspace-hostname>/api/2.0/mcp/genie/{space_id}
```

Example:
```
https://your-workspace.cloud.databricks.com/api/2.0/mcp/genie/01f0be3dcc771e60ada71b6ec9f61870
```

### Tool Discovery

The Genie MCP Server exposes a tool called `query_space_{space_id}` that accepts:
- `query`: The natural language question
- `conversation_id`: Optional, for multi-turn conversations

### Authentication

MCP uses Databricks Workspace Client authentication:
- Personal Access Tokens (PAT) for development
- OAuth 2.0 for production
- Azure Active Directory for enterprise

## Real-World Example

Consider a financial services company with:
- **Slack** for engineering teams
- **Microsoft Teams** for business units
- **CLI** for data scientists
- **Claude Desktop** for knowledge workers

All need access to the same Genie analytics.

**Without MCP:**
- 4 separate Genie integrations
- 4 separate authentication setups
- 4 separate error handling implementations
- 4x the maintenance burden

**With MCP:**
- 1 universal MCP client (used by all 4 platforms)
- 1 authentication setup
- 1 error handling implementation
- Shared maintenance and updates

## What You'll Build

In this tutorial, you'll create:

1. **Slack Bot** - Responds to @mentions and DMs, queries Genie via MCP
2. **Teams Bot** - Responds to messages, queries Genie via MCP

Both bots use the **same MCP client code**, demonstrating the M+N pattern in practice.

## Next Steps

- [Connection Methods](02-connection-methods.md) - Learn about the three ways to connect to Genie
- [Prerequisites](03-prerequisites.md) - Set up your environment

