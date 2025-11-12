# Connection Methods: When to Use Each

There are three primary ways to connect to Databricks Genie. This guide explains each method and when to use it.

## Method 1: Genie Conversational API

### What It Is

Direct REST API calls to Genie's conversational endpoints. You make HTTP requests directly to Genie's API.

**Endpoint Format:**
```
POST /api/2.0/genie/conversations/{conversation_id}/messages
```

### How It Works

```python
import requests
from databricks.sdk import WorkspaceClient

workspace_client = WorkspaceClient()
headers = workspace_client.config.authenticate()

response = requests.post(
    f"{workspace_url}/api/2.0/genie/conversations/{conv_id}/messages",
    headers=headers,
    json={"query": "What was Q4 revenue?"}
)
```

### When to Use

**Use Conversational API if:**
- Building a single-platform integration
- Full control over request/response handling is required
- Custom conversation flow extensions are needed
- Legacy system integration is necessary

**Avoid if:**
- Supporting multiple platforms (Slack, Teams, CLI, etc.)
- Standardized error handling and tool discovery is preferred
- Reducing maintenance burden is a priority

### Pros and Cons

**Pros:**
- Direct control over API calls
- Can customize request/response format
- No protocol abstraction layer

**Cons:**
- Platform-specific code for each integration
- Manual error handling
- No tool discovery mechanism
- More code to maintain

---

## Method 2: Genie MCP Server (Recommended)

### What It Is

Standardized protocol-based integration using Model Context Protocol. Databricks provides a managed MCP server for Genie.

**Endpoint Format:**
```
https://<workspace>/api/2.0/mcp/genie/{space_id}
```

### How It Works

```python
from shared.mcp_client import create_mcp_client

mcp_client = create_mcp_client()
response, conv_id = await mcp_client.ask_genie(
    space_id="01f0be3dcc771e60ada71b6ec9f61870",
    question="What was Q4 revenue?"
)
```

### When to Use

**Use MCP Server if:**
- Building multi-platform integrations (Slack, Teams, CLI, etc.)
- Standardized protocol and error handling is required
- Code duplication across platforms must be minimized
- Centralized maintenance and updates are priorities
- Production applications need enterprise-grade reliability

**Avoid if:**
- Only one platform is needed with maximum control requirements
- Custom protocol modifications are essential
- MCP servers are unavailable in the workspace

### Pros and Cons

**Pros:**
- Standardized protocol - consistent code across all platforms
- Tool discovery - automatic identification of available tools
- Error handling - unified response format and exception handling
- Code reuse - single client implementation supporting multiple platforms
- Scalability - straightforward addition of new platforms or data sources
- Managed service - no server deployment or maintenance required

**Cons:**
- Requires MCP server availability within the workspace
- Minimal protocol overhead (negligible for most use cases)
- Reduced direct control compared to direct REST API calls

### This Tutorial's Focus

**This tutorial focuses on Method 2 (MCP Server)** because it's the best choice for multi-platform integrations and demonstrates the M+N pattern.

---

## Method 3: Agentic Integration

### What It Is

Using Databricks Agent Framework to create conversational agents that can interact with Genie and other tools. Agents handle complex workflows and tool orchestration.

### How It Works

Agents use the Agent Framework to:
- Understand user intent
- Select appropriate tools (Genie, Vector Search, UC Functions)
- Orchestrate multi-step workflows
- Handle errors and retries

### When to Use

**Use Agentic Integration if:**
- Complex multi-step workflows requiring orchestration
- Intelligent tool selection based on user intent is required
- Conversation memory and context management across sessions
- Sophisticated AI assistants with autonomous capabilities
- Multi-tool coordination and decision-making are needed

**Avoid if:**
- Simple query-response patterns are sufficient
- Direct control over tool selection is required
- Minimal complexity is preferred

### Pros and Cons

**Pros:**
- Intelligent tool orchestration
- Handles complex workflows
- Built-in conversation management
- Can combine multiple data sources automatically

**Cons:**
- More complex setup
- Requires Agent Framework knowledge
- Less control over individual tool calls
- May be overkill for simple use cases

---

## Decision Matrix

| Scenario | Recommended Method | Reason |
|----------|-------------------|--------|
| Single platform, simple queries | Conversational API | Direct control, straightforward implementation |
| Multiple platforms, simple queries | **MCP Server** | Code reuse, standardization |
| Single platform, complex workflows | Conversational API | Full control over orchestration |
| Multiple platforms, complex workflows | Agentic Integration | Intelligent orchestration across platforms |
| Production multi-platform application | **MCP Server** | Operational efficiency, scalability |
| Prototype/MVP | Conversational API | Rapid implementation |
| Enterprise deployment | **MCP Server** | Standardization, vendor support |

## Real-World Examples

### Example 1: Slack Bot for Analytics

**Scenario:** Engineering team needs Genie access in Slack

**Choice:** **MCP Server**
- Same code implementation can be reused for Teams integration
- Standardized error handling and tool discovery
- Simplified integration of Vector Search or UC Functions in future phases

### Example 2: Custom Dashboard Integration

**Scenario:** Single web dashboard needs Genie queries

**Choice:** Conversational API
- Only one platform
- Need custom UI/UX
- Full control over request/response

### Example 3: Multi-Tool AI Assistant

**Scenario:** AI assistant that queries Genie, searches docs, executes functions

**Choice:** Agent-Based Integration
- Enables complex multi-tool workflows
- Automatic tool selection based on user intent
- Multi-step reasoning and execution

## Summary

**For multi-platform integration (Teams and Slack):**

MCP Server is the recommended approach because it:
1. Supports multiple platforms with unified code
2. Implements standardized protocol reducing complexity
3. Enables centralized maintenance and extension
4. Provides production-ready architecture
5. Demonstrates the M+N integration pattern

## Next Steps

- [Prerequisites](03-prerequisites.md) - Configure your environment
- [MCP Setup](04-mcp-setup.md) - Initialize Genie MCP Server

