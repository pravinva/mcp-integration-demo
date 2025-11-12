# Setup Guide - Databricks MCP Universal Client

This guide provides step-by-step instructions for setting up and running all four demo applications.

## Table of Contents

1. [Prerequisites](#prerequisites)
2. [Databricks Workspace Configuration](#databricks-workspace-configuration)
3. [Local Environment Setup](#local-environment-setup)
4. [Data Source Setup](#data-source-setup)
5. [Running the Demos](#running-the-demos)
6. [Troubleshooting](#troubleshooting)
7. [Production Deployment](#production-deployment)

## Prerequisites

### Required Tools

- **Python 3.9+** (3.10 or 3.11 recommended)
- **Databricks CLI** (for authentication)
- **Git** (to clone repository)
- **Virtual environment tool** (venv or conda)

### Verify Installations

```bash
# Check Python version
python3 --version
# Should show: Python 3.9.x or higher

# Check pip
pip3 --version

# Install Databricks CLI
pip install databricks-cli

# Verify installation
databricks --version
```

### Databricks Workspace Requirements

You need access to a Databricks workspace with:

1. **Unity Catalog enabled**
2. **SQL Warehouse** (any size works for demos)
3. **Cluster** (optional, for production Vector Search setup)
4. **Permissions:**
   - CREATE CATALOG (or use existing catalog)
   - CREATE SCHEMA (or use existing schema)
   - CREATE FUNCTION (for UC Functions demo)
   - USE CATALOG and USE SCHEMA
   - Vector Search endpoint access (if available)

## Databricks Workspace Configuration

### Step 1: Configure Databricks CLI Authentication

**Option A: Token Authentication (Recommended for demos)**

```bash
# Configure Databricks CLI
databricks configure --token

# Enter when prompted:
# Host: https://your-workspace.databricks.com
# Token: dapi... (generate from User Settings > Access Tokens)
```

**Option B: OAuth (Recommended for production)**

```bash
databricks configure --oauth
# Follow OAuth flow in browser
```

**Verify Configuration:**

```bash
# Test connection
databricks workspace ls /
# Should list workspace folders without errors
```

### Step 2: Verify SQL Warehouse Access

```bash
# List SQL warehouses
databricks sql-warehouses list

# Should show at least one warehouse
# Note the warehouse ID for later use
```

### Step 3: Create Databricks Personal Access Token

1. Log into Databricks workspace
2. Click your username (top right) → **Settings**
3. Navigate to **Developer** → **Access tokens**
4. Click **Generate new token**
5. Set comment: "MCP Universal Client Demo"
6. Set lifetime: 90 days
7. Click **Generate**
8. **Copy token immediately** (you won't see it again)

## Local Environment Setup

### Step 1: Clone Repository

```bash
# Clone repository
git clone https://github.com/your-org/databricks-mcp-demo
cd databricks-mcp-demo

# Verify structure
ls -la
# Should see: demos/, shared/, scripts/, docs/, README.md
```

### Step 2: Create Virtual Environment

**Using venv (standard library):**

```bash
# Create virtual environment
python3 -m venv venv

# Activate (macOS/Linux)
source venv/bin/activate

# Activate (Windows)
venv\Scripts\activate

# Verify activation
which python
# Should show path inside venv/ directory
```

**Using conda:**

```bash
# Create environment
conda create -n databricks-mcp python=3.10

# Activate
conda activate databricks-mcp
```

### Step 3: Install Dependencies

```bash
# Install core dependencies
pip install -r requirements.txt

# Verify installations
python -c "import databricks.sdk; print('Databricks SDK:', databricks.sdk.__version__)"
python -c "import dotenv; print('python-dotenv: OK')"
```

**Expected Output:**
```
Databricks SDK: 0.20.0
python-dotenv: OK
```

### Step 4: Configure Environment Variables

```bash
# Copy example environment file
cp .env.example .env

# Edit .env file
nano .env  # or use your preferred editor
```

**Minimum required configuration:**

```bash
# .env file contents

# Databricks Workspace
DATABRICKS_HOST=https://your-workspace.databricks.com
DATABRICKS_TOKEN=dapi...  # Your personal access token

# Or use CLI profile instead of token
# DATABRICKS_CONFIG_PROFILE=DEFAULT

# SQL Warehouse (get ID from Step 2)
DATABRICKS_WAREHOUSE_ID=abc123def456

# Genie Space (for Slack demo)
GENIE_SPACE_ID=your_genie_space_id  # Optional initially

# Vector Search Index (for RAG demo)
VECTOR_SEARCH_INDEX_ID=main.docs.technical_index  # Created in next section

# UC Function (for REST API and Pipeline demos)
UC_FUNCTION_NAME=demo_retail.ecommerce.calculate_discount  # Created in next section
```

**Test Configuration:**

```bash
# Test workspace connection
python -c "
from shared.config import get_workspace_client
w = get_workspace_client()
print('Connected to workspace:', w.config.host)
print('Current user:', w.current_user.me().user_name)
"
```

Expected output:
```
Connected to workspace: https://your-workspace.databricks.com
Current user: your.email@company.com
```

## Data Source Setup

### Setup 1: Unity Catalog Function (Required for REST API and Pipeline demos)

**Automated Setup:**

```bash
# Run UC Function setup script
python scripts/setup_uc_function.py
```

**Expected Output:**
```
======================================================================
🔧 Unity Catalog Function Setup
======================================================================

📊 Step 1: Creating catalog and schema...
✅ Using SQL warehouse: Starter Warehouse (abc123)
✅ Catalog created: demo_retail
✅ Schema created: demo_retail.ecommerce
✅ Function created: demo_retail.ecommerce.calculate_discount

🧪 Step 2: Testing UC Function...

Test: $50,000.00 / Enterprise
  ✅ Function executed successfully
Test: $25,000.00 / Mid-Market
  ✅ Function executed successfully
...

======================================================================
🎉 Setup Complete!
======================================================================

Function Details:
  📝 Name: demo_retail.ecommerce.calculate_discount
  📊 Catalog: demo_retail
  📁 Schema: ecommerce
```

**Verify UC Function:**

```bash
# Test function manually
databricks sql-warehouses execute <warehouse-id> \
  "SELECT demo_retail.ecommerce.calculate_discount(50000.0, 'Enterprise') as result"
```

**Add to .env:**

```bash
# Update .env file
echo "UC_FUNCTION_NAME=demo_retail.ecommerce.calculate_discount" >> .env
```

### Setup 2: Vector Search Index (Required for RAG demo)

**Option A: Automated Setup (Recommended)**

```bash
# Run Vector Search setup script
python scripts/create_vector_search.py
```

This script:
1. Creates catalog `main` and schema `docs` (if needed)
2. Creates Delta table with sample documentation
3. Creates Vector Search endpoint (serverless)
4. Creates vector index with delta sync
5. Waits for index to be ready
6. Tests search functionality

**Expected Output:**
```
======================================================================
🔧 Vector Search Index Setup
======================================================================

📊 Step 1: Creating catalog and schema...
✅ Catalog exists: main
✅ Schema created: main.docs

📄 Step 2: Creating source Delta table...
✅ Table created: main.docs.technical_docs
✅ Inserted 25 sample documents

🔍 Step 3: Creating Vector Search endpoint...
✅ Endpoint created: mcp-demo-endpoint (serverless)

🎯 Step 4: Creating vector index...
✅ Index created: main.docs.technical_index
⏳ Waiting for index to be ready (this may take 5-10 minutes)...
✅ Index ready! Status: ONLINE

🧪 Step 5: Testing vector search...
Query: "databricks authentication methods"
Found 3 relevant documents:
  1. "Authentication Guide" (score: 0.89)
  2. "Security Best Practices" (score: 0.76)
  3. "Unity Catalog Access Control" (score: 0.71)

======================================================================
🎉 Setup Complete!
======================================================================

Index Details:
  📝 Name: main.docs.technical_index
  📊 Endpoint: mcp-demo-endpoint
  📁 Source table: main.docs.technical_docs
  🔢 Embedding dimension: 1536
  📏 Delta sync: ENABLED
```

**Option B: Manual Setup**

If automated setup fails or you want to use existing data:

1. **Create Delta table with text documents:**

```sql
CREATE TABLE IF NOT EXISTS main.docs.technical_docs (
  id STRING,
  content STRING,
  metadata STRING
);

-- Insert sample documents
INSERT INTO main.docs.technical_docs VALUES
  ('doc1', 'Databricks authentication supports OAuth, tokens, and service principals...', '{"category": "auth"}'),
  ('doc2', 'Unity Catalog provides centralized governance...', '{"category": "governance"}');
```

2. **Create Vector Search endpoint** (via UI):
   - Navigate to **Compute** → **Vector Search**
   - Click **Create Endpoint**
   - Name: `mcp-demo-endpoint`
   - Type: Serverless
   - Click **Create**

3. **Create Vector Search index** (via UI):
   - Click **Create Index**
   - Name: `main.docs.technical_index`
   - Endpoint: `mcp-demo-endpoint`
   - Source table: `main.docs.technical_docs`
   - Primary key: `id`
   - Text column: `content`
   - Sync mode: **Continuous (Delta Sync)**
   - Click **Create**

4. **Wait for index to be online** (5-10 minutes)

**Add to .env:**

```bash
# Update .env file
echo "VECTOR_SEARCH_INDEX_ID=main.docs.technical_index" >> .env
```

### Setup 3: Genie Space (Required for Slack demo)

**Create Genie Space** (via UI):

1. Navigate to **Workspace** → **Genie** (in left sidebar)
2. Click **Create Genie Space**
3. Configure:
   - Name: "Sales Analytics Demo"
   - Data sources: Select relevant tables/schemas
   - Click **Create**
4. Note the **Space ID** (visible in URL or space settings)

**Add to .env:**

```bash
# Update .env file
echo "GENIE_SPACE_ID=01abc123-def4-5678-9012-34567890abcd" >> .env
```

### Setup 4: Slack Bot Configuration (Optional, for Slack demo only)

1. **Create Slack App:**
   - Go to https://api.slack.com/apps
   - Click **Create New App** → **From scratch**
   - Name: "Databricks Genie Bot"
   - Workspace: Select your development workspace

2. **Configure Socket Mode:**
   - Navigate to **Settings** → **Socket Mode**
   - Enable Socket Mode
   - Generate App-Level Token (scope: `connections:write`)
   - Copy token → Add to `.env` as `SLACK_APP_TOKEN`

3. **Configure Bot Token:**
   - Navigate to **OAuth & Permissions**
   - Add scopes:
     - `app_mentions:read`
     - `chat:write`
     - `channels:history`
   - Install app to workspace
   - Copy **Bot User OAuth Token** → Add to `.env` as `SLACK_BOT_TOKEN`

4. **Subscribe to Events:**
   - Navigate to **Event Subscriptions**
   - Enable Events
   - Subscribe to: `app_mention`

**Add to .env:**

```bash
# Update .env file (Slack demo only)
echo "SLACK_APP_TOKEN=xapp-..." >> .env
echo "SLACK_BOT_TOKEN=xoxb-..." >> .env
```

## Running the Demos

### Demo 1: Slack Bot (Genie Integration)

**Prerequisites:**
- ✅ Databricks authentication configured
- ✅ Genie space created and ID in `.env`
- ✅ Slack app configured (tokens in `.env`)

**Run:**

```bash
cd demos/01-slack-bot
python slack_bot.py
```

**Expected Output:**
```
======================================================================
Slack Bot - Genie Integration Demo
======================================================================

This bot demonstrates using the universal MCP client to integrate
Databricks Genie with Slack for natural language analytics.

✅ Slack bot initialized with universal MCP client
⚡ Bolt app is running! (Socket Mode)

📢 Bot is ready! Mention @databricks-genie-bot in any channel.

Example questions:
  • @bot What were total sales last quarter?
  • @bot Show me top 10 customers by revenue
  • @bot Compare this month vs last month performance
```

**Test in Slack:**
1. Invite bot to a channel: `/invite @databricks-genie-bot`
2. Mention bot with question: `@databricks-genie-bot What were sales last quarter?`
3. Bot responds with Genie analysis

**Stop:** Press `Ctrl+C`

### Demo 2: RAG Application (Vector Search Integration)

**Prerequisites:**
- ✅ Databricks authentication configured
- ✅ Vector Search index created and ID in `.env`

**Run:**

```bash
cd demos/02-rag-application
python rag_demo.py
```

**Expected Output:**
```
======================================================================
RAG Application Demo - Universal MCP Client Pattern
======================================================================

This demo shows document retrieval using Vector Search via the
universal MCP client for RAG applications.

✅ RAG Application initialized with universal MCP client

📋 Demo Scenario: Technical support chatbot

User Question: "How do I authenticate with Databricks?"

🔍 Step 1: Retrieving relevant documentation...
   • Searching Vector Search index: main.docs.technical_index
   • Looking for top 3 most relevant documents

📚 Retrieved Documents:
   1. "Authentication Guide" (relevance: 0.89)
      Databricks supports multiple authentication methods including OAuth 2.0,
      personal access tokens, and service principals...

   2. "Security Best Practices" (relevance: 0.76)
      When configuring authentication, always use service principals in
      production environments...

   3. "Unity Catalog Access Control" (relevance: 0.71)
      Authentication integrates with Unity Catalog's fine-grained access
      control...

🤖 Step 2: Generating response with context...
   (In production, send retrieved docs + question to LLM)

💡 Response:
   Databricks authentication supports OAuth 2.0, personal access tokens,
   and service principals. For production use, service principals are
   recommended for enhanced security. Authentication integrates with
   Unity Catalog for fine-grained access control.

======================================================================
Demo Complete
======================================================================

Key Takeaway:
  • Universal MCP client handles Vector Search communication
  • RAG app focuses on retrieval logic and response generation
  • Only ~15 lines of Databricks-specific code (9% of total)
```

**Interactive Mode:**

```bash
# Run in interactive mode
python rag_demo.py --interactive

# Ask questions:
> How do I create a Delta table?
> What is Unity Catalog?
> quit
```

### Demo 3: REST API (UC Functions Integration)

**Prerequisites:**
- ✅ Databricks authentication configured
- ✅ UC Function created and name in `.env`

**Run:**

```bash
cd demos/03-rest-api
python api_server.py
```

**Expected Output:**
```
======================================================================
REST API Demo - Universal MCP Client Pattern
======================================================================

This API demonstrates using UC Functions via the universal MCP client
for governed business logic.

✅ REST API initialized with universal MCP client
✅ Universal client connected to Databricks workspace

🌐 Starting FastAPI server...

INFO:     Started server process [12345]
INFO:     Waiting for application startup.
INFO:     Application startup complete.
INFO:     Uvicorn running on http://0.0.0.0:8000 (Press CTRL+C to quit)

📡 API Endpoints:
   • GET  /health          - Health check
   • POST /calculate-discount - Calculate discount using UC Function

📖 API Documentation:
   • Swagger UI: http://localhost:8000/docs
   • ReDoc:      http://localhost:8000/redoc
```

**Test API:**

```bash
# In another terminal, test endpoints

# Health check
curl http://localhost:8000/health

# Calculate discount
curl -X POST http://localhost:8000/calculate-discount \
  -H "Content-Type: application/json" \
  -d '{
    "order_amount": 50000.0,
    "customer_segment": "Enterprise"
  }'

# Expected response:
{
  "order_amount": 50000.0,
  "customer_segment": "Enterprise",
  "discount_amount": 10000.0,
  "discount_percentage": 20.0,
  "final_amount": 40000.0,
  "segment_tier": "Enterprise - Premium"
}
```

**Interactive API Documentation:**

Open http://localhost:8000/docs in browser for Swagger UI with interactive testing.

**Stop:** Press `Ctrl+C`

### Demo 4: Data Pipeline (Batch UC Functions)

**Prerequisites:**
- ✅ Databricks authentication configured
- ✅ UC Function created and name in `.env`

**Run:**

```bash
cd demos/04-data-pipeline
python pipeline_example.py
```

**Expected Output:**
```
======================================================================
Data Pipeline Demo - Universal MCP Client Pattern
======================================================================

This demo shows batch processing with UC Functions via the
universal MCP client. Notice:
  • Same UC Function as REST API uses (code reuse)
  • Same universal client (consistency)
  • Different execution pattern (batch vs single)

✅ Data Pipeline initialized with universal MCP client

📥 Input: 10 orders to process

🔄 Processing batch of 10 records...
✅ Batch processing complete:
   • Processed: 10 records
   • Errors: 0 records
   • Duration: 1.23s
   • Throughput: 8.1 records/second

💾 Saving 10 transformed records...
   Output path: s3://bucket/transformed/

📊 Sample transformed records:
   1. Order ORD-001: $50,000.00 → $40,000.00 (20.0% discount)
   2. Order ORD-002: $25,000.00 → $21,250.00 (15.0% discount)
   3. Order ORD-003: $75,000.00 → $60,000.00 (20.0% discount)
   ... and 7 more records

======================================================================
Demo Complete
======================================================================

Key Takeaways:
  • Universal MCP client works in batch context
  • UC Function reused from REST API (no duplicate logic)
  • Batch processing with concurrency control
  • Same governance, audit trail, and access control
```

**Test Single Record:**

```bash
# Test with single record (useful for debugging)
python pipeline_example.py test
```

## Troubleshooting

### Issue: "Authentication failed"

**Error:**
```
databricks.sdk.errors.Unauthenticated: Authentication failed
```

**Solutions:**

1. Verify Databricks CLI configuration:
```bash
databricks auth profiles
# Should show DEFAULT profile

databricks workspace ls /
# Should list workspace folders
```

2. Check .env file:
```bash
cat .env | grep DATABRICKS
# Verify DATABRICKS_HOST and DATABRICKS_TOKEN are set
```

3. Generate new token:
- Old token may have expired
- Generate new token (see Step 3 in Workspace Configuration)
- Update .env with new token

### Issue: "UC Function not found"

**Error:**
```
databricks.sdk.errors.NotFound: Function 'demo_retail.ecommerce.calculate_discount' not found
```

**Solutions:**

1. Verify function exists:
```bash
databricks sql-warehouses execute <warehouse-id> \
  "SHOW FUNCTIONS IN demo_retail.ecommerce"
# Should list calculate_discount
```

2. Re-run setup script:
```bash
python scripts/setup_uc_function.py
```

3. Check catalog permissions:
```bash
databricks sql-warehouses execute <warehouse-id> \
  "SHOW GRANTS ON CATALOG demo_retail"
# Verify you have EXECUTE permission
```

### Issue: "Vector Search index not ready"

**Error:**
```
databricks.sdk.errors.InvalidState: Vector Search index is not ready
```

**Solutions:**

1. Check index status:
```python
from shared.config import get_workspace_client
w = get_workspace_client()
index = w.vector_search_indexes.get_index(name="main.docs.technical_index")
print("Status:", index.status.state)
# Should be: ONLINE
```

2. Wait for index to be ready (5-10 minutes after creation)

3. Check for errors:
```python
if index.status.message:
    print("Error:", index.status.message)
```

### Issue: "Slack bot not responding"

**Error:**
Bot doesn't respond to mentions in Slack

**Solutions:**

1. Verify bot is running:
```bash
# Check terminal for "Bolt app is running!" message
```

2. Check Slack tokens in .env:
```bash
cat .env | grep SLACK
# Verify SLACK_APP_TOKEN and SLACK_BOT_TOKEN are set
```

3. Verify bot is invited to channel:
```
/invite @databricks-genie-bot
```

4. Check Slack app configuration:
- Socket Mode: Enabled
- Event Subscriptions: `app_mention` subscribed
- Bot scopes: `app_mentions:read`, `chat:write`

### Issue: "Module not found"

**Error:**
```
ModuleNotFoundError: No module named 'databricks'
```

**Solutions:**

1. Verify virtual environment is activated:
```bash
which python
# Should show path inside venv/ directory
```

2. Reinstall dependencies:
```bash
pip install -r requirements.txt
```

3. Check Python version:
```bash
python --version
# Should be 3.9 or higher
```

### Issue: "Connection timeout"

**Error:**
```
asyncio.TimeoutError: Connection to Databricks timed out
```

**Solutions:**

1. Check workspace URL:
```bash
echo $DATABRICKS_HOST
# Should be: https://your-workspace.databricks.com
# NOT: https://your-workspace.cloud.databricks.com
```

2. Test network connectivity:
```bash
curl -I https://your-workspace.databricks.com
# Should return 200 OK or redirect
```

3. Check firewall/VPN:
- Ensure Databricks workspace is accessible
- Try from different network if corporate firewall blocks access

### Debug Mode

Enable debug logging for troubleshooting:

```bash
# Set environment variable
export DEBUG=true

# Run demo
python demos/02-rag-application/rag_demo.py
```

This enables detailed logging of:
- MCP protocol messages
- API requests/responses
- Authentication flow
- Error stack traces

## Production Deployment

### Environment Configuration

**Development:**
```bash
# .env
DATABRICKS_CONFIG_PROFILE=DEFAULT  # Use CLI profile
DEBUG=true
```

**Production:**
```bash
# Use environment variables (not .env file)
export DATABRICKS_HOST=https://prod-workspace.databricks.com
export DATABRICKS_TOKEN=<from-secrets-manager>  # Use service principal token
export DEBUG=false
export LOG_LEVEL=INFO
```

### Service Principal Setup

1. **Create service principal:**
```bash
databricks service-principals create \
  --display-name "mcp-client-prod"
```

2. **Grant permissions:**
```sql
-- Grant catalog access
GRANT USE CATALOG ON CATALOG demo_retail TO `mcp-client-prod`;
GRANT USE SCHEMA ON SCHEMA demo_retail.ecommerce TO `mcp-client-prod`;
GRANT EXECUTE ON FUNCTION demo_retail.ecommerce.calculate_discount TO `mcp-client-prod`;
```

3. **Generate token:**
```bash
databricks tokens create \
  --lifetime-seconds 31536000 \
  --comment "Production MCP Client"
```

4. **Store securely:**
- AWS: Secrets Manager
- Azure: Key Vault
- GCP: Secret Manager

### Docker Deployment

**Dockerfile:**
```dockerfile
FROM python:3.10-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install --no-cache-dir -r requirements.txt

COPY shared/ shared/
COPY demos/03-rest-api/ .

# Don't copy .env - use environment variables
CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

**Build and run:**
```bash
docker build -t databricks-mcp-api .

docker run -p 8000:8000 \
  -e DATABRICKS_HOST=$DATABRICKS_HOST \
  -e DATABRICKS_TOKEN=$DATABRICKS_TOKEN \
  -e UC_FUNCTION_NAME=$UC_FUNCTION_NAME \
  databricks-mcp-api
```

### Kubernetes Deployment

**ConfigMap (non-sensitive):**
```yaml
apiVersion: v1
kind: ConfigMap
metadata:
  name: databricks-config
data:
  DATABRICKS_HOST: "https://prod-workspace.databricks.com"
  UC_FUNCTION_NAME: "demo_retail.ecommerce.calculate_discount"
```

**Secret (sensitive):**
```yaml
apiVersion: v1
kind: Secret
metadata:
  name: databricks-secret
type: Opaque
stringData:
  DATABRICKS_TOKEN: "dapi..."  # From Secrets Manager
```

**Deployment:**
```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: databricks-mcp-api
spec:
  replicas: 3
  selector:
    matchLabels:
      app: databricks-mcp-api
  template:
    metadata:
      labels:
        app: databricks-mcp-api
    spec:
      containers:
      - name: api
        image: databricks-mcp-api:latest
        ports:
        - containerPort: 8000
        envFrom:
        - configMapRef:
            name: databricks-config
        - secretRef:
            name: databricks-secret
        resources:
          requests:
            memory: "256Mi"
            cpu: "250m"
          limits:
            memory: "512Mi"
            cpu: "500m"
```

### Monitoring

**Health Check Endpoint:**

Add to all production deployments:

```python
@app.get("/health")
async def health_check():
    try:
        # Test Databricks connection
        await mcp_client.test_connection()
        return {"status": "healthy", "timestamp": datetime.utcnow()}
    except Exception as e:
        return {"status": "unhealthy", "error": str(e)}, 503
```

**Prometheus Metrics:**

```python
from prometheus_client import Counter, Histogram, make_asgi_app

# Metrics
requests_total = Counter('mcp_requests_total', 'Total requests', ['capability'])
request_duration = Histogram('mcp_request_duration_seconds', 'Request duration')

# Add metrics endpoint
metrics_app = make_asgi_app()
app.mount("/metrics", metrics_app)
```

## Next Steps

After completing setup:

1. **Explore Architecture:** Read [ARCHITECTURE.md](ARCHITECTURE.md) for technical deep-dive
2. **Understand Metrics:** See [METRICS.md](METRICS.md) for code measurements
3. **Read Blog Post:** [BLOG_POST_V3.md](../BLOG_POST_V3.md) for full context
4. **Customize:** Adapt demos to your use cases
5. **Deploy:** Follow production deployment guide above

## Support

- **Issues:** https://github.com/your-org/databricks-mcp-demo/issues
- **Databricks MCP Docs:** https://docs.databricks.com/mcp/
- **Databricks Community:** https://community.databricks.com/

## License

This reference implementation is provided for educational purposes. Adapt freely to your organization's needs.
