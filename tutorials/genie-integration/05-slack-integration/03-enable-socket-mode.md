# Step 3: Enable Socket Mode

Socket Mode allows your bot to receive events without a public URL. Perfect for local development!

## What is Socket Mode?

**Traditional approach:**
- Bot needs a public URL (e.g., `https://your-bot.com/slack/events`)
- Requires ngrok or similar tunneling service
- More complex setup

**Socket Mode:**
- Uses WebSocket connection
- No public URL needed
- Works behind firewalls
- Perfect for development and testing

## Step-by-Step Instructions

### 1. Navigate to Socket Mode

In your Slack app settings:
1. Click **"Socket Mode"** in the left sidebar
2. You'll see Socket Mode settings

### 2. Enable Socket Mode

1. Toggle **"Enable Socket Mode"** to **ON**
2. You'll see a confirmation message

### 3. Verify App-Level Token

Socket Mode requires an **App-Level Token** with `connections:write` scope.

**If you already created one:**
- Ready to use (from Step 2)

**If you need to create one:**
1. Go to **"Basic Information"** → **"App-Level Tokens"**
2. Click **"Generate Token and Scopes"**
3. Name: `Socket Mode Token`
4. Scope: `connections:write`
5. Generate and copy the token

### 4. Verify Token in .env

Make sure your `.env` has:

```bash
SLACK_APP_TOKEN=xapp-your-app-token-here
```

This token is used for Socket Mode connection.

## How Socket Mode Works

```
Your Bot (localhost)
    ↓
WebSocket Connection
    ↓
Slack Platform
    ↓
Events delivered to your bot
```

**Key advantages:**
- No ngrok or tunneling infrastructure required
- Works seamlessly on any network configuration
- Immediate connection establishment
- Ideal for development and testing environments

## Test Socket Mode Connection

Once you've implemented the bot (next step), you can test:

```bash
python slack_bot.py
```

You should see:
```
Starting Slack Genie Bot...
Configuration valid
Bot is running... Send a DM or @mention me in a channel!
```

## Next Steps

- [Implement Bot](04-implement-bot.md) - Write the bot code

## Troubleshooting

### "Socket Mode not available"

- Check you're on a paid Slack plan (Socket Mode requires paid plan)
- Or use Events API with ngrok for free plans

### Connection fails

- Verify `SLACK_APP_TOKEN` is correct
- Check token has `connections:write` scope
- Ensure Socket Mode is enabled in app settings

### Bot not receiving events

- Check bot is running
- Verify Bot Token is correct
- Check Event Subscriptions are configured (next step)

