# Teams Bot - Bot Framework Emulator Setup Guide

This guide shows you how to test the Teams bot locally using Bot Framework Emulator - **no Azure needed!**

## ⏱️ Time Required: 5-10 minutes

## Step 1: Download Bot Framework Emulator

1. **Go to Releases Page**
   - Visit: https://github.com/Microsoft/BotFramework-Emulator/releases
   - Download the latest version for your OS:
     - **Mac**: `.dmg` file
     - **Windows**: `.exe` installer
     - **Linux**: `.AppImage` or `.deb` package

2. **Install**
   - **Mac**: Open `.dmg`, drag to Applications
   - **Windows**: Run `.exe` installer
   - **Linux**: Make executable and run

✅ **Result:** Bot Framework Emulator installed

---

## Step 2: Start the Teams Bot

1. **Open terminal** in project directory:
   ```bash
   cd /path/to/mcp-integration-blog
   source venv/bin/activate
   ```

2. **Start the bot:**
   ```bash
   python demos/03-teams/test_teams_bot.py
   ```

3. **You should see:**
   ```
   ======================================================================
   🧪 Teams Bot - Emulator Test Setup
   ======================================================================
   
   ✅ Databricks configuration valid
   
   📍 Bot running on: http://localhost:3978/api/messages
   
   Press Ctrl+C to stop
   ```

✅ **Result:** Bot running on port 3978

**⚠️ Keep this terminal open!** The bot needs to keep running.

---

## Step 3: Connect Emulator to Bot

1. **Open Bot Framework Emulator**
   - Launch the application you just installed

2. **Click "Open Bot"**
   - You'll see a dialog box

3. **Enter Bot URL:**
   ```
   http://localhost:3978/api/messages
   ```

4. **Leave these fields EMPTY** (important!):
   - **Microsoft App ID**: (leave empty)
   - **Microsoft App Password**: (leave empty)
   
   ⚠️ **For local testing, you don't need Azure credentials!**

5. **Click "Connect"**

✅ **Result:** Emulator connected to your bot

---

## Step 4: Test the Bot!

You should see a welcome message. Try these commands:

### 📊 Analytics (Genie)
```
What was Q4 revenue?
Show me top 5 customers
Compare Q3 vs Q4 performance
```

### 🔍 Search Documentation (Vector Search)
```
search how to create Genie space
search MCP integration guide
search vector search tutorial
```

### 💰 Calculate (UC Functions)
```
calculate 50000 Enterprise
calculate 25000 SMB
calculate 35000 Mid-Market
```

### ⚙️ Commands
```
/help
/reset
```

---

## 🎯 What You Should See

### Welcome Message
When you first connect, you'll see:
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

**You:** `What was Q4 revenue?`

**Bot:** 
```
🧞 Genie:

[Response with SQL query and results showing Q4 revenue]
```

**You:** `search MCP tutorial`

**Bot:**
```
📚 Search Results:

[Documentation results from Vector Search]
```

**You:** `calculate 50000 Enterprise`

**Bot:**
```
💰 Calculation:

[Discount calculation result from UC Function]
```

---

## 🐛 Troubleshooting

### "Cannot connect to bot"

**Check:**
1. ✅ Bot is running (`python demos/03-teams/test_teams_bot.py`)
2. ✅ Port 3978 is not blocked by firewall
3. ✅ URL is exactly: `http://localhost:3978/api/messages`
4. ✅ No other app using port 3978

**Fix:**
```bash
# Check if port is in use
lsof -i :3978

# Kill process if needed
kill -9 <PID>
```

### "Bot not responding"

**Check:**
1. ✅ Bot terminal shows no errors
2. ✅ Databricks config is valid (or USE_MOCK_MCP=true)
3. ✅ Check console output for error messages

**Fix:**
- Check `.env` has `GENIE_SPACE_ID` set
- Or set `USE_MOCK_MCP=true` for testing

### Emulator crashes or won't start

**Fix:**
- Download latest version from GitHub
- Check system requirements
- Try running as administrator (Windows)

### "Module not found" error

**Fix:**
```bash
source venv/bin/activate
pip install -r requirements.txt
```

---

## 📸 Visual Guide

### Step 1: Bot Framework Emulator Window
```
┌─────────────────────────────────────┐
│  Bot Framework Emulator             │
│                                     │
│  [Open Bot]  [Settings]  [Help]   │
└─────────────────────────────────────┘
```

### Step 2: Open Bot Dialog
```
┌─────────────────────────────────────┐
│  Connect to a bot                   │
│                                     │
│  Bot URL:                           │
│  http://localhost:3978/api/messages │
│                                     │
│  Microsoft App ID:                  │
│  [leave empty]                      │
│                                     │
│  Microsoft App Password:             │
│  [leave empty]                      │
│                                     │
│  [Cancel]  [Connect]                │
└─────────────────────────────────────┘
```

### Step 3: Chat Window
```
┌─────────────────────────────────────┐
│  Chat with your bot                 │
│                                     │
│  Bot: 👋 Welcome to Databricks...   │
│                                     │
│  You: [Type message here...]        │
│                                     │
└─────────────────────────────────────┘
```

---

## 🎉 Success Indicators

✅ **Bot running:** Terminal shows "Bot running on: http://localhost:3978/api/messages"  
✅ **Emulator connected:** Shows welcome message  
✅ **Bot responds:** Answers your questions  
✅ **All 3 data sources work:** Genie, Vector Search, UC Functions  

---

## 💡 Pro Tips

1. **Keep bot terminal visible** - Shows logs and errors
2. **Use `/reset`** - Clear conversation context
3. **Check console** - Emulator shows request/response details
4. **Try mock mode** - Set `USE_MOCK_MCP=true` if Databricks not configured

---

## 🚀 Next Steps

Once Teams bot works locally:

1. ✅ Test all three data sources
2. ✅ Try different question types
3. ✅ Deploy to Azure Functions (see `README.md`)
4. ✅ Configure Azure Bot resource
5. ✅ Add to Teams workspace

---

## 📚 Related Files

- **Bot code**: `demos/03-teams/teams_bot.py`
- **Test script**: `demos/03-teams/test_teams_bot.py`
- **Full guide**: `demos/03-teams/README.md`

---

## 🎯 Quick Reference

**Start bot:**
```bash
python demos/03-teams/test_teams_bot.py
```

**Emulator URL:**
```
http://localhost:3978/api/messages
```

**Test commands:**
- `What was Q4 revenue?`
- `search MCP tutorial`
- `calculate 50000 Enterprise`
- `/help`

**That's it!** The bot uses the same `shared/mcp_client.py` as CLI, Claude, and Slack! 🚀

