# Quick Start Guide - Testing with ~/.databrickscfg

The fastest way to test the MCP showcase is using your existing Databricks CLI configuration.

## Option 1: Using Existing ~/.databrickscfg (Recommended)

If you already use Databricks CLI, you're ready to go!

### Step 1: Verify Your Configuration

Check if ~/.databrickscfg exists
cat ~/.databrickscfg

Should look like:
[DEFAULT]
host = https://your-workspace.cloud.databricks.com
token = dapi...

Clone the project
git clone <your-repo-url>
cd databricks-mcp-showcase

Create virtual environment
python -m venv venv
source venv/bin/activate # Windows: venv\Scripts\activate

Install dependencies
pip install -r requirements.txt


### Step 3: Configure Genie Space ID

Create a minimal `.env` file:

.env
GENIE_SPACE_ID=your-genie-space-id-here

Optional: If not using DEFAULT profile
DATABRICKS_PROFILE=myprofile


**To find your Genie Space ID:**
1. Go to Databricks SQL → Genie
2. Open your Genie Space
3. Look at the URL: `/sql/genie/{space_id}`
4. Copy the space_id

### Step 4: Test with CLI


cd demos/01-cli
python genie_cli.py

You should see:
🔑 Using Databricks CLI profile: DEFAULT
📁 Reading from: ~/.databrickscfg
✅ Connected as: your.email@company.com
📍 Workspace: https://your-workspace.cloud.databricks.com
✅ Configuration valid


### Step 5: Ask Your First Question

🧑 You: What was our revenue in Q4 2024?

🤔 Thinking...

🧞 Genie:
[Response with data and SQL query]


**It works! 🎉**

---

## Option 2: First-Time Setup (No existing ~/.databrickscfg)

If you don't have Databricks CLI configured:

### Step 1: Install Databricks CLI

pip install databricks-cli


### Step 2: Configure Authentication

databricks configure --token

You'll be prompted for:
Databricks Host: https://your-workspace.cloud.databricks.com
Token: dapi... (create at User Settings → Access Tokens)


This creates `~/.databrickscfg` automatically.

### Step 3: Follow Option 1 Steps 2-5

---

## Testing the Full Demo (All 3 Data Sources)

Once CLI works, test with all data sources:



cd demos/01-cli
python genie_cli_full.py

Try the demo command:
🧑 You: /demo

This will query:
1️⃣ Genie (analytics)
2️⃣ Vector Search (documentation)
3️⃣ UC Functions (calculations)
All using the SAME MCP client!


---

## What's Happening Behind the Scenes

When you run the CLI:


config.py reads your ~/.databrickscfg
client = WorkspaceClient(profile="DEFAULT")

Automatically gets:
- host from ~/.databrickscfg
- token from ~/.databrickscfg
- No need for .env variables!
MCP client uses this authenticated client
mcp_client = UniversalMCPClient(client)

Query any data source
response = await mcp_client.ask_genie(space_id, "What was revenue?")



---

## Troubleshooting

### Error: "Failed to connect using profile 'DEFAULT'"

**Solution 1:** Check your ~/.databrickscfg exists

ls -la ~/.databrickscfg
cat ~/.databrickscfg



### Error: "GENIE_SPACE_ID not set"

Create `.env` file:
echo "GENIE_SPACE_ID=your-space-id" > .env


### Error: "Permission denied" when querying

Check Genie Space permissions:
1. Go to your Genie Space in Databricks
2. Settings → Permissions
3. Make sure your user has "Can Use" or "Can Manage"

### Want to use Mock Mode (no Databricks)?

.env
USE_MOCK_MCP=true
GENIE_SPACE_ID=mock-space-id


Now runs with fake data - great for development!

---

## Next Steps

Once CLI works:

1. ✅ **Test Slack bot locally** (needs Slack tokens)

cd demos/02-slack
python slack_bot.py


3. ✅ **Configure Claude Desktop** (copy config.json)

4. ✅ **Deploy Slack to Databricks Apps** (production)

---

## Configuration Priority

The code checks authentication in this order:

1. **OAuth credentials** (if `DATABRICKS_OAUTH_CLIENT_ID` set in .env)
2. **~/.databrickscfg profile** (if no OAuth, uses this - easiest!)
3. **Explicit token** (if `DATABRICKS_TOKEN` in .env)
4. **Mock mode** (if `USE_MOCK_MCP=true`)

For CLI testing, option 2 (~/.databrickscfg) is perfect!

---

## Summary: Fastest Path to Testing

1. Verify Databricks CLI works
databricks workspace list

2. Clone repo
git clone <repo>
cd databricks-mcp-showcase

3. Setup Python
python -m venv venv
source venv/bin/activate
pip install -r requirements.txt

4. Add Genie Space ID
echo "GENIE_SPACE_ID=your-space-id" > .env

5. Test!
cd demos/01-cli
python genie_cli.py

6. Try full demo
python genie_cli_full.py

Type: /demo


**That's it! No complex OAuth setup, no Azure, just your existing Databricks credentials.**


