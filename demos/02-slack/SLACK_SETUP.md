# Slack App Setup Guide - Step by Step

This guide walks you through creating and configuring a Slack app for the Genie bot.

## ⏱️ Time Required: 10-15 minutes

## Step 1: Create Slack App

1. **Go to Slack API**
   - Visit: https://api.slack.com/apps
   - Sign in with your Slack account

2. **Create New App**
   - Click **"Create New App"** button (top right)
   - Select **"From scratch"**
   - Enter:
     - **App Name**: `Databricks Genie Bot` (or any name)
     - **Pick a workspace**: Select your workspace
   - Click **"Create App"**

✅ **Result:** You'll see the app's "Basic Information" page

---

## Step 2: Enable Socket Mode

1. **Navigate to Socket Mode**
   - In left sidebar, click **"Socket Mode"**
   - Toggle **"Enable Socket Mode"** to ON

2. **Create App-Level Token**
   - Click **"Generate Token"** button
   - Enter token name: `genie-bot-connections`
   - Click **"Generate"**
   - **COPY THE TOKEN** (starts with `xapp-`)
   - ⚠️ **Save it!** You won't see it again.

✅ **Result:** Socket Mode enabled, App-Level Token created

---

## Step 3: Configure Bot Token Scopes

1. **Navigate to OAuth & Permissions**
   - In left sidebar, click **"OAuth & Permissions"**
   - Scroll down to **"Scopes"** section
   - Under **"Bot Token Scopes"**, click **"Add an OAuth Scope"**

2. **Add Required Scopes**
   Add these scopes one by one:
   - ✅ `app_mentions:read` - Listen for @mentions
   - ✅ `chat:write` - Send messages
   - ✅ `im:read` - Read direct messages
   - ✅ `im:write` - Send direct messages

✅ **Result:** All 4 scopes added under "Bot Token Scopes"

---

## Step 4: Install App to Workspace

1. **Install App**
   - Still on "OAuth & Permissions" page
   - Scroll to top
   - Click **"Install to Workspace"** button
   - Review permissions
   - Click **"Allow"**

2. **Copy Bot User OAuth Token**
   - After installation, you'll see **"Bot User OAuth Token"**
   - **COPY THE TOKEN** (starts with `xoxb-`)
   - ⚠️ **Save it!** This is your `SLACK_BOT_TOKEN`

✅ **Result:** App installed, Bot Token copied

---

## Step 5: Add Bot to Your .env File

1. **Create or edit `.env` file** in project root:
   ```bash
   cd /path/to/mcp-integration-blog
   nano .env  # or use your favorite editor
   ```

2. **Add Slack tokens:**
   ```bash
   # Slack Configuration
   SLACK_BOT_TOKEN=xoxb-your-bot-token-here
   SLACK_APP_TOKEN=xapp-your-app-token-here
   
   # Databricks (if not already set)
   GENIE_SPACE_ID=your-genie-space-id
   ```

3. **Replace placeholders:**
   - `xoxb-your-bot-token-here` → Your Bot User OAuth Token
   - `xapp-your-app-token-here` → Your App-Level Token
   - `your-genie-space-id` → Your Genie Space ID

✅ **Result:** Tokens saved in `.env` file

---

## Step 6: Test the Bot

1. **Start the bot:**
   ```bash
   cd demos/02-slack
   python test_slack_bot.py
   ```

   Or directly:
   ```bash
   python slack_bot.py
   ```

2. **You should see:**
   ```
   ✅ Slack tokens configured
   ✅ Databricks configuration valid
   🚀 Bot is running...
   ```

3. **Test in Slack:**
   - Open Slack
   - Find your bot user (search for app name)
   - Send a DM: `What was Q4 revenue?`
   - Bot should respond!

✅ **Result:** Bot running and responding

---

## Step 7: Add Bot to Channel (Optional)

1. **Invite bot to channel:**
   - Go to any channel
   - Type: `/invite @Databricks Genie Bot`
   - Or mention: `@Databricks Genie Bot help`

2. **Test @mentions:**
   - In channel: `@Databricks Genie Bot what was Q4 revenue?`
   - Bot responds in thread

✅ **Result:** Bot works in channels too

---

## 🎯 Quick Checklist

- [ ] App created at https://api.slack.com/apps
- [ ] Socket Mode enabled
- [ ] App-Level Token created (`xapp-...`)
- [ ] Bot Token Scopes added (4 scopes)
- [ ] App installed to workspace
- [ ] Bot User OAuth Token copied (`xoxb-...`)
- [ ] Tokens added to `.env` file
- [ ] Bot tested and responding

---

## 🐛 Troubleshooting

### "Invalid token" error
- ✅ Verify `SLACK_BOT_TOKEN` starts with `xoxb-`
- ✅ Verify `SLACK_APP_TOKEN` starts with `xapp-`
- ✅ Check for extra spaces or quotes in `.env`

### Bot not responding
- ✅ Check bot is running (`python slack_bot.py`)
- ✅ Verify app is installed to workspace
- ✅ Check bot is added to channel (for @mentions)
- ✅ Check console for error messages

### "Missing scope" error
- ✅ Go back to "OAuth & Permissions"
- ✅ Verify all 4 scopes are added
- ✅ Reinstall app to workspace (click "Reinstall to Workspace")

### Bot not appearing in Slack
- ✅ Check app is installed to workspace
- ✅ Look for bot user in "Apps" section
- ✅ Try searching for your app name

---

## 📸 Visual Guide (What You'll See)

### Step 1: Create App
```
[Create New App] → [From scratch] → Enter name → Create
```

### Step 2: Socket Mode
```
Socket Mode → Enable Socket Mode: ON → Generate Token → Copy token
```

### Step 3: OAuth Scopes
```
OAuth & Permissions → Bot Token Scopes → Add:
- app_mentions:read
- chat:write
- im:read
- im:write
```

### Step 4: Install
```
OAuth & Permissions → Install to Workspace → Allow → Copy Bot Token
```

---

## 🎉 Success!

Once setup is complete, you can:

- ✅ DM the bot: `What was Q4 revenue?`
- ✅ @mention in channel: `@Genie Bot search MCP docs`
- ✅ Calculate: `@Genie Bot calculate 50000 Enterprise`
- ✅ Get help: `@Genie Bot help`

**All using the same `shared/mcp_client.py` as CLI, Claude, and Teams!** 🚀

---

## 💡 Pro Tips

1. **Test in DM first** - Easier to debug
2. **Check console logs** - Shows what bot receives
3. **Use `/reset`** - Clear conversation context
4. **Thread replies** - Bot maintains context in threads

---

## 📚 Next Steps

After Slack bot works:
- ✅ Deploy to Databricks Apps (see `demos/02-slack/README.md`)
- ✅ Test Teams bot with Emulator
- ✅ Configure Claude Desktop MCP

All platforms ready! 🎉

