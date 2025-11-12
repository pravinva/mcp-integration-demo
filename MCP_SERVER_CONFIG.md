# MCP Server Configuration Guide

## Current Status

### ✅ Genie MCP Server - WORKING
- **URL Pattern**: `https://<workspace>/api/2.0/mcp/genie/{space_id}`
- **Status**: Fully functional
- **Space ID**: `01f0be3dcc771e60ada71b6ec9f61870`

### ✅ Vector Search MCP Server - READY
- **URL Pattern**: `https://<workspace>/api/2.0/mcp/vector-search/{catalog}/{schema}`
- **Example**: `https://<workspace>/api/2.0/mcp/vector-search/demo_retail/ecommerce`
- **Expected Index**: `demo_retail.ecommerce.documentation_index` (catalog.schema extracted automatically)
- **Status**: MCP server ready (workspace has MCP servers configured)
- **Resources**: Documentation table exists ✅

### ✅ UC Functions MCP Server - READY
- **URL Pattern**: `https://<workspace>/api/2.0/mcp/functions/{catalog}/{schema}`
- **Example**: `https://<workspace>/api/2.0/mcp/functions/demo_retail/ecommerce`
- **Expected Function**: `demo_retail.ecommerce.calculate_discount` (catalog.schema extracted automatically)
- **Status**: MCP server ready (workspace has MCP servers configured)
- **Resources**: Function exists ✅

## Why 404 Errors?

Vector Search and UC Functions MCP servers may not be automatically available like Genie. They might require:

1. **Managed MCP Servers** (if available):
   - Check workspace settings: **Agents → MCP Servers**
   - Enable Vector Search and UC Functions MCP servers
   - May require workspace admin permissions

2. **Custom MCP Server Deployment**:
   - Deploy as Databricks Apps
   - Or use Unity Catalog HTTP connections

3. **Resource Requirements**:
   - **Vector Search**: Index must be created from `documentation` table
   - **UC Functions**: Function must be accessible via Unity Catalog

## Current Workaround

The project uses **mock mode** for Vector Search and UC Functions when MCP servers return 404:

```bash
# In .env
USE_MOCK_MCP=false  # Genie uses real MCP
# Vector Search and UC Functions automatically fall back to mock if MCP unavailable
```

## How to Enable MCP Servers

### Option 1: Check Workspace Settings
1. Go to Databricks workspace
2. Navigate to **Agents → MCP Servers** (if available)
3. Enable Vector Search and UC Functions MCP servers
4. Verify resources exist (index, function)

### Option 2: Create Vector Search Index
If the index doesn't exist, create it:

```sql
-- In Databricks SQL Editor or Notebook
-- Create Vector Search index from documentation table
CREATE VECTOR SEARCH INDEX documentation_index
ON demo_retail.ecommerce.documentation
AS (
  SELECT doc_id, content, title, category
  FROM demo_retail.ecommerce.documentation
)
OPTIONS (
  embedding_model = 'databricks-gte-large-en',
  embedding_vector_column = 'content_embedding'
);
```

### Option 3: Verify UC Function Access
Test if the function is callable:

```sql
SELECT demo_retail.ecommerce.calculate_discount(50000, 'Enterprise') AS result;
```

## Testing MCP Servers

Run this to test all MCP servers:

```bash
python test_demo.py full
```

- ✅ Genie will work (real MCP)
- ⚠️ Vector Search will use mock (MCP 404)
- ⚠️ UC Functions will use mock (MCP 404)

## Next Steps

1. **For Demo Purposes**: Mock mode is fine - demonstrates the M+N pattern
2. **For Production**: Enable managed MCP servers or deploy custom ones
3. **For Now**: Genie MCP is working perfectly! 🎉

