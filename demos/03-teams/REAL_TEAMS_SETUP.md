# Deploy Teams Bot to Real Microsoft Teams

## 🎯 Goal: Test with Real Teams (Not Emulator)

To use **real Microsoft Teams**, you need to deploy to Azure. Here's the fastest path:

---

## ⚡ Quick Setup (30 minutes)

### Step 1: Azure Account (5 min)

1. **Sign up:** https://azure.microsoft.com/free/
2. **Get $200 free credit** for 30 days
3. **No charges** for free tier services

### Step 2: Create Azure Bot (5 min)

1. **Go to:** https://portal.azure.com
2. **Create → Search "Azure Bot" → Create**
3. **Fill in:**
   - Bot handle: `genie-teams-bot` (must be unique)
   - Pricing: **F0 (Free)**
   - Microsoft App ID: **Create new** → **COPY THE ID**
   - App Password: **Create new** → **COPY THE PASSWORD** (you won't see it again!)
4. **Create**

**Save these:**
- Microsoft App ID
- App Password

### Step 3: Deploy Bot Code (15 min)

**Option A: Azure App Service (Easiest)**

1. **Create App Service:**
   - Portal → Create → "Web App"
   - Runtime: Python 3.11
   - Plan: Free (F1)

2. **Deploy Code:**
   - Go to App Service → Deployment Center
   - Choose: Local Git or ZIP deploy
   - Upload your bot code

3. **Set Environment Variables:**
   - App Service → Configuration → Application settings
   - Add:
     ```
     MICROSOFT_APP_ID=your-app-id
     MICROSOFT_APP_PASSWORD=your-app-password
     GENIE_SPACE_ID=your-space-id
     DATABRICKS_PROFILE=DEFAULT
     ```

4. **Get URL:**
   - App Service → Overview → URL
   - Example: `https://your-app.azurewebsites.net`

### Step 4: Configure Azure Bot (5 min)

1. **Go to Azure Bot resource**
2. **Configuration → Messaging endpoint:**
   ```
   https://your-app.azurewebsites.net/api/messages
   ```
3. **Save**

### Step 5: Enable Teams Channel (2 min)

1. **Azure Bot → Channels**
2. **Microsoft Teams → Apply**
3. **Done!**

### Step 6: Add to Teams (2 min)

1. **Open Microsoft Teams**
2. **Apps → Search:** Your bot name
3. **Add**
4. **Start chatting!**

---

## 🚀 Automated Deployment Script

I can create a deployment script that:
- Creates Azure resources
- Deploys your bot
- Configures everything
- Gets you a Teams-ready bot

Would you like me to create that?

---

## 💰 Cost

**Free Tier Includes:**
- ✅ Azure Bot: Always free
- ✅ App Service: 10 apps free
- ✅ $200 credit for 30 days

**Total Cost:** $0/month (free tier)

---

## 📋 What You Need

1. ✅ Azure account (free)
2. ✅ Microsoft Teams account (free)
3. ✅ Your bot code (ready!)
4. ✅ 30 minutes

---

## 🎯 Next Steps

**Option 1: Manual Setup** (follow steps above)

**Option 2: I can create deployment scripts** to automate it

**Option 3: Use Azure CLI** for faster setup

Which do you prefer? I can help with any of these! 🚀

