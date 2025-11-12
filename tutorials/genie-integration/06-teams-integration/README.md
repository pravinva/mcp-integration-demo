# Teams Integration Tutorial

Complete guide to building a Microsoft Teams bot that connects to Databricks Genie via MCP.

## Overview

You'll build a Teams bot that:
- Responds to messages in Teams
- Queries Genie via MCP Server
- Uses Agents Playground for development (FREE!)
- Deploys to Azure for production

## Development vs Production

### Development Environment (Free)

**Microsoft 365 Agents Playground:**
- No cost to use
- Teams-like user interface in browser
- No Azure subscription required
- Ideal for development and testing
- No Teams application registration required

### Production Environment (Azure)

**Azure Deployment:**
- Real Microsoft Teams integration
- Production-grade hosting
- Scalable infrastructure
- Enterprise-level features and SLAs

## Tutorial Steps

1. [Development Setup](01-development-setup.md) - Configure Agents Playground (Free tier)
2. [Implement Bot](02-implement-bot.md) - Develop the bot application
3. [Test with Playground](03-test-with-playground.md) - Validate in Teams-like environment
4. [Production Deployment](04-production-deployment.md) - Deploy to Azure (when ready)
5. [Add to Teams](05-add-to-teams.md) - Integrate with real Teams workspace

## Architecture

```
Teams User
    ↓
Microsoft Teams / Agents Playground
    ↓
Teams Bot (teams_bot.py)
    ↓
shared/mcp_client.py  ← THE SAME CODE AS SLACK!
    ↓
Genie MCP Server
    ↓
Genie Space
```

## What You'll Build

A production-ready Teams bot that:
- Answers analytics questions using Genie
- Maintains conversation context across interactions
- Handles errors with user-friendly messaging
- Implements Teams-native formatting for responses
- Operates in both direct chats and team channels

## Quick Start (Development Environment)

```bash
# 1. Install Agents Playground
npm install -g @microsoft/m365agentsplayground

# 2. Start the bot
python teams_bot.py

# 3. Launch the playground
agentsplayground -e "http://localhost:3978/api/messages"
```

## Next Step

Start with [Development Setup](01-development-setup.md) - It's free to begin!

