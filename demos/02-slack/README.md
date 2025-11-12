# Slack Bot Setup Guide

This guide shows how to run the Slack bot locally and deploy it to Databricks Apps.

## Local Testing (Socket Mode)

### Prerequisites

1. **Slack App Created**
   - Go to https://api.slack.com/apps
   - Create new app or select existing

2. **Bot Token Scopes**
   - Go to "OAuth & Permissions"
   - Add Bot Token Scopes:
     - `app_mentions:read` - Listen for @mentions
     - `chat:write` - Send messages
     - `im:read` - Read DMs
     - `im:write` - Send DMs

3. **Socket Mode Enabled**
   - Go to "Socket Mode"
   - Enable Socket Mode
   - Create App-Level Token with `connections:write` scope
   - Copy the token (starts with `xapp-`)

4. **Install App**
   - Go to "Install App"
   - Install to workspace
   - Copy Bot User OAuth Token (starts with `xoxb-`)

### Configuration

Add to `.env` file:

```bash
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_APP_TOKEN=xapp-your-app-token-here
GENIE_SPACE_ID=your-genie-space-id
```

### Run Locally

```bash
cd demos/02-slack
python test_slack_bot.py
```

Or directly:

```bash
python slack_bot.py
```

### Testing

1. **DM the bot:**
   - Open Slack
   - Find your bot user
   - Send DM: "What was Q4 revenue?"

2. **@mention in channel:**
   - Add bot to channel
   - @mention: "@Genie Bot search MCP documentation"

3. **Commands:**
   - `@Genie Bot calculate 50000 Enterprise`
   - `@Genie Bot search how to use Genie`
   - `@Genie Bot what was Q4 revenue?`

## Deployment to Databricks Apps

### Step 1: Prepare Secrets

Store Slack tokens as Databricks secrets:

```bash
# Create secret scope (if not exists)
databricks secrets create-scope --scope slack-bot

# Store tokens
databricks secrets put --scope slack-bot --key slack-bot-token
databricks secrets put --scope slack-bot --key slack-app-token
databricks secrets put --scope slack-bot --key databricks-oauth-client-id
databricks secrets put --scope slack-bot --key databricks-oauth-client-secret
```

### Step 2: Update app.yaml

Edit `app.yaml`:
- Update `GENIE_SPACE_ID` with your space ID
- Verify secret references match your secret scope name

### Step 3: Deploy

```bash
cd demos/02-slack
databricks apps deploy genie-slack-bot
```

### Step 4: Configure Slack

Update Slack app settings:
- **Event Subscriptions**: Enable and set Request URL to Databricks Apps endpoint
- **Interactivity**: Enable and set Request URL
- **OAuth Redirect URLs**: Add Databricks Apps callback URL

## Features

### 1. Natural Language Analytics (Genie)

Just ask questions:
- "What was Q4 revenue?"
- "Show me top 5 customers"
- "Compare Q3 vs Q4"

### 2. Documentation Search (Vector Search)

Start with "search":
- "search how to create Genie space"
- "search MCP integration guide"

### 3. Calculations (UC Functions)

Start with "calculate" or "discount":
- "calculate 50000 Enterprise"
- "discount 25000 Mid-Market"

### 4. Conversation Context

- Maintains context within threads
- Use `/reset` to start fresh
- Use `/help` for commands

## Troubleshooting

### Bot Not Responding

1. Check bot is running: `ps aux | grep slack_bot`
2. Check Slack app is installed to workspace
3. Verify tokens in `.env` are correct
4. Check Socket Mode is enabled

### "Invalid token" Error

- Verify `SLACK_BOT_TOKEN` starts with `xoxb-`
- Verify `SLACK_APP_TOKEN` starts with `xapp-`
- Regenerate tokens if needed

### Bot Not in Channel

- Add bot to channel: `/invite @Genie Bot`
- Or mention bot: `@Genie Bot help`

## Code Reuse

Notice: The Slack bot uses the **same** `shared/mcp_client.py` as:
- CLI (`demos/01-cli/`)
- Teams bot (`demos/03-teams/`)
- Claude Desktop (`demos/04-claude/`)

That's the M+N pattern in action! 🎉

