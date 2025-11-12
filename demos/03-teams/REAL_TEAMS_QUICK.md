# Real Teams Deployment - Step by Step

## 🎯 You Want Real Teams (Not Emulator)

Perfect! Here's exactly what you need to do:

---

## 📋 Prerequisites Checklist

- [ ] Azure account (free): https://azure.microsoft.com/free/
- [ ] Microsoft Teams account (free)
- [ ] Your Genie Space ID ready
- [ ] ~30 minutes

---

## 🚀 Deployment Steps

### 1. Azure Account (5 min)

**Sign up:** https://azure.microsoft.com/free/

- Free tier includes everything you need
- $200 credit for 30 days
- No charges for free tier services

### 2. Create Azure Bot (5 min)

**In Azure Portal:**

1. **Create a resource** → Search "Azure Bot" → Create
2. **Basics:**
   - Bot handle: `genie-teams-bot-<yourname>` (must be unique globally)
   - Subscription: Your subscription
   - Resource group: Create new `mcp-bots`
   - Pricing: **F0 (Free)**
3. **Microsoft App ID:**
   - Click "Create new"
   - **COPY THE APP ID** - you'll need it!
4. **App Password:**
   - Click "Create new"
   - **COPY THE PASSWORD** - ⚠️ **You won't see it again!**
5. **Create**

**Save these immediately:**
- Microsoft App ID
- App Password

### 3. Create App Service (5 min)

1. **Create a resource** → Search "Web App" → Create
2. **Basics:**
   - Name: `genie-teams-app-<yourname>` (must be unique)
   - Runtime: **Python 3.11**
   - Operating System: **Linux**
   - Region: Choose closest
3. **App Service Plan:**
   - Create new
   - Name: `genie-teams-plan`
   - Pricing: **Free (F1)**
4. **Create**

**Note the URL:** `https://your-app-name.azurewebsites.net`

### 4. Deploy Bot Code (10 min)

**Option A: ZIP Deploy (Easiest)**

1. **Prepare ZIP:**
   ```bash
   cd demos/03-teams
   zip -r ../bot-deploy.zip . \
     -x "*.pyc" "__pycache__/*" "*.log" "*.md" \
     -x "test_*.py" "quick_start.py" "launch_playground.py"
   ```

2. **Upload:**
   - App Service → Deployment Center
   - Source: Local Git/ZIP
   - Upload `bot-deploy.zip`

3. **Set Environment Variables:**
   - App Service → Configuration → Application settings
   - Add:
     ```
     MICROSOFT_APP_ID=<your-app-id>
     MICROSOFT_APP_PASSWORD=<your-app-password>
     GENIE_SPACE_ID=<your-genie-space-id>
     DATABRICKS_PROFILE=DEFAULT
     ```
   - **Save**

4. **Restart App Service:**
   - Overview → Restart

**Option B: Azure CLI (Faster)**

```bash
# Install Azure CLI
brew install azure-cli

# Login
az login

# Run deployment script
python deploy_to_azure.py
```

### 5. Configure Azure Bot (3 min)

1. **Azure Bot → Configuration**
2. **Messaging endpoint:**
   ```
   https://your-app-name.azurewebsites.net/api/messages
   ```
3. **Save**

### 6. Enable Teams Channel (2 min)

1. **Azure Bot → Channels**
2. **Microsoft Teams → Apply**
3. **Bot is now registered with Teams!**

### 7. Add to Teams (2 min)

1. **Open Microsoft Teams**
2. **Apps** (left sidebar)
3. **Search:** Your bot name
4. **Add**
5. **Start chatting!**

---

## ✅ Verification

**Test in Teams:**
- `What was Q4 revenue?`
- `search MCP tutorial`
- `calculate 50000 Enterprise`
- `/help`

**All should work!** 🎉

---

## 🐛 Troubleshooting

### Bot Not Responding

1. Check App Service logs:
   - App Service → Log stream
   - Look for errors

2. Verify environment variables:
   - App Service → Configuration
   - Check all variables are set

3. Test endpoint:
   ```bash
   curl https://your-app.azurewebsites.net/
   ```
   Should return health check message

### Bot Not Appearing in Teams

1. Verify Teams channel enabled:
   - Azure Bot → Channels
   - Microsoft Teams should show "Enabled"

2. Wait a few minutes:
   - Bot registration can take 2-5 minutes

3. Search again:
   - Teams → Apps → Search bot name

---

## 💰 Cost

**Free Tier:**
- ✅ Azure Bot: Always free
- ✅ App Service: 10 apps free
- ✅ Teams: Free
- **Total: $0/month**

---

## 🎯 Quick Reference

**Azure Portal:** https://portal.azure.com  
**App Service URL:** `https://your-app-name.azurewebsites.net`  
**Messaging Endpoint:** `https://your-app-name.azurewebsites.net/api/messages`  
**Teams:** Apps → Search → Add

---

## 🚀 Ready?

1. ✅ Sign up for Azure
2. ✅ Follow steps above
3. ✅ Deploy to Azure
4. ✅ Add to Teams
5. ✅ Start chatting in real Teams!

**That's it!** You'll have real Teams integration! 🎉

