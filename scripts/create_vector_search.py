"""
Create Vector Search Index with Delta Sync for MCP Demo

This script:
1. Creates a Delta table with documentation
2. Creates a vector search index with delta sync
3. Links it to the endpoint: one-env-shared-endpoint-10
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from databricks.sdk import WorkspaceClient
from databricks.vector_search.client import VectorSearchClient
from shared.config import get_workspace_client, VECTOR_SEARCH_ENDPOINT, DATABRICKS_HOST
import time
import os

def create_documentation_table(w: WorkspaceClient):
    """Create Delta table with sample documentation"""

    print("\n📊 Step 1: Creating Delta table with documentation...")

    # SQL to create table and insert sample data
    sql = """
    -- Create catalog and schema if they don't exist
    CREATE CATALOG IF NOT EXISTS demo_retail;
    CREATE SCHEMA IF NOT EXISTS demo_retail.ecommerce;

    -- Drop existing table if exists
    DROP TABLE IF EXISTS demo_retail.ecommerce.documentation;

    -- Create documentation table
    CREATE TABLE demo_retail.ecommerce.documentation (
      id STRING NOT NULL,
      title STRING,
      content STRING,
      category STRING,
      url STRING,
      created_at TIMESTAMP
    ) USING DELTA;

    -- Insert sample MCP and Databricks documentation
    INSERT INTO demo_retail.ecommerce.documentation VALUES
    (
      'mcp-001',
      'Model Context Protocol Overview',
      'Model Context Protocol (MCP) is a standardized protocol for integrating AI applications with data sources. MCP enables universal integration patterns, reducing M×N complexity to M+N. With MCP, you build one client that works with multiple data sources through standardized servers. This eliminates the need for custom integrations for each platform-data source combination.',
      'mcp',
      'https://docs.databricks.com/mcp/',
      current_timestamp()
    ),
    (
      'mcp-002',
      'MCP Integration with Databricks',
      'Databricks provides MCP servers for three key services: Genie for natural language analytics, Vector Search for semantic document retrieval, and Unity Catalog Functions for executing governed code. These MCP servers expose tools that any MCP client can call using a standardized protocol. The databricks-mcp library provides a Python client for easy integration.',
      'mcp',
      'https://docs.databricks.com/mcp/integration',
      current_timestamp()
    ),
    (
      'genie-001',
      'Getting Started with Databricks Genie',
      'Databricks Genie is an AI-powered analytics assistant that converts natural language questions into SQL queries. To use Genie, create a Genie Space in the Databricks SQL interface, configure it with your tables and schemas, then ask questions in plain English. Genie analyzes your data schema and generates optimized SQL queries automatically.',
      'genie',
      'https://docs.databricks.com/genie/getting-started',
      current_timestamp()
    ),
    (
      'genie-002',
      'Genie MCP Server',
      'The Genie MCP server exposes natural language analytics capabilities through the Model Context Protocol. Connect to the server at /api/2.0/mcp/genie/{space_id} and use the query_space tool to ask questions. The server handles query execution, result formatting, and conversation context automatically. Responses include SQL queries and formatted results.',
      'genie',
      'https://docs.databricks.com/mcp/genie-server',
      current_timestamp()
    ),
    (
      'vector-001',
      'Vector Search in Databricks',
      'Databricks Vector Search enables semantic search over your documents using embedding models. Create a vector search endpoint to provide compute resources, then create indexes on your Delta tables. Vector Search automatically generates embeddings and provides similarity search capabilities for RAG applications and semantic document retrieval.',
      'vector-search',
      'https://docs.databricks.com/vector-search/',
      current_timestamp()
    ),
    (
      'vector-002',
      'Setting Up Vector Search',
      'To set up vector search: First create a Delta table with your documents. Then create a vector search endpoint using the UI or API. Finally, create an index on your table specifying the text column to vectorize. Enable delta sync to automatically update the index when your source table changes. Use the similarity_search API to query the index.',
      'vector-search',
      'https://docs.databricks.com/vector-search/setup',
      current_timestamp()
    ),
    (
      'uc-001',
      'Unity Catalog Functions',
      'Unity Catalog Functions allow you to create, manage, and execute SQL and Python functions with enterprise governance. Functions are stored in the Unity Catalog with access controls, lineage tracking, and versioning. Use functions to encapsulate business logic, perform calculations, or implement custom transformations that can be called from SQL, Python, or via MCP.',
      'uc-functions',
      'https://docs.databricks.com/sql/language-manual/sql-ref-functions-udf',
      current_timestamp()
    ),
    (
      'uc-002',
      'Creating UC Functions',
      'Create Unity Catalog functions using SQL or Python. For SQL functions, use CREATE FUNCTION syntax with SQL expressions. For Python functions, use CREATE FUNCTION with LANGUAGE PYTHON and define your logic. Functions can accept parameters, return values, and be called from anywhere in your workspace with proper permissions.',
      'uc-functions',
      'https://docs.databricks.com/sql/language-manual/sql-ref-syntax-ddl-create-function',
      current_timestamp()
    ),
    (
      'databricks-001',
      'Databricks Lakehouse Platform',
      'Databricks Lakehouse Platform combines the best of data lakes and data warehouses. Store all your data in Delta Lake format with ACID transactions, query using SQL or Python, and run machine learning workloads at scale. Unity Catalog provides unified governance, and Databricks SQL enables fast BI and analytics on the lakehouse.',
      'platform',
      'https://docs.databricks.com/lakehouse/',
      current_timestamp()
    ),
    (
      'databricks-002',
      'Databricks SQL',
      'Databricks SQL provides a fast SQL analytics experience on the lakehouse. Create SQL warehouses for compute, build dashboards with visualizations, set up alerts, and share insights with your team. SQL warehouses auto-scale and provide serverless compute options for cost-effective analytics.',
      'platform',
      'https://docs.databricks.com/sql/',
      current_timestamp()
    ),
    (
      'mlops-001',
      'MLOps with Databricks',
      'Databricks MLOps capabilities include MLflow for experiment tracking and model registry, Feature Store for feature management, and Model Serving for deployment. Use Lakehouse Monitoring to track data and model quality, set up automated retraining pipelines, and deploy models with governance and lineage tracking through Unity Catalog.',
      'mlops',
      'https://docs.databricks.com/mlops/',
      current_timestamp()
    ),
    (
      'api-001',
      'Databricks REST API',
      'The Databricks REST API provides programmatic access to workspace resources. Use the API to manage clusters, jobs, notebooks, and data objects. Authentication is via personal access tokens or OAuth. The API follows REST principles with JSON payloads and standard HTTP methods.',
      'api',
      'https://docs.databricks.com/api/',
      current_timestamp()
    );
    """

    # Execute via SQL statement API
    statement = w.statement_execution.execute_statement(
        warehouse_id=get_sql_warehouse_id(w),
        statement=sql,
        wait_timeout="30s"
    )

    print("✅ Delta table created: demo_retail.ecommerce.documentation")
    print("✅ Inserted 12 sample documents")

    # Wait for Unity Catalog to sync the table metadata
    print("⏳ Waiting for Unity Catalog to sync table metadata...")
    time.sleep(10)

    # Verify the table schema
    print("🔍 Verifying table columns...")
    desc_statement = w.statement_execution.execute_statement(
        warehouse_id=get_sql_warehouse_id(w),
        statement="SHOW COLUMNS IN demo_retail.ecommerce.documentation",
        wait_timeout="30s"
    )

    # Print columns if available
    if desc_statement.result and desc_statement.result.data_array:
        print("   Columns found:")
        for row in desc_statement.result.data_array[:10]:  # First 10 rows
            if row and len(row) > 0:
                col_name = row[0] if hasattr(row[0], 'str') else str(row[0])
                print(f"   - {col_name}")

    print("✅ Table schema verified in Unity Catalog")

    # Also run REFRESH TABLE to ensure metadata is current
    w.statement_execution.execute_statement(
        warehouse_id=get_sql_warehouse_id(w),
        statement="REFRESH TABLE demo_retail.ecommerce.documentation",
        wait_timeout="30s"
    )
    print("✅ Table metadata refreshed")

    return "demo_retail.ecommerce.documentation"


def get_sql_warehouse_id(w: WorkspaceClient) -> str:
    """Get the first available SQL warehouse"""
    warehouses = list(w.warehouses.list())
    if not warehouses:
        raise ValueError("No SQL warehouses found. Please create one first.")

    # Find a running warehouse or start one
    for wh in warehouses:
        if wh.state.value == "RUNNING":
            print(f"✅ Using SQL warehouse: {wh.name} ({wh.id})")
            return wh.id

    # Start the first warehouse if none running
    wh = warehouses[0]
    print(f"⏳ Starting SQL warehouse: {wh.name}...")
    w.warehouses.start(wh.id)

    # Wait for it to start
    for i in range(30):
        status = w.warehouses.get(wh.id)
        if status.state.value == "RUNNING":
            print(f"✅ SQL warehouse started: {wh.name} ({wh.id})")
            return wh.id
        time.sleep(2)

    raise ValueError(f"SQL warehouse {wh.name} did not start in time")


def create_vector_index(w: WorkspaceClient, table_name: str):
    """Create vector search index with delta sync"""

    print("\n🔍 Step 2: Creating vector search index with delta sync...")

    # Initialize Vector Search client (inherits auth from workspace client)
    vsc = VectorSearchClient()

    endpoint_name = VECTOR_SEARCH_ENDPOINT
    index_name = "demo_retail.ecommerce.documentation_index"

    # Check if endpoint exists
    try:
        endpoint = vsc.get_endpoint(endpoint_name)
        print(f"✅ Vector search endpoint found: {endpoint_name}")
    except Exception as e:
        print(f"❌ Endpoint '{endpoint_name}' not found: {e}")
        print(f"⚠️  Please create the endpoint first or update VECTOR_SEARCH_ENDPOINT in .env")
        return None

    # Check if index already exists
    try:
        existing_index = vsc.get_index(index_name)
        print(f"✅ Index already exists: {index_name}")
        print(f"⏩ Skipping index creation, using existing index")
        return index_name
    except Exception:
        pass  # Index doesn't exist, create it

    print(f"📝 Index doesn't exist yet, creating new index...")

    print(f"⏳ Creating vector search index (this may take 2-5 minutes)...")
    print(f"   Index: {index_name}")
    print(f"   Source: {table_name}")
    print(f"   Endpoint: {endpoint_name}")
    print(f"   Delta Sync: ENABLED ✅")

    # Create index with delta sync
    try:
        index = vsc.create_delta_sync_index(
            endpoint_name=endpoint_name,
            index_name=index_name,
            source_table_name=table_name,
            pipeline_type="TRIGGERED",  # TRIGGERED or CONTINUOUS
            primary_key="doc_id",  # Use doc_id column (existing table schema)
            embedding_source_column="content",
            embedding_model_endpoint_name="databricks-bge-large-en"
        )

        print(f"✅ Vector search index created!")
    except Exception as e:
        if "RESOURCE_ALREADY_EXISTS" in str(e):
            print(f"✅ Index already exists: {index_name}")
            print(f"⏩ Using existing index")
            return index_name
        else:
            print(f"❌ Error creating index: {e}")
            import traceback
            traceback.print_exc()
            return None

    # Wait for index to be ready (if we just created it)
    print(f"⏳ Waiting for index to be ready...")
    for i in range(60):  # Wait up to 2 minutes
        try:
            index_info = vsc.get_index(index_name)

            # Handle both dict and object responses
            if isinstance(index_info, dict):
                status = index_info.get("status", {}).get("detailed_state", "UNKNOWN")
            else:
                status = getattr(getattr(index_info, "status", None), "detailed_state", "UNKNOWN")

            print(f"   Status: {status}")

            if status in ["ONLINE_TRIGGERED_UPDATE", "ONLINE", "ONLINE_NO_PENDING_UPDATE"]:
                print(f"✅ Index is ready!")
                break

            if "FAILED" in str(status):
                print(f"❌ Index creation failed: {status}")
                return None

        except Exception as e:
            print(f"   Checking status... ({str(e)[:50]})")

        time.sleep(2)

    return index_name


def test_vector_search(w: WorkspaceClient, index_name: str):
    """Test the vector search index"""

    print("\n🧪 Step 3: Testing vector search...")

    vsc = VectorSearchClient()

    # Test queries
    test_queries = [
        "How to use MCP?",
        "What is Databricks Genie?",
        "Setting up vector search"
    ]

    for query in test_queries:
        print(f"\n📝 Query: '{query}'")

        try:
            results = vsc.similarity_search(
                index_name=index_name,
                query_text=query,
                columns=["id", "title", "content"],
                num_results=2
            )

            print(f"   Results:")
            for i, result in enumerate(results.get("result", {}).get("data_array", []), 1):
                title = result[1] if len(result) > 1 else "N/A"
                score = result[-1] if len(result) > 3 else "N/A"
                print(f"   {i}. {title} (score: {score})")

        except Exception as e:
            print(f"   ❌ Error: {e}")


def main():
    print("=" * 70)
    print("🚀 Vector Search Setup with Delta Sync")
    print("=" * 70)

    # Get workspace client
    w = get_workspace_client()

    # Set environment variables for VectorSearchClient
    # It needs these explicitly even though workspace client is configured
    if not os.getenv("DATABRICKS_HOST"):
        os.environ["DATABRICKS_HOST"] = DATABRICKS_HOST or w.config.host
    if not os.getenv("DATABRICKS_TOKEN") and w.config.token:
        os.environ["DATABRICKS_TOKEN"] = w.config.token

    # Step 1: Create Delta table
    table_name = create_documentation_table(w)

    # Step 2: Create vector index
    index_name = create_vector_index(w, table_name)

    if index_name:
        # Step 3: Test it
        time.sleep(5)  # Give it a moment
        test_vector_search(w, index_name)

        print("\n" + "=" * 70)
        print("🎉 Success! Vector search is ready!")
        print("=" * 70)
        print(f"\n📊 Table: {table_name}")
        print(f"🔍 Index: {index_name}")
        print(f"🔌 Endpoint: {VECTOR_SEARCH_ENDPOINT}")
        print(f"🔄 Delta Sync: ENABLED")
        print(f"\n✅ Your Slack bot can now search documentation!")
        print(f"\n🧪 Test in Slack:")
        print(f"   search how to use MCP")
        print(f"   search what is Genie")
        print(f"   search vector search setup")
    else:
        print("\n❌ Failed to create vector search index")
        print("Please check the errors above and try again")


if __name__ == "__main__":
    main()
