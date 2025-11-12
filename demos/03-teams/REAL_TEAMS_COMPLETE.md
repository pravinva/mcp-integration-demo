# 🚀 Deploy to Real Microsoft Teams - Complete Guide

## ✅ What You Need

1. **Azure Account** (free): https://azure.microsoft.com/free/
2. **Microsoft Teams** (free account works)
3. **Your Genie Space ID**
4. **~30 minutes**

---

## 📋 Step-by-Step (Follow in Order)

### Step 1: Azure Account (5 min)

1. Go to: https://azure.microsoft.com/free/
2. Sign up with Microsoft account
3. Verify (phone number may be required)
4. Get $200 free credit + free tier

**✅ Done when:** You can access https://portal.azure.com

---

### Step 2: Create Azure Bot (5 min)

1. **Go to:** https://portal.azure.com
2. **Click:** "Create a resource" (top left)
3. **Search:** "Azure Bot"
4. **Click:** "Create"

**Fill in:**
- **Bot handle:** `genie-teams-bot-<yourname>` (must be globally unique)
  - Example: `genie-teams-bot-pravin`
- **Subscription:** Your subscription
- **Resource group:** Create new → Name: `mcp-bots`
- **Pricing tier:** **F0 (Free)**
- **Microsoft App ID:** Click "Create new" → **COPY THE ID**
- **App Password:** Click "Create new" → **COPY THE PASSWORD** ⚠️

**⚠️ CRITICAL:** Save App ID and Password - you won't see the password again!

5. **Click:** "Review + create" → "Create"

**✅ Done when:** Azure Bot resource is created

---

### Step 3: Create App Service (5 min)

1. **Portal → Create a resource → Search "Web App" → Create**

**Basics tab:**
- **Name:** `genie-teams-app-<yourname>` (must be globally unique)
  - Example: `genie-teams-app-pravin`
- **Publish:** Code
- **Runtime stack:** Python 3.11
- **Operating System:** Linux
- **Region:** Choose closest (e.g., East US)

**App Service Plan:**
- **Create new**
- **Name:** `genie-teams-plan`
- **Pricing tier:** **Free (F1)**

2. **Click:** "Review + create" → "Create"

**✅ Done when:** App Service is created  
**📝 Note:** Your app URL will be `https://your-app-name.azurewebsites.net`

---

### Step 4: Prepare Deployment Package (2 min)

**Run this script:**

```bash
cd demos/03-teams
python prepare_deployment.py
```

This creates `bot-deploy.zip` in project root.

**✅ Done when:** `bot-deploy.zip` file exists

---

### Step 5: Deploy Code (5 min)

1. **Go to App Service** in Azure Portal
2. **Deployment Center** (left menu)
3. **Source:** Choose "Local Git" or "ZIP Deploy"
4. **If ZIP Deploy:**
   - Click "Browse"
   - Upload `bot-deploy.zip`
   - Click "Deploy"
5. **Wait for deployment** (2-3 minutes)

**✅ Done when:** Deployment shows "Success"

---

### Step 6: Set Environment Variables (3 min)

1. **App Service → Configuration** (left menu)
2. **Application settings** tab
3. **Click "+ New application setting"**
4. **Add these:**

```
Name: MICROSOFT_APP_ID
Value: <your-app-id-from-step-2>

Name: MICROSOFT_APP_PASSWORD
Value: <your-app-password-from-step-2>

Name: GENIE_SPACE_ID
Value: <your-genie-space-id>

Name: DATABRICKS_PROFILE
Value: DEFAULT
```

5. **Click "Save"**
6. **Restart App Service:**
   - Overview → Restart button

**✅ Done when:** All variables saved and app restarted

---

### Step 7: Configure Azure Bot (3 min)

1. **Go to Azure Bot resource**
2. **Configuration** (left menu)
3. **Messaging endpoint:**
   ```
   https://your-app-name.azurewebsites.net/api/messages
   ```
   Replace `your-app-name` with your actual app name
4. **Click "Apply"**

**✅ Done when:** Endpoint is saved

---

### Step 8: Enable Teams Channel (2 min)

1. **Azure Bot → Channels** (left menu)
2. **Click "Microsoft Teams"**
3. **Click "Apply"**
4. **Wait 1-2 minutes** for registration

**✅ Done when:** Teams channel shows "Enabled"

---

### Step 9: Add Bot to Teams (2 min)

1. **Open Microsoft Teams** (web or desktop)
2. **Click "Apps"** (left sidebar, bottom)
3. **Search:** Your bot name (e.g., "genie-teams-bot")
4. **Click on your bot**
5. **Click "Add"** or "Add to a team"
6. **Start chatting!**

**✅ Done when:** Bot appears in Teams and responds!

---

## 🎉 Success!

You now have:
- ✅ Bot running on Azure
- ✅ Connected to real Microsoft Teams
- ✅ All 3 data sources working (Genie, Vector Search, UC Functions)
- ✅ Real Teams experience!

---

## 💬 Test in Teams

Try these commands:
- `What was Q4 revenue?`
- `search MCP tutorial`
- `calculate 50000 Enterprise`
- `/help`

**All should work in real Teams!** 🚀

---

## 🐛 Troubleshooting

### Bot Not Responding

1. **Check App Service logs:**
   - App Service → Log stream
   - Look for Python errors

2. **Verify environment variables:**
   - App Service → Configuration
   - Check all 4 variables are set

3. **Test endpoint:**
   ```bash
   curl https://your-app-name.azurewebsites.net/
   ```
   Should return health check

### Bot Not in Teams

1. **Wait 2-5 minutes** - Registration takes time
2. **Verify Teams channel enabled:**
   - Azure Bot → Channels → Microsoft Teams should show "Enabled"
3. **Search again** in Teams Apps

### Deployment Failed

1. **Check ZIP file:**
   - Make sure `bot-deploy.zip` includes `teams_bot.py` and `shared/` folder
2. **Check logs:**
   - App Service → Deployment Center → Logs
3. **Try redeploy:**
   - Delete old deployment, upload again

---

## 💰 Cost

**Free Tier:**
- Azure Bot: Always free ✅
- App Service: 10 apps free ✅
- Teams: Free ✅
- **Total: $0/month** ✅

---

## 📚 Quick Reference

**Azure Portal:** https://portal.azure.com  
**App Service URL:** `https://your-app-name.azurewebsites.net`  
**Messaging Endpoint:** `https://your-app-name.azurewebsites.net/api/messages`  
**Teams:** Apps → Search → Add

---

## ✅ Checklist

- [ ] Azure account created
- [ ] Azure Bot created (App ID/Password saved)
- [ ] App Service created
- [ ] Deployment package created (`bot-deploy.zip`)
- [ ] Code deployed to Azure
- [ ] Environment variables set
- [ ] Messaging endpoint configured
- [ ] Teams channel enabled
- [ ] Bot added to Teams
- [ ] Can chat in Teams!

**Once all checked, you're done!** 🎉

---

## 🚀 Ready to Deploy?

1. **Sign up:** https://azure.microsoft.com/free/
2. **Follow steps above**
3. **Deploy to Azure**
4. **Add to Teams**
5. **Start chatting in real Teams!**

**That's the real Teams experience!** 🎉

