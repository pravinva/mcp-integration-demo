# 🚀 Quick Start: Teams Bot with Agents Playground

**Test your Teams bot with the same Genie space as Slack!**

## ✅ Already Configured!

Your Teams bot uses the **same `.env` file** as Slack, so it's already configured for:
- **Genie Space:** `01f0be3dcc771e60ada71b6ec9f61870` (ecommerce analytics)
- **Catalog/Schema:** `demo_retail.ecommerce`

## 🎯 Two Simple Steps

### Step 1: Start the Bot

```bash
cd demos/03-teams
python test_teams_bot.py
```

**Keep this terminal open!** You should see:
```
🚀 Starting Teams bot...
📍 Bot running on: http://localhost:3978/api/messages
```

### Step 2: Launch Agents Playground

**Open a NEW terminal** and run:

```bash
agentsplayground -e "http://localhost:3978/api/messages" -c "emulator"
```

**What happens:**
- ✅ Browser opens automatically
- ✅ You see Teams-like chat interface
- ✅ Bot is connected and ready!

## 🧪 Test It!

Try the same questions you use in Slack:
- `What was Q4 revenue?`
- `Show me top 5 customers`
- `What tables are available?`
- `Compare Q3 vs Q4 performance`

## ✨ What Makes This Special

**The Teams bot uses the EXACT same code as Slack:**
- ✅ Same `shared/mcp_client.py`
- ✅ Same Genie space (`01f0be3dcc771e60ada71b6ec9f61870`)
- ✅ Same MCP integration
- ✅ **80% code reuse!** That's the M+N pattern!

## 🐛 Troubleshooting

### "agentsplayground: command not found"
```bash
npm install -g @microsoft/m365agentsplayground
```

### Bot not responding
- Check bot terminal for errors
- Verify `.env` has `GENIE_SPACE_ID=01f0be3dcc771e60ada71b6ec9f61870`
- Make sure bot is still running

### Can't connect
- Verify URL: `http://localhost:3978/api/messages`
- Check port 3978 is not blocked
- Try restarting bot

## 📚 More Info

- Full tutorial: `../../tutorials/genie-integration/06-teams-integration/`
- Bot code: `teams_bot.py`
- MCP client: `../../shared/mcp_client.py`

