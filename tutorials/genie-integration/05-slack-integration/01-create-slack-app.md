# Step 1: Create Slack App

This guide walks you through creating a Slack app from scratch.

## Prerequisites

- Admin access to a Slack workspace
- Ability to create applications at https://api.slack.com/apps

## Step-by-Step Instructions

### 1. Go to Slack API Portal

Navigate to: **https://api.slack.com/apps**

### 2. Create New App

1. Click **"Create New App"** button (top right)
2. Select **"From scratch"**
3. Fill in:
   - **App Name:** `Databricks Genie Bot` (or your choice)
   - **Pick a workspace:** Select your workspace
4. Click **"Create App"**

### 3. Note Your App Credentials

After creating, you'll see:
- **App ID:** (e.g., `A01234567`)
- **Client ID:** (e.g., `1234567890.1234567890123`)
- **Client Secret:** (e.g., `abc123def456...`) - **Keep this secret!**

**Don't close this page yet!** You'll need it for the next steps.

## What You've Created

You now have:
- A Slack application registered in your workspace
- Application credentials (App ID, Client ID, Client Secret)
- Configured application settings page

## Next Steps

- [Configure OAuth](02-configure-oauth.md) - Set up permissions and get tokens

## Troubleshooting

### "Create New App" button not visible

- Make sure you're logged into Slack
- Check you have admin access to a workspace
- Try a different browser or incognito mode

### Can't select workspace

- Verify you're an admin of at least one workspace
- Try refreshing the page
- Check workspace permissions

