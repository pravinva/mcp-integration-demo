# Quick Test: Teams Bot with Agents Playground

Test your Teams bot with the same Genie space as Slack (`01f0be3dcc771e60ada71b6ec9f61870`).

## Prerequisites

✅ Same `.env` file as Slack bot (already configured!)
✅ Agents Playground installed: `npm install -g @microsoft/m365agentsplayground`

## Quick Start

### Step 1: Verify Configuration

Make sure your `.env` has:
```bash
GENIE_SPACE_ID=01f0be3dcc771e60ada71b6ec9f61870
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_TOKEN=your-token
```

### Step 2: Start the Bot

```bash
cd demos/03-teams
python test_teams_bot.py
```

You should see:
```
🚀 Starting Teams bot...
📍 Bot running on: http://localhost:3978/api/messages
```

**Keep this terminal open!**

### Step 3: Launch Agents Playground

In a **NEW terminal**:

```bash
agentsplayground -e "http://localhost:3978/api/messages" -c "emulator"
```

**What happens:**
- Browser opens automatically
- You see Teams-like chat interface
- Bot is connected!

### Step 4: Test!

Try these questions (same as Slack bot):
- `What was Q4 revenue?`
- `Show me top 5 customers`
- `What tables are available?`
- `Compare Q3 vs Q4 performance`

## Troubleshooting

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

## Success!

If bot responds to questions, you're all set! 🎉

The Teams bot uses the **same MCP client** as Slack - demonstrating the M+N pattern!

