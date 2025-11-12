# Slack Local Testing - Real Slack Interface

Test your bot in **actual Slack** using Socket Mode - no ngrok or public URLs needed!

## Prerequisites

1. **Slack Workspace** (you can create a free one)
2. **Admin access** to install apps
3. Python 3.8+ with virtual environment

## Step 1: Create Slack App

1. Go to https://api.slack.com/apps
2. Click **Create New App**
3. Choose **From scratch**
4. **App Name**: `Databricks Genie Bot`
5. **Workspace**: Select your workspace
6. Click **Create App**

## Step 2: Enable Socket Mode

Socket Mode lets you test locally without exposing a public URL!

1. In your app settings, go to **Socket Mode** (left sidebar)
2. Toggle **Enable Socket Mode** to ON
3. Click **Generate Token**
   - **Token Name**: `genie-bot-websocket`
   - **Scope**: Select `connections:write`
4. Click **Generate**
5. **Copy the token** - starts with `xapp-`
6. Click **Done**

## Step 3: Configure Bot Features

### 3a. Add Bot User

1. Go to **App Home** (left sidebar)
2. Under **Your App's Presence in Slack**:
   - Click **Add Bot User**
   - **Display name**: `Genie Bot`
   - **Default username**: `@genie-bot`
   - Toggle **Always Show My Bot as Online** to ON
3. Click **Add Bot User**
4. Click **Save Changes**

### 3b. OAuth & Permissions

1. Go to **OAuth & Permissions** (left sidebar)
2. Scroll to **Scopes** → **Bot Token Scopes**
3. Add these scopes:
   ```
   app_mentions:read
   channels:history
   chat:write
   groups:history
   im:history
   im:read
   im:write
   mpim:history
   users:read
   ```
4. Scroll to top → Click **Install to Workspace**
5. Click **Allow**
6. **Copy the Bot User OAuth Token** - starts with `xoxb-`

### 3c. Event Subscriptions

1. Go to **Event Subscriptions** (left sidebar)
2. Toggle **Enable Events** to ON
3. Under **Subscribe to bot events**, add:
   ```
   app_mention
   message.channels
   message.groups
   message.im
   message.mpim
   ```
4. Click **Save Changes**

**Note:** You don't need a Request URL - Socket Mode handles this!

## Step 4: Configure Environment

Edit `/Users/pravin.varma/Documents/Demo/mcp-integration-blog/.env`:

```bash
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token-from-step-3b
SLACK_APP_TOKEN=xapp-your-app-token-from-step-2

# Databricks Configuration
DATABRICKS_HOST=https://your-workspace.databricks.com
DATABRICKS_TOKEN=your-pat-token
# Or use profile:
DATABRICKS_PROFILE=DEFAULT

# Data Sources
GENIE_SPACE_ID=your-genie-space-id
VECTOR_SEARCH_INDEX_ID=catalog.schema.index_name
UC_FUNCTION_NAME=catalog.schema.calculate_discount

# Optional: Mock mode for testing without Databricks
# USE_MOCK_MCP=true
```

## Step 5: Start Bot

```bash
cd /Users/pravin.varma/Documents/Demo/mcp-integration-blog
source venv/bin/activate
python3 demos/02-slack/slack_bot.py
```

You should see:
```
============================================================
🤖 Starting Slack Genie Bot...
============================================================
✅ Configuration valid
📊 Genie Space: your-space-id
🔍 Vector Search: catalog.schema.index
⚙️ UC Function: catalog.schema.calculate_discount

🚀 Bot is running... Send a DM or @mention me in a channel!
Press Ctrl+C to stop
============================================================
⚡️ Bolt app is running!
```

**Keep this terminal running!**

## Step 6: Chat in Real Slack!

Open Slack (desktop app or web):

### Option 1: Direct Message

1. Click **Apps** in left sidebar
2. Find **Genie Bot**
3. Send messages:
   ```
   What was our Q4 revenue?

   search MCP integration guide

   calculate 50000 Enterprise

   help
   ```

### Option 2: Channel Mention

1. Go to any channel
2. Type: `@Genie Bot What was our revenue?`
3. Bot will reply in thread

### Option 3: Add to Channel

1. Go to channel → Details → Integrations
2. Click **Add apps**
3. Select **Genie Bot**
4. Now you can @mention it in that channel!

## Features You'll See

### 🎨 Rich Formatting
- Slack blocks with sections and dividers
- Formatted code snippets
- Bold/italic text
- Emoji reactions

### 💬 Threading
- Conversations maintain context
- Follow-up questions work
- Each thread has its own conversation ID

