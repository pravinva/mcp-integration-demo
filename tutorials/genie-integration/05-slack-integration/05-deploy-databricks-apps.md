# Step 5: Deploy to Databricks Apps

Deploy your Slack bot to Databricks Apps for production hosting.

## Why Databricks Apps?

- No Azure subscription required
- Integrated with Databricks workspace
- Automatic scaling and resource management
- Built-in security and access controls
- Simplified deployment process

## Prerequisites

- Databricks workspace with Applications feature enabled
- Workspace administrator permissions (required for initial deployment)
- Bot code tested locally

## Step-by-Step Deployment

### 1. Prepare Deployment Package

Create `app.yaml` in your project root:

```yaml
name: genie-slack-bot
description: Slack bot for Databricks Genie via MCP
version: 1.0.0

resources:
  - type: compute
    name: default
    compute_type: serverless

runtime:
  type: python
  version: "3.11"

entrypoint:
  file: demos/02-slack/slack_bot.py

environment:
  variables:
    - name: SLACK_BOT_TOKEN
      required: true
    - name: SLACK_APP_TOKEN
      required: true
    - name: GENIE_SPACE_ID
      required: true
    - name: DATABRICKS_HOST
      required: true
    - name: DATABRICKS_TOKEN
      required: true
```

### 2. Create Deployment Package

Package your code:

```bash
# Create deployment directory
mkdir -p deploy
cp -r demos/02-slack deploy/
cp -r shared deploy/
cp requirements.txt deploy/
cp app.yaml deploy/

# Create zip file
cd deploy
zip -r ../bot-deploy.zip .
cd ..
```

### 3. Deploy via Databricks CLI

```bash
# Install Databricks CLI if needed
pip install databricks-cli

# Configure CLI
databricks configure --token

# Deploy app
databricks apps deploy \
  --app-name genie-slack-bot \
  --app-package bot-deploy.zip \
  --app-version 1.0.0
```

### 4. Configure Environment Variables

In Databricks Apps UI:

1. Go to **Apps** → Your app
2. Click **"Configuration"**
3. Add environment variables:
   - `SLACK_BOT_TOKEN`
   - `SLACK_APP_TOKEN`
   - `GENIE_SPACE_ID`
   - `DATABRICKS_HOST`
   - `DATABRICKS_TOKEN`
4. Save

### 5. Start the App

1. Go to **Apps** → Your app
2. Click **"Start"**
3. Monitor logs for startup

## Alternative: Deploy via UI

### 1. Create App in Databricks

1. Go to **Apps** in Databricks workspace
2. Click **"Create App"**
3. Fill in:
   - **Name:** `genie-slack-bot`
   - **Description:** `Slack bot for Genie`
   - **Runtime:** Python 3.11
4. Upload `bot-deploy.zip`
5. Click **"Create"**

### 2. Configure Environment

1. Go to app settings
2. Add environment variables (same as above)
3. Save

### 3. Deploy and Start

1. Click **"Deploy"**
2. Wait for deployment
3. Click **"Start"**

## Verify Deployment

### Check Logs

In Databricks Apps UI:
1. Go to your application
2. Click **"Logs"**
3. Look for:
   ```
   Starting Slack Genie Bot...
   Configuration valid
   Bot is running...
   ```

### Test Bot

1. Send DM to bot in Slack
2. Bot should respond
3. Check logs for any errors

## Monitoring

### View Logs

```bash
databricks apps logs --app-name genie-slack-bot --tail
```

### Check Status

```bash
databricks apps status --app-name genie-slack-bot
```

## Troubleshooting

### App Won't Start

- Check logs for errors
- Verify environment variables are set
- Check Databricks token is valid
- Verify Slack tokens are correct

### Bot Not Responding

- Check app is running (status should be "Running")
- Check logs for errors
- Verify Slack app is installed in workspace
- Test tokens locally first

### Deployment Fails

- Check `app.yaml` syntax
- Verify all files are in zip
- Check workspace has Apps enabled
- Verify permissions

## Next Steps

- [Testing](06-testing.md) - Comprehensive testing guide

