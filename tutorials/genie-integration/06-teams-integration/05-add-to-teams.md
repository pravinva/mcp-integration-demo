# Step 5: Add Bot to Teams

Add your deployed bot to Microsoft Teams for real users.

## Prerequisites

- Bot deployed to Azure
- Azure Bot resource configured
- Teams administrator access (for organization-wide deployment) or personal Teams access

## Step-by-Step Instructions

### Option 1: Add to Personal Teams (Easiest)

#### 1. Find Your Bot

1. Go to Azure Portal
2. Navigate to your Azure Bot resource
3. Click **"Test in Web Chat"**
4. Verify bot works

#### 2. Get Bot Direct Line Secret

1. In Azure Bot, go to **"Channels"**
2. Click **"Microsoft Teams"**
3. Click **"Edit"**
4. Note the **Bot ID** (same as Microsoft App ID)

#### 3. Add Bot to Teams

**Method A: Via Teams App**

1. Open Microsoft Teams
2. Click **"Apps"** (left sidebar)
3. Search for your bot by name
4. Click **"Add"**

**Method B: Via Direct Link**

1. In Azure Bot, go to **"Channels"** → **"Microsoft Teams"**
2. Click **"Open in Teams"**
3. Follow prompts to add bot

**Method C: Via Bot ID**

1. In Teams, click **"Chat"**
2. Click **"New chat"**
3. Search for bot by App ID
4. Start conversation

### Option 2: Add to Team/Channel (Organization)

#### 1. Create Teams App Manifest

Create `manifest.json`:

```json
{
  "$schema": "https://developer.microsoft.com/json-schemas/teams/v1.16/MicrosoftTeams.schema.json",
  "manifestVersion": "1.16",
  "id": "your-bot-app-id",
  "version": "1.0.0",
  "packageName": "com.yourcompany.geniebot",
  "developer": {
    "name": "Your Company",
    "websiteUrl": "https://yourcompany.com",
    "privacyUrl": "https://yourcompany.com/privacy",
    "termsOfUseUrl": "https://yourcompany.com/terms"
  },
  "name": {
    "short": "Genie Bot",
    "full": "Databricks Genie Bot"
  },
  "description": {
    "short": "AI-powered analytics assistant",
    "full": "Query Databricks Genie using natural language"
  },
  "icons": {
    "outline": "outline.png",
    "color": "color.png"
  },
  "accentColor": "#0078D4",
  "bots": [
    {
      "botId": "your-microsoft-app-id",
      "scopes": ["personal", "team", "groupchat"],
      "commandLists": [
        {
          "scopes": ["personal", "team", "groupchat"],
          "commands": [
            {
              "title": "help",
              "description": "Show help"
            }
          ]
        }
      ]
    }
  ],
  "permissions": ["identity", "messageTeamMembers"],
  "validDomains": []
}
```

#### 2. Create App Package

1. Create `manifest` folder
2. Add `manifest.json`
3. Add icons (192x192 PNG)
4. Zip folder: `manifest.zip`

#### 3. Upload to Teams

1. In Teams, go to **"Apps"**
2. Click **"Upload a custom app"** (bottom)
3. Select `manifest.zip`
4. Click **"Add"**

#### 4. Add to Team

1. Go to your team
2. Click **"..."** (more options)
3. Select **"Manage team"**
4. Go to **"Apps"** tab
5. Find your bot
6. Click **"Add"**

## Verify Bot Works

### Test in Personal Chat

1. Find bot in chat list
2. Send message: `What tables are available?`
3. Bot should respond

### Test in Channel

1. Go to any channel
2. @mention bot: `@Genie Bot what was revenue?`
3. Bot should respond

## Troubleshooting

### Bot Not Appearing

**Check:**
1. Bot is deployed and running
2. Azure Bot configuration is correct
3. Teams channel is enabled

**Solution:**
- Verify bot status in Azure
- Check Teams app is installed
- Try adding via App ID

### Bot Not Responding

**Check:**
1. Bot is running in Azure
2. Messaging endpoint is correct
3. Environment variables are set

**Solution:**
- Check App Service logs
- Verify bot configuration
- Test in Azure Web Chat first

### Permission Errors

**Check:**
1. Bot has correct scopes
2. User has permissions
3. Team settings allow bots

**Solution:**
- Check bot scopes in manifest
- Verify team settings
- Contact Teams admin

## Next Steps

- Review [Best Practices](../08-best-practices.md)
- Check [Troubleshooting](../07-troubleshooting.md)

## Summary

You have successfully:
- Built a Teams bot integrated with MCP
- Tested using Agents Playground (free tier)
- Deployed to Azure infrastructure
- Added the bot to Microsoft Teams

**The bot uses the same MCP client as Slack - demonstrating the M+N integration pattern!**