### 🏠 App Home Tab
Click the bot in Apps → **Home** tab shows:
- Welcome message
- What the bot can do
- Quick start examples

### ⚡ Real-Time
- Instant responses via WebSocket
- No polling, no delays
- Just like chatting with a person!

## Testing All Features

### 1. Analytics (Genie)
```
What was our total revenue in Q4 2024?
Show me top 5 customers
Compare Q3 vs Q4 performance
```

### 2. Documentation Search (Vector Search)
```
search how to create a Genie space
search MCP protocol documentation
search best practices for Unity Catalog
```

### 3. Business Functions (UC Functions)
```
calculate 50000 Enterprise
calculate 25000 Mid-Market
discount 100000 SMB
```

### 4. Commands
```
/help      - Show help message
/reset     - Start new conversation
reset      - Same as /reset
```

## Socket Mode Benefits

| Feature | Webhook (Traditional) | Socket Mode |
|---------|----------------------|-------------|
| Public URL | Required (ngrok) | **Not needed** ✅ |
| Setup | Complex | **Simple** ✅ |
| Local Testing | Difficult | **Easy** ✅ |
| Firewall | Must allow inbound | **Works anywhere** ✅ |
| Debugging | Hard | **Easy** ✅ |
| Production | Recommended | Also works! ✅ |

## Debugging

### Enable Debug Logging

Edit `slack_bot.py`, add at top:
```python
import logging
logging.basicConfig(level=logging.DEBUG)
```

You'll see:
- Every message received
- Every API call
- Full request/response details

### Set Breakpoints

In VS Code:
1. Set breakpoint in `slack_bot.py`
2. Run → Start Debugging (F5)
3. Select **Python File**
4. Send message in Slack
5. Debugger will pause at breakpoint!

## Common Issues

### "Bot not responding"

**Check:**
1. Terminal shows `⚡️ Bolt app is running!`
2. Bot token starts with `xoxb-`
3. App token starts with `xapp-`
4. Socket Mode is enabled in Slack app settings

**Fix:**
```bash
# Restart bot
Ctrl+C
python3 demos/02-slack/slack_bot.py
```

### "App mention not working"

**Check:**
1. Event Subscriptions are enabled
2. `app_mention` event is subscribed
3. Bot is invited to the channel

**Fix:**
```
# In channel, type:
/invite @Genie Bot
```

### "No response to DM"

**Check:**
1. `message.im` event is subscribed
2. Bot has `im:read` and `im:write` scopes

**Fix:**
Go to OAuth & Permissions → Add missing scopes → Reinstall app

## Deploy to Production

When ready, you have options:

### Option 1: Keep Socket Mode
- Run bot on a server (EC2, Databricks Apps, etc.)
- Socket Mode works in production too!
- No need to change anything

### Option 2: Switch to Webhooks
- Deploy with `app.yaml` to Databricks Apps
- Databricks Apps provides public URL automatically
- Use Event Subscriptions with Request URL

## Next Steps

### Test M×N Integration

Your bot is now talking to:
- ✅ Genie MCP (analytics)
- ✅ Vector Search MCP (documentation)
- ✅ UC Functions MCP (actions)

All using the **same** `shared/mcp_client.py`!

### Customize

Edit `demos/02-slack/slack_bot.py`:
- Add more commands
- Customize formatting
- Add buttons/interactive elements
- Create slash commands

### Monitor

Check bot activity:
- Slack App Management → Your App → **Event Activity**
- See all messages and responses
- Debug failed events

## Resources

- Slack Bolt Python: https://slack.dev/bolt-python/
- Socket Mode Guide: https://api.slack.com/apis/connections/socket
- Block Kit Builder: https://app.slack.com/block-kit-builder
- Slack App Directory: https://api.slack.com/start/overview

---

**🎉 You're now chatting with your bot in real Slack!**

No tunnels, no ngrok, no public URLs - just pure local development! 🚀

## Bonus: Slack vs Teams Comparison

Both use the **same MCP client** (`shared/mcp_client.py`):

| Aspect | Slack | Teams |
|--------|-------|-------|
| Local Testing | Socket Mode | Teams Toolkit |
| Interface | Real Slack | Real Teams |
| Setup | 10 minutes | 15 minutes |
| Features | All 3 MCP servers ✅ | All 3 MCP servers ✅ |
| Code Reuse | 80% shared | 80% shared |
| Threading | ✅ | ✅ |
| Rich Formatting | ✅ | ✅ |

**That's the M+N transformation in action!** One client, multiple platforms! 🎯
