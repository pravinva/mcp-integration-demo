# Deploy Teams Bot to Real Microsoft Teams

## 🎯 What You Need

### ✅ Required (Free Options Available)

1. **Microsoft Azure Account** (Free tier available)
   - Sign up: https://azure.microsoft.com/free/
   - Free tier includes: $200 credit for 30 days + always-free services
   - No credit card required for free tier

2. **Azure Bot Resource** (Free)
   - Part of Azure free tier
   - No cost for basic bot

3. **Azure Functions** (Free tier available)
   - Free tier: 1 million requests/month
   - Or use Azure App Service (also has free tier)

4. **Microsoft Teams Developer Account** (Free)
   - Use your existing Microsoft account
   - Or create free Teams account

### ❌ NOT Required

- ❌ Paid Azure subscription (free tier works)
- ❌ Credit card (for free tier)
- ❌ Teams license (free Teams works)
- ❌ Bot Framework Emulator (only for local testing)

---

## 🚀 Step-by-Step Deployment

### Step 1: Create Azure Account (Free)

1. **Go to:** https://azure.microsoft.com/free/
2. **Sign up** with Microsoft account
3. **Verify** (may require phone number)
4. **Get $200 free credit** for 30 days

**Time:** ~5 minutes

---

### Step 2: Create Azure Bot Resource

