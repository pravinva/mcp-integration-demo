# Agents Playground Node.js 25 Compatibility Issue

## Problem

Agents Playground has a compatibility issue with Node.js 25:
```
TypeError: Cannot read properties of undefined (reading 'prototype')
```

## Solutions

### Option 1: Use Node.js 18 or 20 (Recommended)

Install and use an older Node.js version:

```bash
# Install nvm if you don't have it
curl -o- https://raw.githubusercontent.com/nvm-sh/nvm/v0.39.0/install.sh | bash

# Install Node.js 20 (LTS)
nvm install 20
nvm use 20

# Verify version
node --version  # Should show v20.x.x

# Now try Agents Playground again
agentsplayground -e "http://localhost:3978/api/messages" -c "emulator"
```

### Option 2: Use Bot Framework Emulator (Alternative)

Download Bot Framework Emulator:
- Mac: https://github.com/Microsoft/BotFramework-Emulator/releases
- Download the latest `.dmg` file
- Install and run
- Connect to: `http://localhost:3978/api/messages`
- Leave App ID/Password empty for local testing

### Option 3: Deploy to Azure and Test in Real Teams

Deploy your bot to Azure and test in actual Microsoft Teams:
- See: `04-production-deployment.md`
- This gives you the real Teams experience!

### Option 4: Wait for Agents Playground Update

Microsoft will likely fix this in a future update. Check:
- https://www.npmjs.com/package/@microsoft/m365agentsplayground
- For updates and compatibility fixes

## Current Status

✅ **Bot is running** on `http://localhost:3978/api/messages`
❌ **Agents Playground** has Node.js 25 compatibility issue

## Quick Test Without UI

You can verify the bot is working by checking the health endpoint:

```bash
curl http://localhost:3978/api/messages
```

Should return: "Teams Bot is running!"

## Recommendation

**For now:** Use **Option 1** (Node.js 20) to get Agents Playground working, or deploy to Azure for real Teams testing.

