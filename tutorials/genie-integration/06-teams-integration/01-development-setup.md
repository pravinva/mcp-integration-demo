# Step 1: Development Setup with Agents Playground

Set up Microsoft 365 Agents Playground for FREE local development and testing.

## What is Agents Playground?

**Microsoft 365 Agents Playground** provides a free local testing environment with a Teams-like interface. Key features:
- Development and testing without cloud deployment
- No Azure subscription required
- No Teams application registration required
- Real Teams-like user interface experience

## Prerequisites

- Node.js 18.x or higher installed
- Python environment configured
- Microsoft account (personal or organizational)

## Step-by-Step Setup

### 1. Install Node.js

**If not already installed:**
- Download from: https://nodejs.org/
- Select LTS version (18.x or higher)
- Follow the installation wizard

**Verify installation:**
```bash
node --version
npm --version
```

Should display version 18.x or higher.

### 2. Install Agents Playground

```bash
npm install -g @microsoft/m365agentsplayground
```

**Verify installation:**
```bash
agentsplayground --version
```

### 3. Prepare Your Bot Code

Ensure you have:
- Bot code ready (created in the next step)
- `.env` file configured
- MCP client set up

### 4. Start Your Bot

In one terminal:

```bash
cd tutorials/genie-integration/06-teams-integration/code
python teams_bot.py
```

You should see:
```
============================================================
Teams Bot Running
============================================================
Listening on: http://localhost:3978/api/messages

To test:
1. Open Agents Playground
2. Connect to: http://localhost:3978/api/messages
3. Start chatting!

Press Ctrl+C to stop
============================================================
```

**Keep this terminal open!** The bot needs to keep running.

### 5. Launch Agents Playground

In another terminal:

```bash
agentsplayground -e "http://localhost:3978/api/messages" -c "emulator"
```

**What happens:**
- Browser opens automatically
- You see Teams-like interface
- Bot is connected and ready!

### 6. Test Your Bot

In the Agents Playground:
1. Type: `What tables are available?`
2. Bot should respond!
3. Try more questions

## What You'll See

### Agents Playground Interface

- **Left sidebar:** Chat interface (like Teams)
- **Main area:** Conversation with bot
- **Input box:** Type messages here

### Bot Responses

- Formatted messages
- Typing indicators
- Error messages (if any)

## Advantages of Agents Playground

### vs Bot Framework Emulator

| Feature | Agents Playground | Bot Framework Emulator |
|---------|------------------|----------------------|
| **UI** | Teams-like in browser | Generic chat UI |
| **Cost** | FREE | FREE |
| **Setup** | Simple npm install | Download app |
| **Future** | Active development | Deprecated (2025) |

### vs Real Teams

| Feature | Agents Playground | Real Teams |
|---------|------------------|------------|
| **Cost** | FREE | Requires Azure |
| **Setup Time** | 5 minutes | 30+ minutes |
| **Registration** | Not needed | Required |
| **UI** | Teams-like | Real Teams |
| **Use Case** | Development | Production |

## Troubleshooting

### "agentsplayground: command not found"

**Solution:**
```bash
# Reinstall globally
npm uninstall -g @microsoft/m365agentsplayground
npm install -g @microsoft/m365agentsplayground

# Or use npx
npx @microsoft/m365agentsplayground -e "http://localhost:3978/api/messages"
```

### "Cannot connect to bot"

**Check:**
1. Bot is running (check terminal)
2. URL is correct: `http://localhost:3978/api/messages`
3. Port 3978 is not blocked
4. No firewall blocking localhost

**Solution:**
- Verify bot terminal shows "Listening on: http://localhost:3978/api/messages"
- Try restarting bot
- Check no other app using port 3978

### Browser doesn't open

**Solution:**
- Manually open browser
- Go to: `http://localhost:3978` (or check terminal for URL)
- Or use: `agentsplayground -e "http://localhost:3978/api/messages" --open`

### Bot not responding

**Check:**
1. Bot terminal shows no errors
2. `.env` file has `GENIE_SPACE_ID`
3. MCP connection works (test separately)

**Solution:**
- Check bot logs in terminal
- Verify Genie Space ID is correct
- Test MCP connection directly

## Next Steps

- [Implement Bot](02-implement-bot.md) - Write the bot code
- [Test with Playground](03-test-with-playground.md) - Comprehensive testing

