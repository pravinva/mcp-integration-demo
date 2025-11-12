# Connecting Teams and Slack to Databricks Genie via MCP

Complete tutorial for integrating Microsoft Teams and Slack with Databricks Genie using the Model Context Protocol (MCP) server.

## Tutorial Structure

1. **[Introduction](01-introduction.md)** - What is Genie, what is MCP, and why use it
2. **[Connection Methods](02-connection-methods.md)** - Three ways to connect and when to use each
3. **[Prerequisites](03-prerequisites.md)** - Setup requirements and credentials
4. **[MCP Setup](04-mcp-setup.md)** - Configure Genie MCP Server
5. **[Slack Integration](05-slack-integration/)** - Complete Slack bot tutorial
6. **[Teams Integration](06-teams-integration/)** - Teams bot with Agents Playground
7. **[Troubleshooting](07-troubleshooting.md)** - Common issues and solutions
8. **[Best Practices](08-best-practices.md)** - Security, performance, and maintenance

## Quick Start

**For Slack:**
```bash
cd 05-slack-integration
# Follow the step-by-step guide
```

**For Teams:**
```bash
cd 06-teams-integration
# Start with development setup (Agents Playground - Free tier available)
```

## Architecture

Both integrations use the **same MCP client** - demonstrating the M+N pattern:

```
Slack/Teams User
    ↓
Platform (Slack/Teams)
    ↓
Bot Application
    ↓
shared/mcp_client.py  ← Shared integration layer
    ↓
Databricks MCP Server
    ↓
Genie Space
```

## Key Benefits

- **Code reuse** - Single MCP client implementation across multiple platforms
- **Standardized protocol** - Consistent interface for platform integration
- **Operational efficiency** - Centralized maintenance and updates
- **Enterprise-ready** - Designed for production deployment across Databricks Apps and Azure

## Learning Outcomes

- Configure and test Genie MCP Server endpoints
- Implement Slack bot integrations with Socket Mode
- Develop Teams bot implementations using Agents Playground
- Deploy applications to production environments
- Evaluate connection method trade-offs for different scenarios

## Getting Started

Begin with [Introduction](01-introduction.md) to understand the architectural patterns, then follow the platform-specific guides for your deployment requirements.

