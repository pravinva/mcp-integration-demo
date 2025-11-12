# How to Chat with Teams Bot - Step by Step

## 🚀 Quick Start Guide

### Step 1: Make Sure Bot is Running

Open a terminal and run:

```bash
cd /Users/pravin.varma/Documents/Demo/mcp-integration-blog/demos/03-teams
source ../../venv/bin/activate
python test_teams_bot.py
```

You should see:
```
🚀 Starting Teams bot...
📍 Bot running on: http://localhost:3978/api/messages
```

**⚠️ Keep this terminal window open!** The bot needs to keep running.

---

### Step 2: Download Bot Framework Emulator

If you haven't already:

1. **Go to:** https://github.com/Microsoft/BotFramework-Emulator/releases
2. **Download** the latest version for your OS:
   - Mac: `.dmg` file
   - Windows: `.exe` installer
   - Linux: `.AppImage` or `.deb`
3. **Install** it

**Time:** ~2 minutes

---

### Step 3: Open Bot Framework Emulator

1. **Launch** Bot Framework Emulator (the app you just installed)
2. You'll see the main window

---

### Step 4: Connect to Your Bot

1. **Click "Open Bot"** button (or File → Open Bot)
2. **In the dialog box, enter:**
   ```
   http://localhost:3978/api/messages
   ```
3. **Leave these fields EMPTY:**
   - Microsoft App ID: (leave empty)
   - Microsoft App Password: (leave empty)
   
   ⚠️ **Important:** For local testing, you don't need Azure credentials!
4. **Click "Connect"**

---

### Step 5: Start Chatting!

Once connected, you'll see:
- A welcome message from the bot
- A chat input box at the bottom

**Try these commands:**

#### 📊 Analytics Questions (Genie)
```
What was Q4 revenue?
Show me top 5 customers
Compare Q3 vs Q4 performance
What was our total revenue in 2024?
```

#### 🔍 Search Documentation (Vector Search)
```
search how to create Genie space
search MCP integration guide
search vector search tutorial
```

#### 💰 Calculate Discounts (UC Functions)
```
calculate 50000 Enterprise
calculate 25000 SMB
calculate 35000 Mid-Market
```

#### ⚙️ Commands
```
/help
/reset
```

---

## 📸 What You'll See

### Welcome Message
When you first connect:
```
👋 Welcome to Databricks Genie!

I can help you with:
📊 Data analytics (ask natural language questions)
🔍 Documentation search (start with "search")
💰 Calculations (start with "calculate")

Try asking:
- "What was our revenue last quarter?"
- "search MCP integration guide"
- "calculate 50000 Enterprise"

Type /help for more information.
```

### Example Conversation

**You type:** `What was Q4 revenue?`

**Bot responds:**
```
🧞 Genie:

[Response with SQL query and Q4 revenue data]
```

**You type:** `search MCP tutorial`

**Bot responds:**
```
📚 Search Results:

[Documentation results from Vector Search]
```

---

## 🐛 Troubleshooting

### "Cannot connect to bot"

**Check:**
1. ✅ Bot is running (check terminal window)
2. ✅ URL is exactly: `http://localhost:3978/api/messages`
3. ✅ No firewall blocking port 3978

**Fix:**
- Make sure bot terminal shows "Bot running on: http://localhost:3978/api/messages"
- Try restarting the bot

### Bot not responding

**Check:**
1. ✅ Bot terminal shows no errors
2. ✅ Check console output in Emulator (bottom panel)
3. ✅ Verify `GENIE_SPACE_ID` is set in `.env`

**Fix:**
- Check bot terminal for error messages
- Try `/help` command first
- Check `.env` file has `GENIE_SPACE_ID`

### Emulator won't start

**Fix:**
- Download latest version from GitHub
- Check system requirements
- Try running as administrator (Windows)

---

## 💡 Pro Tips

1. **Keep bot terminal visible** - Shows logs and helps debug
2. **Use `/reset`** - Clears conversation context
3. **Check Emulator console** - Shows request/response details
4. **Try mock mode** - Set `USE_MOCK_MCP=true` if Databricks not configured

---

## 🎯 Quick Reference

**Start Bot:**
```bash
cd demos/03-teams
python test_teams_bot.py
```

**Emulator URL:**
```
http://localhost:3978/api/messages
```

**Test Commands:**
- `What was Q4 revenue?`
- `search MCP tutorial`
- `calculate 50000 Enterprise`
- `/help`

---

## ✅ Success Checklist

- [ ] Bot is running (terminal shows "Bot running")
- [ ] Bot Framework Emulator installed
- [ ] Connected to `http://localhost:3978/api/messages`
- [ ] Welcome message received
- [ ] Bot responds to questions

**Once all checked, you're ready to chat!** 🎉

---

## 🚀 That's It!

The bot uses the same `shared/mcp_client.py` as:
- ✅ CLI (`demos/01-cli/`)
- ✅ Claude Desktop (`demos/04-claude/`)
- ✅ Slack (`demos/02-slack/`)

**80% code reuse!** That's the M+N pattern in action! 🚀

