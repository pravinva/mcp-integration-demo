#!/usr/bin/env python3
"""
Create Vector Search Index for MCP Demo

Creates a Vector Search index from the documentation table.
The index enables semantic search via MCP server.

Requirements:
- Vector Search endpoint (provides compute)
- Vector Search index (created from documentation table)
"""

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from shared.config import get_workspace_client
import time

def create_vector_search_index():
    """Create Vector Search index from documentation table"""
    
    print("=" * 60)
    print("📚 Creating Vector Search Index")
    print("=" * 60)
    
    client = get_workspace_client()
    
    # Use Vector Search APIs from databricks-sdk
    try:
        from databricks.sdk.service.vectorsearch import VectorSearchEndpointsAPI, VectorSearchIndexesAPI
        endpoints_api = VectorSearchEndpointsAPI(client.api_client)
        indexes_api = VectorSearchIndexesAPI(client.api_client)
        print("✅ Vector Search APIs initialized")
    except ImportError as e:
        print(f"❌ Vector Search APIs not available: {e}")
        print("   Make sure databricks-sdk is up to date")
        return False
    
    # Configuration
    catalog = "demo_retail"
    schema = "ecommerce"
    table_name = "documentation"
    index_name = "documentation_index"
    full_index_name = f"{catalog}.{schema}.{index_name}"
    
    print(f"\n📋 Configuration:")
    print(f"   Catalog: {catalog}")
    print(f"   Schema: {schema}")
    print(f"   Source Table: {table_name}")
    print(f"   Index Name: {full_index_name}")
    
    # Check for Vector Search endpoints
    print(f"\n📡 Checking Vector Search Endpoints...")
    endpoint_name = None
    try:
        # List endpoints (returns Iterator)
        endpoints = list(endpoints_api.list_endpoints())
        
        if endpoints:
            # Use first available endpoint
            endpoint = endpoints[0]
            endpoint_name = endpoint.name
            status = getattr(endpoint, 'endpoint_status', getattr(endpoint, 'status', 'UNKNOWN'))
            print(f"✅ Found endpoint: {endpoint_name} (Status: {status})")
        else:
            print("⚠️  No Vector Search endpoints found")
            print("   Creating endpoint...")
            # Create endpoint
            endpoint_name = "mcp-demo-endpoint"
            try:
                from databricks.sdk.service.vectorsearch import EndpointType
                endpoint = endpoints_api.create_endpoint(
                    name=endpoint_name,
                    endpoint_type=EndpointType.STANDARD
                )
                # Wait for endpoint to be ready
                endpoint.wait()
                print(f"✅ Created endpoint: {endpoint_name}")
            except Exception as e:
                if "already exists" in str(e).lower() or "RESOURCE_ALREADY_EXISTS" in str(e):
                    endpoint_name = "mcp-demo-endpoint"
                    print(f"✅ Endpoint already exists: {endpoint_name}")
                else:
                    print(f"❌ Error creating endpoint: {e}")
                    import traceback
                    traceback.print_exc()
                    return False
    except Exception as e:
        print(f"⚠️  Error checking endpoints: {e}")
        print("   Trying with default endpoint name...")
        endpoint_name = "mcp-demo-endpoint"
    
    if not endpoint_name:
        print("❌ No endpoint available")
        return False
    
    # Check if index already exists
    print(f"\n🔍 Checking if index exists...")
    try:
        indexes = list(indexes_api.list_indexes(endpoint_name=endpoint_name))
        existing = next((idx for idx in indexes if idx.name == full_index_name), None)
        if existing:
            print(f"✅ Index already exists: {full_index_name}")
            index_id = getattr(existing, 'index_id', getattr(existing, 'name', 'N/A'))
            print(f"   Index ID: {index_id}")
            return True
    except Exception as e:
        print(f"⚠️  Could not check existing indexes: {e}")
        print("   Proceeding to create...")
    
    # Create the index
    print(f"\n🔨 Creating Vector Search index...")
    print(f"   Endpoint: {endpoint_name}")
    print(f"   Index: {full_index_name}")
    print("   This may take a few minutes...")
    
    try:
        from databricks.sdk.service.vectorsearch import (
            VectorIndexType,
            DeltaSyncVectorIndexSpecRequest,
            EmbeddingSourceColumn,
            PipelineType
        )
        
        # Create delta sync index spec
        delta_spec = DeltaSyncVectorIndexSpecRequest(
            source_table=f"{catalog}.{schema}.{table_name}",
            pipeline_type=PipelineType.TRIGGERED,
            embedding_source_columns=[
                EmbeddingSourceColumn(
                    embedding_model_endpoint_name="databricks-gte-large-en",
                    name="content"
                )
            ]
        )
        
        # Create the index
        index = indexes_api.create_index(
            name=full_index_name,
            endpoint_name=endpoint_name,
            primary_key="doc_id",
            index_type=VectorIndexType.DELTA_SYNC,
            delta_sync_index_spec=delta_spec
        )
        
        print(f"✅ Index creation initiated!")
        print(f"   Index: {full_index_name}")
        
        # Sync the index
        print(f"\n🔄 Syncing index...")
        try:
            indexes_api.sync_index(endpoint_name=endpoint_name, index_name=full_index_name)
            print("✅ Index sync triggered")
        except Exception as sync_error:
            if "not ready" in str(sync_error).lower():
                print("⚠️  Index not ready for sync yet")
                print("   Will sync automatically when ready")
            else:
                print(f"⚠️  Sync note: {sync_error}")
        
        # Wait for index to be ready
        print(f"\n⏳ Waiting for index to be ready...")
        max_wait = 300  # 5 minutes
        waited = 0
        
        while waited < max_wait:
            time.sleep(10)
            waited += 10
            
            try:
                status = indexes_api.get_index(endpoint_name=endpoint_name, index_name=full_index_name)
                index_status = getattr(status, 'status', getattr(status, 'index_status', 'UNKNOWN'))
                print(f"   Status after {waited}s: {index_status}")
                
                if index_status in ['ONLINE', 'ACTIVE', 'READY']:
                    print(f"\n✅ Index is ready!")
                    index_id = getattr(status, 'index_id', getattr(status, 'name', 'N/A'))
                    print(f"   Index ID: {index_id}")
                    return True
                elif index_status in ['FAILED', 'ERROR']:
                    print(f"\n❌ Index creation failed")
                    return False
                    
            except Exception as e:
                if waited < 60:  # Only show errors after 1 minute
                    print(f"   Still initializing... ({waited}s)")
                else:
                    print(f"   Status check: {str(e)[:100]}")
        
        print(f"\n⚠️  Index creation taking longer than expected")
        print(f"   Check status manually in Databricks UI")
        print(f"   Index: {full_index_name}")
        return True
        
    except Exception as e:
        print(f"\n❌ Error creating index: {e}")
        import traceback
        traceback.print_exc()
        
        # Try alternative approach - maybe need different parameters
        print(f"\n💡 Alternative: Create index via SQL or Databricks UI")
        print(f"   See: https://docs.databricks.com/en/generative-ai/vector-search/create-index.html")
        return False


if __name__ == "__main__":
    success = create_vector_search_index()
    
    if success:
        print("\n" + "=" * 60)
        print("✅ Vector Search index setup complete!")
        print("=" * 60)
        print("\nNext steps:")
        print("1. Test MCP server: python scripts/check_mcp_servers.py")
        print("2. Run demo: python test_demo.py full")
    else:
        print("\n" + "=" * 60)
        print("❌ Vector Search index creation failed")
        print("=" * 60)
        print("\n💡 Options:")
        print("1. Create index manually in Databricks UI")
        print("2. Use mock mode for Vector Search (USE_MOCK_MCP=true)")
        print("3. Check Vector Search documentation for requirements")

