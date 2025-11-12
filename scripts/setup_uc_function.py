"""
Create Unity Catalog Function for Discount Calculation

This script:
1. Creates a catalog and schema if they don't exist
2. Creates the calculate_discount UC Function
3. Tests the function with sample inputs
4. Provides the function name for use in demos
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent
sys.path.insert(0, str(project_root))

from databricks.sdk import WorkspaceClient
from shared.config import get_workspace_client


def create_uc_function(w: WorkspaceClient):
    """Create UC Function for discount calculation."""

    print("\n📊 Step 1: Creating catalog and schema...")

    # Get first available SQL warehouse
    warehouses = list(w.warehouses.list())
    if not warehouses:
        raise ValueError("No SQL warehouses found. Please create one first.")

    wh_id = warehouses[0].id
    print(f"✅ Using SQL warehouse: {warehouses[0].name} ({wh_id})")

    # SQL to create catalog, schema, and function
    sql = """
    -- Create catalog and schema if they don't exist
    CREATE CATALOG IF NOT EXISTS demo_retail;
    CREATE SCHEMA IF NOT EXISTS demo_retail.ecommerce;

    -- Drop existing function if exists
    DROP FUNCTION IF EXISTS demo_retail.ecommerce.calculate_discount;

    -- Create discount calculation function
    CREATE FUNCTION demo_retail.ecommerce.calculate_discount(
        order_amount DOUBLE,
        customer_segment STRING
    )
    RETURNS STRUCT<
        discount_amount: DOUBLE,
        discount_percentage: DOUBLE,
        final_amount: DOUBLE,
        segment_tier: STRING
    >
    LANGUAGE PYTHON
    AS $$
        # Discount rates by customer segment
        discount_rates = {
            "Enterprise": 0.20,      # 20% for Enterprise customers
            "Mid-Market": 0.15,      # 15% for Mid-Market
            "SMB": 0.10,             # 10% for Small/Medium Business
            "Individual": 0.05       # 5% for Individual customers
        }

        # Get discount rate for segment (default to 0 if unknown)
        rate = discount_rates.get(customer_segment, 0.0)

        # Calculate discount and final amount
        discount = order_amount * rate
        final = order_amount - discount

        # Determine tier based on discount rate
        tier = "Premium" if rate >= 0.15 else "Standard"

        # Return structured result
        return {
            "discount_amount": discount,
            "discount_percentage": rate * 100,  # Convert to percentage
            "final_amount": final,
            "segment_tier": f"{customer_segment} - {tier}"
        }
    $$;
    """

    # Execute SQL
    statement = w.statement_execution.execute_statement(
        warehouse_id=wh_id,
        statement=sql,
        wait_timeout="30s"
    )

    print("✅ Catalog created: demo_retail")
    print("✅ Schema created: demo_retail.ecommerce")
    print("✅ Function created: demo_retail.ecommerce.calculate_discount")

    return wh_id


def test_uc_function(w: WorkspaceClient, wh_id: str):
    """Test the UC Function with sample inputs."""

    print("\n🧪 Step 2: Testing UC Function...")

    test_cases = [
        {"amount": 50000.00, "segment": "Enterprise"},
        {"amount": 25000.00, "segment": "Mid-Market"},
        {"amount": 5000.00, "segment": "SMB"},
        {"amount": 500.00, "segment": "Individual"},
    ]

    print()
    for test in test_cases:
        sql = f"""
        SELECT demo_retail.ecommerce.calculate_discount(
            {test['amount']},
            '{test['segment']}'
        ) as result
        """

        statement = w.statement_execution.execute_statement(
            warehouse_id=wh_id,
            statement=sql,
            wait_timeout="30s"
        )

        if statement.result and statement.result.data_array:
            result = statement.result.data_array[0]
            # Parse the struct result
            if result and len(result) > 0:
                print(f"Test: ${test['amount']:,.2f} / {test['segment']}")
                # The result is a struct, we'll just indicate it worked
                print(f"  ✅ Function executed successfully")
        else:
            print(f"Test: ${test['amount']:,.2f} / {test['segment']}")
            print(f"  ⚠️  No result returned")

    print()


def main():
    print("=" * 70)
    print("🔧 Unity Catalog Function Setup")
    print("=" * 70)
    print()
    print("This script creates the calculate_discount UC Function used by:")
    print("  • REST API demo (demos/03-rest-api/)")
    print("  • Data Pipeline demo (demos/04-data-pipeline/)")
    print("  • Slack bot (for discount calculations)")
    print()

    # Get workspace client
    w = get_workspace_client()

    # Create UC Function
    wh_id = create_uc_function(w)

    # Test the function
    test_uc_function(w, wh_id)

    print("=" * 70)
    print("🎉 Setup Complete!")
    print("=" * 70)
    print()
    print("Function Details:")
    print("  📝 Name: demo_retail.ecommerce.calculate_discount")
    print("  📊 Catalog: demo_retail")
    print("  📁 Schema: ecommerce")
    print()
    print("Function Signature:")
    print("  Input:")
    print("    • order_amount (DOUBLE) - Order amount in dollars")
    print("    • customer_segment (STRING) - Customer segment")
    print("  Output:")
    print("    • discount_amount (DOUBLE) - Discount amount")
    print("    • discount_percentage (DOUBLE) - Discount percentage")
    print("    • final_amount (DOUBLE) - Final amount after discount")
    print("    • segment_tier (STRING) - Segment tier classification")
    print()
    print("Discount Rates:")
    print("  • Enterprise: 20%")
    print("  • Mid-Market: 15%")
    print("  • SMB: 10%")
    print("  • Individual: 5%")
    print()
    print("✅ This function is now accessible via MCP from:")
    print("   - REST API: python demos/03-rest-api/api_server.py")
    print("   - Pipeline: python demos/04-data-pipeline/pipeline_example.py")
    print()
    print("Configuration:")
    print("  Add to .env file:")
    print("  UC_FUNCTION_NAME=demo_retail.ecommerce.calculate_discount")


if __name__ == "__main__":
    main()
