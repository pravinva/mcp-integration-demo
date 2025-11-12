# Deploy to Real Microsoft Teams - Fast Track

## 🎯 Goal: Real Teams Experience

To use **real Microsoft Teams** (not emulator), deploy to Azure. Here's the fastest way:

---

## ⚡ Quick Path (30 minutes)

### Step 1: Azure Account (5 min)

1. **Sign up:** https://azure.microsoft.com/free/
2. **Get $200 free credit** + free tier services
3. **No charges** for free tier

### Step 2: Create Azure Bot (5 min)

1. **Portal:** https://portal.azure.com
2. **Create → Search "Azure Bot" → Create**
3. **Settings:**
   - Bot handle: `genie-teams-bot-<yourname>` (must be unique)
   - Pricing: **F0 (Free)**
   - Microsoft App ID: **Create new** → **SAVE THE ID**
   - App Password: **Create new** → **SAVE THE PASSWORD** ⚠️
4. **Create**

**⚠️ IMPORTANT:** Save App ID and Password - you'll need them!

### Step 3: Create App Service (5 min)

1. **Portal → Create → "Web App"**
2. **Settings:**
   - Name: `genie-teams-bot-<yourname>` (must be unique)
   - Runtime: **Python 3.11**
   - Plan: **Free (F1)**
3. **Create**

### Step 4: Deploy Bot Code (10 min)

**Option A: ZIP Deploy (Easiest)**

1. **Prepare deployment package:**
   ```bash
   cd demos/03-teams
   zip -r bot-deploy.zip . -x "*.pyc" "__pycache__/*" "*.log"
   ```

2. **Upload to Azure:**
   - App Service → Deployment Center → Local Git/ZIP
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

**Option B: Git Deploy (If you have repo)**

1. **App Service → Deployment Center**
2. **Connect to GitHub/GitLab**
3. **Auto-deploy on push**

### Step 5: Configure Bot (3 min)

1. **Azure Bot → Configuration**
2. **Messaging endpoint:**
   ```
   https://your-app-name.azurewebsites.net/api/messages
   ```
3. **Save**

### Step 6: Enable Teams (2 min)

1. **Azure Bot → Channels**
2. **Microsoft Teams → Apply**
3. **Done!**

### Step 7: Add to Teams (2 min)

1. **Open Microsoft Teams**
2. **Apps → Search:** Your bot name
3. **Add**
4. **Chat!**

---

## 🚀 Automated Script (Coming Soon)

I can create a script that:
- Creates Azure resources
- Deploys your bot
- Configures everything
- Gets you Teams-ready in 15 minutes

Would you like me to create that?

---

## 📋 What You'll Need

**Before Starting:**
- ✅ Azure account (free)
- ✅ Microsoft Teams account
- ✅ Your Genie Space ID
- ✅ ~30 minutes

**During Setup:**
- ✅ Microsoft App ID (from Azure Bot)
- ✅ App Password (from Azure Bot)
- ✅ App Service URL (from deployment)

---

## 💰 Cost

**Free Tier:**
- Azure Bot: Always free
- App Service: 10 apps free
- Teams: Free
- **Total: $0/month**

---

## ✅ Success Checklist

- [ ] Azure account created
- [ ] Azure Bot created (App ID/Password saved)
- [ ] App Service created
- [ ] Bot code deployed
- [ ] Environment variables set
- [ ] Messaging endpoint configured
- [ ] Teams channel enabled
- [ ] Bot added to Teams
- [ ] Can chat in Teams!

---

## 🎯 Ready to Deploy?

**Follow:** `REAL_TEAMS_SETUP.md` for detailed steps

**Or tell me:** "Create deployment script" and I'll automate it! 🚀

---

## 💡 Pro Tips

1. **Use unique names** - Bot handle and app name must be globally unique
2. **Save credentials** - App Password shown only once
3. **Test locally first** - Make sure bot works before deploying
4. **Free tier is enough** - No need to upgrade for testing

**Let's get you on real Teams!** 🎉

