# Step 2: Configure OAuth & Permissions

Configure your Slack app's OAuth scopes and install it to get bot tokens.

## Step-by-Step Instructions

### 1. Navigate to OAuth & Permissions

In your Slack app settings:
1. Click **"OAuth & Permissions"** in the left sidebar
2. Scroll down to **"Scopes"** section

### 2. Configure Bot Token Scopes

Add these **Bot Token Scopes**:

**Required Scopes:**
- `app_mentions:read` - Listen for @mentions
- `chat:write` - Send messages
- `im:history` - Read direct message history
- `im:read` - View direct messages
- `im:write` - Send direct messages

**Optional (for rich features):**
- `channels:history` - Read channel messages (if needed)
- `users:read` - Get user information

**How to add:**
1. Scroll to **"Bot Token Scopes"**
2. Click **"Add New Scope"**
3. Type scope name and select from dropdown
4. Repeat for each scope

### 3. Install App to Workspace

1. Scroll to top of **"OAuth & Permissions"** page
2. Click **"Install to Workspace"** button
3. Review permissions (you'll see what the bot can do)
4. Click **"Allow"**

### 4. Copy Your Tokens

After installation, you'll see:

**Bot User OAuth Token:**
```
xoxb-YOUR-BOT-TOKEN-WILL-APPEAR-HERE
```

**Important:** This token starts with `xoxb-` and is your **Bot Token**

**Copy this token** - you'll need it for `.env` file!

### 5. Get App-Level Token (for Socket Mode)

1. Go to **"Basic Information"** in left sidebar
2. Scroll to **"App-Level Tokens"**
3. Click **"Generate Token and Scopes"**
4. Fill in:
   - **Token Name:** `Socket Mode Token`
   - **Scopes:** Select `connections:write`
5. Click **"Generate"**
6. **Copy the token** - starts with `xapp-`

**Important:** This is your **App Token** for Socket Mode

## Update Your .env File

Add these to your `.env` file:

```bash
# Slack Configuration
SLACK_BOT_TOKEN=xoxb-your-bot-token-here
SLACK_APP_TOKEN=xapp-your-app-token-here
```

**Example:**
```bash
SLACK_BOT_TOKEN=xoxb-YOUR-BOT-TOKEN-HERE
SLACK_APP_TOKEN=xapp-YOUR-APP-TOKEN-HERE
```

## Verify Installation

Your application should now:
- Be installed in your workspace
- Appear in "Installed apps" in workspace settings
- Have Bot Token (`xoxb-...`)
- Have App Token (`xapp-...`)

## Security Considerations

**Credential management best practices:**
- Never commit tokens to version control
- Add `.env` to `.gitignore` file
- Rotate tokens if compromised
- Use environment variables for production deployments

## Next Steps

- [Enable Socket Mode](03-enable-socket-mode.md) - Set up Socket Mode for local development

## Troubleshooting

### "Install to Workspace" button not visible

- Make sure you've added at least one Bot Token Scope
- Refresh the page
- Check you're the app owner

### Token not working

- Verify token starts with correct prefix (`xoxb-` for bot, `xapp-` for app)
- Check token hasn't expired
- Regenerate token if needed

### Missing scopes error

- Add required scopes listed above
- Reinstall app after adding scopes
- Check scope names are exact matches

