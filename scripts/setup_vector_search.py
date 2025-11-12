#!/usr/bin/env python3
"""
Complete Vector Search Setup Script

This script:
1. Enables Change Data Feed (CDF) on the documentation table
2. Creates Vector Search endpoint (if needed)
3. Creates Vector Search index
4. Syncs the index
"""

import sys
from pathlib import Path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from shared.config import get_workspace_client
import time

def enable_cdf_via_sql(client):
    """Enable Change Data Feed on documentation table using SQL"""
    print("\n" + "=" * 60)
    print("🔧 Step 1: Enabling Change Data Feed")
    print("=" * 60)
    
    try:
        from databricks.sdk.service.sql import StatementState
        
        # Get SQL warehouse
        warehouses = list(client.warehouses.list())
        if not warehouses:
            print("❌ No SQL warehouse available")
            return False
        
        warehouse_id = warehouses[0].id
        warehouse_name = warehouses[0].name
        print(f"   Using warehouse: {warehouse_name}")
        
        # Use fully qualified table name (no need for USE statements)
        print("   Enabling Change Data Feed...")
        sql = "ALTER TABLE demo_retail.ecommerce.documentation SET TBLPROPERTIES (delta.enableChangeDataFeed = true)"
        
        result = client.statement_execution.execute_statement(
            warehouse_id=warehouse_id,
            statement=sql,
            wait_timeout='30s'
        )
        
        if result.status.state == StatementState.SUCCEEDED:
            print("✅ Change Data Feed enabled!")
            return True
        else:
            print(f"⚠️  Status: {result.status.state}")
            if result.status.state == StatementState.FAILED:
                # Try to get error message
                error_msg = getattr(result.status, 'error_message', None) or getattr(result.status, 'message', None) or str(result.status)
                print(f"   Error: {error_msg}")
            return False
            
    except Exception as e:
        print(f"❌ Error enabling CDF: {e}")
        import traceback
        traceback.print_exc()
        return False


def create_vector_search_index():
    """Create Vector Search index from documentation table"""
    
    print("\n" + "=" * 60)
    print("📚 Step 2: Creating Vector Search Index")
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
        endpoints = list(endpoints_api.list_endpoints())
        
        if endpoints:
            endpoint = endpoints[0]
            endpoint_name = endpoint.name
            status = getattr(endpoint, 'endpoint_status', getattr(endpoint, 'status', 'UNKNOWN'))
            print(f"✅ Found endpoint: {endpoint_name} (Status: {status})")
        else:
            print("⚠️  No Vector Search endpoints found")
            print("   Creating endpoint...")
            endpoint_name = "mcp-demo-endpoint"
            try:
                from databricks.sdk.service.vectorsearch import EndpointType
                endpoint = endpoints_api.create_endpoint(
                    name=endpoint_name,
                    endpoint_type=EndpointType.STANDARD
                )
                endpoint.wait()
                print(f"✅ Created endpoint: {endpoint_name}")
            except Exception as e:
                if "already exists" in str(e).lower() or "RESOURCE_ALREADY_EXISTS" in str(e):
                    print(f"✅ Endpoint already exists: {endpoint_name}")
                else:
                    print(f"❌ Error creating endpoint: {e}")
                    return False
    except Exception as e:
        print(f"⚠️  Error checking endpoints: {e}")
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
            # sync_index takes index_name only (not endpoint_name)
            indexes_api.sync_index(index_name=full_index_name)
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
                # get_index takes index_name only (not endpoint_name)
                status = indexes_api.get_index(index_name=full_index_name)
                index_status = getattr(status, 'status', getattr(status, 'index_status', 'UNKNOWN'))
                if hasattr(index_status, 'value'):
                    index_status = index_status.value
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
                if waited < 60:
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
        return False


def main():
    """Main execution"""
    print("=" * 60)
    print("🚀 Vector Search Complete Setup")
    print("=" * 60)
    
    client = get_workspace_client()
    
    # Step 1: Enable CDF
    if not enable_cdf_via_sql(client):
        print("\n❌ Failed to enable CDF. Cannot proceed.")
        return False
    
    # Step 2: Create Vector Search index
    if not create_vector_search_index():
        print("\n❌ Failed to create Vector Search index.")
        return False
    
    print("\n" + "=" * 60)
    print("✅ Vector Search Setup Complete!")
    print("=" * 60)
    print("\n📊 Summary:")
    print("   ✅ Change Data Feed enabled on documentation table")
    print("   ✅ Vector Search index created: demo_retail.ecommerce.documentation_index")
    print("\n💡 Next steps:")
    print("   1. Test MCP server: python scripts/check_mcp_servers.py")
    print("   2. Run demo: python demos/01-cli/genie_cli_full.py")
    return True


if __name__ == "__main__":
    success = main()
    sys.exit(0 if success else 1)