1. **Go to Azure Portal:** https://portal.azure.com
2. **Click "Create a resource"**
3. **Search:** "Azure Bot"
4. **Click "Create"**
5. **Fill in:**
   - **Bot handle:** `genie-teams-bot` (must be unique)
   - **Subscription:** Free tier
   - **Resource group:** Create new (e.g., `mcp-bots`)
   - **Pricing tier:** F0 (Free)
   - **Microsoft App ID:** Click "Create new" → Auto-generates
   - **App password:** Click "Create new" → **COPY THIS!** (you won't see it again)
6. **Click "Review + create"** → **Create**

**Save these:**
- Microsoft App ID
- App Password (from step above)

**Time:** ~5 minutes

---

### Step 3: Deploy Bot Code to Azure Functions

#### Option A: Azure Functions (Recommended)

1. **Install Azure Functions Core Tools:**
   ```bash
   brew install azure/functions/azure-functions-core-tools@4
   ```

2. **Create Function App:**
   ```bash
   cd demos/03-teams
   func init . --python
   func new --name teams_bot --template "HTTP trigger"
   ```

3. **Update code** to use Azure Functions format

4. **Deploy:**
   ```bash
   func azure functionapp publish <your-function-app-name>
   ```

#### Option B: Azure App Service (Simpler)

1. **Create App Service** in Azure Portal
2. **Deploy code** via Git or ZIP
3. **Set environment variables**
4. **Configure webhook**

**Time:** ~15-20 minutes

---

### Step 4: Configure Azure Bot

1. **Go to Azure Bot resource** in portal
2. **Settings → Configuration**
3. **Set Messaging endpoint:**
   ```
   https://your-function-app.azurewebsites.net/api/messages
   ```
4. **Save**

---

### Step 5: Register Bot with Teams

1. **In Azure Bot resource**
2. **Channels → Microsoft Teams**
3. **Click "Apply"**
4. **Bot is now registered with Teams!**

---

### Step 6: Add Bot to Teams

1. **Open Microsoft Teams**
2. **Apps → Search:** Your bot name
3. **Click "Add"**
4. **Start chatting!**

---

## 💰 Cost Breakdown

### Free Tier (What You Get)

| Service | Free Tier | Cost After |
|--------|-----------|------------|
| **Azure Bot** | Always free | Free |
| **Azure Functions** | 1M requests/month | $0.20 per million |
| **App Service** | 10 apps free | $13/month per app |
| **Teams** | Free | Free |

**Total Cost:** $0/month (free tier)

### If You Exceed Free Tier

- Azure Functions: ~$0.20 per million requests
- Very unlikely for testing/demo purposes

---

## 🔐 What You Need to Store

### Environment Variables (in Azure)

```bash
MICROSOFT_APP_ID=your-app-id-from-azure
MICROSOFT_APP_PASSWORD=your-app-password-from-azure
GENIE_SPACE_ID=your-genie-space-id
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
DATABRICKS_PROFILE=DEFAULT  # Or use OAuth
```

### Secrets Management

**Option 1: Azure Key Vault** (Free tier)
- Store secrets securely
- Free tier: 10,000 transactions/month

**Option 2: App Settings** (Simpler)
- Store in Function App settings
- Encrypted at rest

---

## 📋 Quick Checklist

### Before Deployment

- [ ] Azure account created
- [ ] Azure Bot resource created
- [ ] App ID and Password saved
- [ ] Bot code ready
- [ ] Environment variables prepared

### Deployment Steps

- [ ] Deploy bot code to Azure Functions/App Service
- [ ] Set environment variables
- [ ] Configure messaging endpoint
- [ ] Enable Teams channel
- [ ] Test in Teams

### After Deployment

- [ ] Bot appears in Teams
- [ ] Can send messages
- [ ] Bot responds correctly
- [ ] All 3 data sources work (Genie, Vector Search, UC Functions)

---

## 🆚 Emulator vs Real Teams

| Feature | Emulator | Real Teams |
|---------|----------|------------|
| **Setup** | Download app | Azure account |
| **Cost** | Free | Free (free tier) |
| **Time** | 2 minutes | 30 minutes |
| **Authentication** | Not needed | Azure Bot required |
| **Deployment** | Local only | Cloud (Azure) |
| **Use Case** | Testing | Production |

---

## 🎯 Recommended Approach

### For Testing/Demo:
✅ **Use Bot Framework Emulator** (what you have now)
- Free
- No Azure needed
- Works perfectly for demos
- Shows same functionality

### For Production:
✅ **Deploy to Azure**
- Free tier available
- Real Teams integration
- Production-ready
- Scalable

---

## 🚀 Quick Start: Real Teams

If you want to deploy now:

1. **Sign up for Azure:** https://azure.microsoft.com/free/ (5 min)
2. **Create Azure Bot:** Azure Portal → Create Bot (5 min)
3. **Deploy code:** Azure Functions or App Service (15 min)
4. **Configure:** Set endpoint and enable Teams (5 min)
5. **Test:** Add bot to Teams and chat!

**Total time:** ~30 minutes

---

## 💡 Pro Tips

1. **Start with Emulator** - Test everything locally first
2. **Use Free Tier** - No cost for testing
3. **Save Credentials** - App ID/Password are critical
4. **Test Locally** - Verify bot works before deploying
5. **Monitor Usage** - Azure Portal shows free tier usage

---

## 📚 Resources

- **Azure Free Account:** https://azure.microsoft.com/free/
- **Azure Bot Docs:** https://docs.microsoft.com/azure/bot-service/
- **Teams Bot Docs:** https://docs.microsoft.com/microsoftteams/platform/bots/how-to/authentication/auth-flow-bot
- **Azure Functions:** https://docs.microsoft.com/azure/azure-functions/

---

## ✅ Summary

**Do you need Azure?**
- ✅ **Yes** - For real Teams deployment
- ✅ **Free tier available** - No cost for testing
- ✅ **No credit card** - Required for free tier signup (but won't be charged)

**For now:**
- ✅ **Emulator works perfectly** - No Azure needed
- ✅ **Same functionality** - Shows all features
- ✅ **Great for demos** - Professional presentation

**When ready for production:**
- ✅ **Deploy to Azure** - Free tier is enough
- ✅ **Real Teams** - Full integration
- ✅ **Scalable** - Can upgrade later

**Bottom line:** You can test everything with the Emulator (free, no Azure). When ready for production Teams, Azure free tier is sufficient! 🚀

