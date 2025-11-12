# Teams Toolkit Setup - Teams-like Interface

Get a **real Teams interface** for local testing using Teams Toolkit!

## Prerequisites

1. **Visual Studio Code** with Teams Toolkit extension
2. **Microsoft 365 Account** (free developer account works)
3. **Node.js** 16+ installed

## Step 1: Install Teams Toolkit Extension

1. Open VS Code
2. Go to Extensions (Cmd+Shift+X)
3. Search for "Teams Toolkit"
4. Install **Teams Toolkit** by Microsoft

## Step 2: Sign In to Microsoft 365

1. In VS Code, click **Teams Toolkit** icon in sidebar
2. Click **Sign in to Microsoft 365**
3. Sign in with your Microsoft 365 account
4. Accept permissions

You can use a free developer account:
- Sign up at: https://developer.microsoft.com/en-us/microsoft-365/dev-program

## Step 3: Configure Environment

Open this project in VS Code:

```bash
cd /Users/pravin.varma/Documents/Demo/mcp-integration-blog/demos/03-teams
code .
```

The project already has:
- ✅ `teamsapp.yml` - Teams Toolkit configuration
- ✅ `appPackage/manifest.json` - Teams app manifest
- ✅ `appPackage/color.png` - App icon (192x192)
- ✅ `appPackage/outline.png` - Sidebar icon (32x32)
- ✅ `teams_bot.py` - Bot implementation

## Step 4: Configure Databricks Credentials

Edit `../../.env` (project root):

```bash
# Databricks Configuration
DATABRICKS_HOST=https://your-workspace.databricks.com
DATABRICKS_TOKEN=your-pat-token

# Or use ~/.databrickscfg
DATABRICKS_PROFILE=DEFAULT

# Data Source IDs
GENIE_SPACE_ID=your-genie-space-id
VECTOR_SEARCH_INDEX_ID=catalog.schema.index_name
UC_FUNCTION_NAME=catalog.schema.calculate_discount
```

## Step 5: Start Bot Server

In terminal:

```bash
cd /Users/pravin.varma/Documents/Demo/mcp-integration-blog
source venv/bin/activate
python3 demos/03-teams/teams_bot.py
```

You should see:
```
============================================================
🤖 Teams Bot Running
============================================================
📍 Listening on: http://localhost:3978/api/messages
```

**Keep this terminal running!**

## Step 6: Provision and Deploy with Teams Toolkit

In VS Code with Teams Toolkit:

1. **Open Teams Toolkit** (left sidebar icon)
2. **DEVELOPMENT** section → Click **Provision**
   - This creates the Teams app and bot registration
   - Bot ID and password will be auto-generated
3. **DEVELOPMENT** section → Click **Deploy**
   - This prepares the app package
4. **DEVELOPMENT** section → Click **Preview Your Teams App (F5)**
   - Select **Debug in Teams (Edge)** or **Debug in Teams (Chrome)**

This will:
- ✅ Create app registration in your Microsoft 365 tenant
- ✅ Generate bot credentials automatically
- ✅ Package the app
- ✅ Open Teams in browser with your bot installed!

## Step 7: Chat in Real Teams Interface!

Teams will open in browser showing your bot:

1. **Personal chat** will auto-open
2. Try these commands:
   ```
   What was our Q4 revenue?

   search how to create Genie space

   calculate 50000 Enterprise

   /help
   ```

3. You can also:
   - Add bot to a team channel
   - @mention the bot in group chats
   - See typing indicators and rich formatting

## Teams Toolkit Features

### Hot Reload
Edit `teams_bot.py` and restart the Python server. Refresh Teams to see changes.

### Debug
- Set breakpoints in VS Code
- Click F5 to debug
- Messages will hit your breakpoints!

### App Package
The packaged app is at:
```
appPackage/build/appPackage.local.zip
```

You can manually upload this to Teams:
1. Teams → Apps → Manage your apps
2. Upload an app → Upload a custom app
3. Select the .zip file

## Troubleshooting

### "Bot ID not set"
The bot credentials are in `env/.env.local` after provisioning:
```bash
BOT_ID=<generated-by-teams-toolkit>
BOT_PASSWORD=<generated-by-teams-toolkit>
```

Update `shared/config.py` to read from this file if needed.

### "Cannot connect to bot"
1. Check Python server is running on port 3978
2. Check firewall allows localhost:3978
3. Try restarting the bot server

### "App not appearing"
1. Click **Provision** again in Teams Toolkit
2. Make sure you're signed into Microsoft 365
3. Check the **OUTPUT** tab in VS Code for errors

## Comparison: Emulator vs Teams Toolkit

| Feature | Bot Framework Emulator | Teams Toolkit |
|---------|------------------------|---------------|
| Interface | Basic chat window | **Real Teams UI** ✅ |
| Rich Cards | Preview only | Full rendering ✅ |
| @mentions | Not supported | Works ✅ |
| Channels | Not supported | Works ✅ |
| Setup | Simple | Requires M365 account |
| Status | Deprecated | **Recommended** ✅ |

## Next Steps

### Deploy to Production

Once you're happy with local testing:

1. **LIFECYCLE** → **Provision in Cloud**
2. **LIFECYCLE** → **Deploy to Cloud**
3. **LIFECYCLE** → **Publish to App Catalog**

This deploys to Azure and makes the bot available to your organization!

### Test All Features

Our bot supports:
- ✅ **Genie Analytics**: Natural language data queries
- ✅ **Vector Search**: Documentation search
- ✅ **UC Functions**: Business calculations
- ✅ **Conversation context**: Follow-up questions
- ✅ **Rich formatting**: Cards and buttons
- ✅ **Help commands**: `/help`, `/reset`

## Resources

- Teams Toolkit Docs: https://learn.microsoft.com/en-us/microsoftteams/platform/toolkit/teams-toolkit-fundamentals
- Bot Framework: https://dev.botframework.com/
- Teams App Design: https://learn.microsoft.com/en-us/microsoftteams/platform/concepts/design/design-teams-app-overview

---

**🎉 You now have a real Teams interface for local testing!**

No emulator needed - you're chatting in actual Microsoft Teams! 🚀
