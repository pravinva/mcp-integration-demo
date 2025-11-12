# Step 4: Production Deployment to Azure

Deploy your Teams bot to Azure for production use in real Teams.

## Prerequisites

- Bot tested locally with Agents Playground
- Azure subscription (free tier available)
- Azure CLI installed (optional for command-line deployment)

## Why Deploy to Azure?

- Real Microsoft Teams integration with production Teams app experience
- Production-grade hosting on scalable infrastructure
- Enterprise-level security, monitoring, and compliance features
- Enables team members to access the bot

## Step-by-Step Deployment

### Option 1: Azure App Service (Recommended)

#### 1. Create Azure Bot Resource

1. Go to **Azure Portal**: https://portal.azure.com
2. Click **"Create a resource"**
3. Search for **"Azure Bot"**
4. Click **"Create"**
5. Fill in:
   - **Subscription:** Your subscription
   - **Resource Group:** Create new or use existing
   - **Bot handle:** `genie-teams-bot` (must be globally unique)
   - **Pricing tier:** F0 (Free) or S1 (Standard)
   - **Microsoft App ID:** Leave empty (will create new)
6. Click **"Review + create"** then **"Create"**

#### 2. Get App ID and Password

After creation:
1. Go to your Azure Bot resource
2. Click **"Configuration"**
3. Note:
   - **Microsoft App ID**
   - Click **"Manage"** next to Microsoft App ID
4. In App Registration:
   - Go to **"Certificates & secrets"**
   - Click **"New client secret"**
   - Copy the **Value** (this is your password)
   - **Save it now** - you won't see it again!

#### 3. Create App Service

1. In Azure Portal, click **"Create a resource"**
2. Search for **"Web App"**
3. Click **"Create"**
4. Fill in:
   - **Subscription:** Same as bot
   - **Resource Group:** Same as bot
   - **Name:** `genie-teams-bot-app` (must be globally unique)
   - **Runtime stack:** Python 3.11
   - **Operating System:** Linux
   - **Region:** Choose closest
5. Click **"Review + create"** then **"Create"**

#### 4. Deploy Your Code

**Option A: Using Azure CLI**

```bash
# Install Azure CLI if needed
# https://docs.microsoft.com/cli/azure/install-azure-cli

# Login
az login

# Create deployment package
cd tutorials/genie-integration/06-teams-integration/code
zip -r deploy.zip . -x "*.pyc" "__pycache__/*"

# Deploy
az webapp deployment source config-zip \
  --resource-group <your-resource-group> \
  --name <your-app-service-name> \
  --src deploy.zip
```

**Option B: Using VS Code**

1. Install **Azure App Service** extension
2. Right-click project folder
3. Select **"Deploy to Web App"**
4. Follow prompts

**Option C: Using GitHub Actions**

Create `.github/workflows/deploy.yml`:

```yaml
name: Deploy to Azure

on:
  push:
    branches: [main]

jobs:
  deploy:
    runs-on: ubuntu-latest
    steps:
      - uses: actions/checkout@v2
      - name: Deploy to Azure
        uses: azure/webapps-deploy@v2
        with:
          app-name: <your-app-service-name>
          publish-profile: ${{ secrets.AZURE_WEBAPP_PUBLISH_PROFILE }}
```

#### 5. Configure Environment Variables

In Azure Portal:
1. Go to your App Service
2. Click **"Configuration"**
3. Click **"New application setting"**
4. Add:
   - `MICROSOFT_APP_ID` = Your App ID
   - `MICROSOFT_APP_PASSWORD` = Your App Password
   - `GENIE_SPACE_ID` = Your Genie Space ID
   - `DATABRICKS_HOST` = Your Databricks host
   - `DATABRICKS_TOKEN` = Your Databricks token
5. Click **"Save"**

#### 6. Configure Bot Messaging Endpoint

1. Go to your Azure Bot resource
2. Click **"Configuration"**
3. Set **Messaging endpoint:**
   ```
   https://<your-app-service-name>.azurewebsites.net/api/messages
   ```
4. Paste your **Microsoft App ID** and **Password**
5. Click **"Apply"**

### Option 2: Azure Functions (Alternative)

For serverless deployment:

1. Create **Function App** in Azure
2. Deploy bot code as HTTP trigger function
3. Configure same environment variables
4. Update bot messaging endpoint

## Verify Deployment

### 1. Check App Service Logs

In Azure Portal:
1. Go to App Service
2. Click **"Log stream"**
3. Look for bot startup messages

### 2. Test Health Endpoint

```bash
curl https://<your-app-service-name>.azurewebsites.net/
```

Should return: "Teams Bot is running!"

### 3. Test Bot Endpoint

```bash
curl -X POST https://<your-app-service-name>.azurewebsites.net/api/messages \
  -H "Content-Type: application/json" \
  -d '{"type":"message","text":"test"}'
```

Should return: 200 OK

## Troubleshooting

### Bot Not Responding

**Check:**
1. App Service is running
2. Environment variables are set
3. Messaging endpoint is correct
4. App ID/Password are correct

**Solution:**
- Check App Service logs
- Verify configuration
- Test locally first

### Deployment Fails

**Check:**
1. Code is valid Python
2. Dependencies in `requirements.txt`
3. Entry point is correct

**Solution:**
- Test locally first
- Check deployment logs
- Verify file structure

## Next Steps

- [Add to Teams](05-add-to-teams.md) - Add bot to real Teams workspace

