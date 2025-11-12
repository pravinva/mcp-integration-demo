# Local Testing with Real UI - No Emulators!

Test your Slack and Teams bots in **actual production interfaces** during development.

## 🎯 What You Get

Both platforms support **local testing with real UI**:

| Platform | Tool | Interface | Setup Time |
|----------|------|-----------|------------|
| **Teams** | Teams Toolkit | Real Teams in browser | 15 min |
| **Slack** | Socket Mode | Real Slack (desktop/web) | 10 min |

No emulators, no fake UIs - you're testing in the actual app! ✨

---

## 🟦 Microsoft Teams - Teams Toolkit

**File:** `demos/03-teams/TEAMS_TOOLKIT_SETUP.md`

### Quick Start

1. **Install Teams Toolkit** extension in VS Code
2. **Sign in** to Microsoft 365 (free developer account works)
3. **Start bot server**:
   ```bash
   python3 demos/03-teams/teams_bot.py
   ```
4. **F5** in VS Code → Teams opens in browser with your bot!

### What You Get

- ✅ Real Teams interface in browser
- ✅ Personal chat, channels, group chats
- ✅ Rich cards, @mentions, typing indicators
- ✅ Hot reload - edit code and refresh
- ✅ Full debugging with breakpoints
- ✅ One-click deploy to production

**See full guide:** `demos/03-teams/TEAMS_TOOLKIT_SETUP.md`

---

## 🟩 Slack - Socket Mode

**File:** `demos/02-slack/SLACK_LOCAL_TESTING.md`

### Quick Start

1. **Create Slack app** at https://api.slack.com/apps
2. **Enable Socket Mode** (no public URL needed!)
3. **Configure** `.env` with tokens
4. **Start bot**:
   ```bash
   python3 demos/02-slack/slack_bot.py
   ```
5. Open Slack and **chat with your bot**!

### What You Get

- ✅ Real Slack (desktop or web app)
- ✅ DMs, channels, threads
- ✅ Rich formatting, blocks, buttons
- ✅ No ngrok or tunnels needed
- ✅ WebSocket connection (instant!)
- ✅ Works anywhere (no firewall issues)

**See full guide:** `demos/02-slack/SLACK_LOCAL_TESTING.md`

---

## 🔄 The M×N → M+N Proof

Both bots use the **exact same** `shared/mcp_client.py`:

```python
# In Slack bot
from shared.mcp_client import create_mcp_client
client = create_mcp_client()
response = await client.ask_genie(space_id, question)

# In Teams bot
from shared.mcp_client import create_mcp_client  # SAME IMPORT!
client = create_mcp_client()                      # SAME CLIENT!
response = await client.ask_genie(space_id, question)  # SAME API!
```

### Both Support All 3 Data Sources

| Data Source | Slack | Teams | Code Reuse |
|-------------|-------|-------|------------|
| Genie (Analytics) | ✅ | ✅ | 100% |
| Vector Search (RAG) | ✅ | ✅ | 100% |
| UC Functions (Actions) | ✅ | ✅ | 100% |

**Result:** 80% code reuse across platforms!

---

## 🚀 Quick Start - Test Both!

### Prerequisites

```bash
cd /Users/pravin.varma/Documents/Demo/mcp-integration-blog
source venv/bin/activate

# Configure .env
cp .env.example .env
# Edit .env with your credentials
```

### Slack (10 minutes)

```bash
# 1. Create Slack app (see SLACK_LOCAL_TESTING.md)
# 2. Add tokens to .env
# 3. Start bot
python3 demos/02-slack/slack_bot.py

# 4. Open Slack and DM your bot!
```

### Teams (15 minutes)

```bash
# 1. Install Teams Toolkit in VS Code
# 2. Open demos/03-teams in VS Code
# 3. Start bot
python3 demos/03-teams/teams_bot.py

# 4. Press F5 in VS Code → Teams opens!
```

---

## 🎨 Features You'll See

### Slack Features

