# Teams Bot - Quick Start Guide

## 🚀 Fastest Way to Test Teams Bot

### Option 1: Quick Start Script (Recommended)

```bash
cd demos/03-teams
python quick_start.py
```

This script:
- ✅ Checks your configuration
- ✅ Verifies port is available
- ✅ Provides connection instructions
- ✅ Starts the bot

### Option 2: Direct Start

```bash
cd demos/03-teams
python test_teams_bot.py
```

---

## 📥 Download Bot Framework Emulator

**Before starting the bot**, download the emulator:

1. **Go to:** https://github.com/Microsoft/BotFramework-Emulator/releases
2. **Download** latest version for your OS
3. **Install** it

**Time:** ~2 minutes

---

## 🔌 Connect Emulator

Once bot is running:

1. **Open Bot Framework Emulator**
2. **Click "Open Bot"**
3. **Enter URL:** `http://localhost:3978/api/messages`
4. **Leave App ID/Password EMPTY** (for local testing)
5. **Click "Connect"**

**That's it!** Start chatting!

---

## 💬 Test Commands

Try these in the emulator:

```
What was Q4 revenue?
search MCP tutorial
calculate 50000 Enterprise
/help
/reset
```

---

## ✅ Success Checklist

- [ ] Bot Framework Emulator downloaded
- [ ] Bot running (`python quick_start.py`)
- [ ] Emulator connected
- [ ] Welcome message received
- [ ] Bot responds to questions

---

## 🐛 Quick Troubleshooting

**Bot won't start?**
- Check: `source venv/bin/activate`
- Check: `pip install -r requirements.txt`

**Can't connect?**
- Verify bot is running (check terminal)
- Verify URL: `http://localhost:3978/api/messages`
- Check port 3978 not blocked

**Bot not responding?**
- Check terminal for errors
- Verify `GENIE_SPACE_ID` in `.env`
- Or set `USE_MOCK_MCP=true`

---

## 📚 Full Guides

- **Detailed Setup**: `EMULATOR_SETUP.md`
- **Complete Guide**: `README.md`
- **Bot Code**: `teams_bot.py`

---

## 🎯 What Makes This Special?

The Teams bot uses the **same** `shared/mcp_client.py` as:
- ✅ CLI (`demos/01-cli/`)
- ✅ Claude Desktop (`demos/04-claude/`)
- ✅ Slack (`demos/02-slack/`)

**80% code reuse!** That's the M+N pattern! 🚀

---

**Ready?** Run `python quick_start.py` and follow the instructions!

