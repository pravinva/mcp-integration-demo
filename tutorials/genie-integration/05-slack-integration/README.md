# Slack Integration Tutorial

Complete guide to building a Slack bot that connects to Databricks Genie via MCP.

## Overview

You'll build a Slack bot that:
- Responds to @mentions in channels
- Handles direct messages
- Queries Genie via MCP Server
- Formats responses for Slack

## Tutorial Steps

1. [Create Slack App](01-create-slack-app.md) - Set up your Slack application
2. [Configure OAuth](02-configure-oauth.md) - Set permissions and scopes
3. [Enable Socket Mode](03-enable-socket-mode.md) - No public URL needed!
4. [Implement Bot](04-implement-bot.md) - Write the bot code
5. [Deploy to Databricks Apps](05-deploy-databricks-apps.md) - Production deployment
6. [Testing](06-testing.md) - Test your bot

## Architecture

```
Slack User
    ↓
Slack Platform
    ↓
Slack Bot (slack_bot.py)
    ↓
shared/mcp_client.py  ← THE SHARED INTEGRATION!
    ↓
Genie MCP Server
    ↓
Genie Space
```

## What You'll Build

A production-ready Slack bot that:
- Answers analytics questions using Genie
- Maintains conversation context across interactions
- Handles errors with user-friendly messaging
- Implements rich Slack formatting for responses
- Operates in both channels and direct messages

## Quick Start

To begin implementation:

```bash
# 1. Create Slack application (follow step 1)
# 2. Configure tokens and add to .env
# 3. Launch the bot
python slack_bot.py
```

## Next Step

Start with [Create Slack App](01-create-slack-app.md)