- 📱 **DMs and Channels** - Chat anywhere
- 💬 **Threading** - Conversations maintain context
- 🎨 **Rich Blocks** - Beautiful formatting
- 🏠 **App Home** - Custom welcome screen
- ⚡ **Real-time** - WebSocket connection

### Teams Features

- 📱 **Personal Chat** - 1-on-1 conversations
- 👥 **Team Channels** - Group discussions
- 🔔 **@Mentions** - Tag the bot
- 💬 **Typing Indicators** - Bot is thinking...
- 🎴 **Adaptive Cards** - Rich interactive UI

### Both Support

```
# Analytics
What was our Q4 revenue?

# Search
search how to create Genie space

# Functions
calculate 50000 Enterprise

# Help
/help
```

---

## 📊 Comparison

| Feature | Bot Emulator (Old) | Slack Socket Mode | Teams Toolkit |
|---------|-------------------|-------------------|---------------|
| **Interface** | Fake chat window | ✅ Real Slack | ✅ Real Teams |
| **Rich Cards** | Preview only | ✅ Full render | ✅ Full render |
| **Threading** | ❌ | ✅ | ✅ |
| **@Mentions** | ❌ | ✅ | ✅ |
| **Channels** | ❌ | ✅ | ✅ |
| **Setup** | 5 min | 10 min | 15 min |
| **Public URL** | Not needed | ❌ Not needed | ❌ Not needed |
| **Production** | ❌ Deprecated | ✅ Works | ✅ Recommended |

**Winner:** Real interfaces with local testing! 🏆

---

## 🐛 Debugging

Both support full debugging:

### Slack
```bash
# Add logging
import logging
logging.basicConfig(level=logging.DEBUG)

# Or use VS Code debugger
# Set breakpoint → F5 → Send Slack message
```

### Teams
```bash
# Teams Toolkit handles this!
# Set breakpoint in VS Code
# F5 → Send Teams message
# Debugger pauses at breakpoint
```

---

## 📚 Documentation

### Slack
- 📖 **Full Guide:** `demos/02-slack/SLACK_LOCAL_TESTING.md`
- 🔗 **Slack API:** https://api.slack.com/start
- 🔗 **Bolt Python:** https://slack.dev/bolt-python/

### Teams
- 📖 **Full Guide:** `demos/03-teams/TEAMS_TOOLKIT_SETUP.md`
- 🔗 **Teams Toolkit:** https://learn.microsoft.com/en-us/microsoftteams/platform/toolkit/
- 🔗 **Bot Framework:** https://dev.botframework.com/

---

## 🎯 Next Steps

1. **Choose your platform** (or do both!)
2. **Follow the setup guide**
3. **Start chatting** in real UI
4. **See M+N in action** - same client, different platforms!

### Deploy to Production

Both are production-ready:
- **Slack:** Deploy to Databricks Apps or any server
- **Teams:** One-click deploy with Teams Toolkit

---

## 💡 Pro Tips

### Slack Tips
- Use **Block Kit Builder** to design rich messages
- Test in **multiple channels** simultaneously
- Create **slash commands** for shortcuts
- Add **app shortcuts** to the ⚡ menu

### Teams Tips
- Design with **Adaptive Cards Designer**
- Test **personal**, **team**, and **group** chats
- Use **message extensions** for search
- Add **tabs** for embedded experiences

### Both
- Keep **console logs open** to see requests
- Use **mock mode** (`USE_MOCK_MCP=true`) to test without Databricks
- Test **conversation threading** with follow-ups
- Try **all 3 data sources** in each platform

---

**🎉 You're now testing in real production interfaces!**

No emulators, no compromises - just the actual user experience! 🚀

---

## 🔗 Quick Links

- [Slack Setup Guide](demos/02-slack/SLACK_LOCAL_TESTING.md)
- [Teams Setup Guide](demos/03-teams/TEAMS_TOOLKIT_SETUP.md)
- [Universal MCP Client](shared/mcp_client.py)
- [Project README](README.md)

**Questions?** Check the individual setup guides for troubleshooting and FAQs!
