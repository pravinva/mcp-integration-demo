"""
Data Pipeline Demo - Batch Unity Catalog Functions Integration

This demonstrates using the universal MCP client in a data pipeline context
to execute Unity Catalog Functions for batch transformations. The pattern shows
how UC Functions provide reusable, governed transformation logic while the
universal client handles all Databricks communication.

Key Pattern: Same universal client, different execution context (batch vs API).
"""

import asyncio
import sys
from pathlib import Path
from typing import List, Dict
import time

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from shared.mcp_client import create_mcp_client
from shared.config import UC_FUNCTION_NAME


class DataPipeline:
    """
    Minimal data pipeline demonstrating UC Functions integration.

    This shows the universal client pattern in batch processing context:
    - Same UC Function as REST API uses (code reuse!)
    - Same universal client (consistency!)
    - Different execution pattern (batch vs single)
    """

    def __init__(self):
        # Universal MCP client - handles ALL Databricks communication
        self.mcp_client = create_mcp_client()
        print("✅ Data Pipeline initialized with universal MCP client")

    async def process_record(self, record: Dict) -> Dict:
        """
        Process a single record using UC Function.

        Notice: Identical integration code as REST API uses.
        The UC Function encapsulates transformation logic.
        """
        # Call UC Function (same as REST API calls it)
        result = await self.mcp_client.call_function(
            UC_FUNCTION_NAME,
            {
                "order_amount": record["amount"],
                "customer_segment": record["segment"]
            }
        )

        # Parse result
        import json
        data = json.loads(result)

        # Extract values from UC Function response
        if "rows" in data and len(data["rows"]) > 0:
            first_row = data["rows"][0]
            if isinstance(first_row, list) and len(first_row) > 0:
                result_obj = first_row[0]
                if isinstance(result_obj, dict):
                    schema = result_obj.get("schema", [])
                    values = result_obj.get("values", [])

                    # Build transformed record
                    transformed = {
                        "order_id": record["order_id"],
                        "original_amount": record["amount"],
                        "customer_segment": record["segment"],
                    }

                    # Add UC Function outputs
                    for i, field_def in enumerate(schema):
                        field_name = field_def.get("name", f"field_{i}")
                        if i < len(values):
                            transformed[field_name] = values[i]

                    return transformed

        raise ValueError("Unexpected UC Function response")

    async def process_batch(self, records: List[Dict]) -> List[Dict]:
        """
        Process batch of records using UC Function.

        This demonstrates batch processing pattern:
        - Process records concurrently (within limits)
        - Handle errors gracefully
        - Track progress
        """
        print(f"\n🔄 Processing batch of {len(records)} records...")

        start_time = time.time()
        results = []
        errors = 0

        # Process records concurrently (with semaphore to limit concurrency)
        semaphore = asyncio.Semaphore(10)  # Limit to 10 concurrent requests

        async def process_with_semaphore(record):
            async with semaphore:
                try:
                    return await self.process_record(record)
                except Exception as e:
                    print(f"   ⚠️  Error processing record {record['order_id']}: {e}")
                    return None

        # Execute all transformations concurrently
        results = await asyncio.gather(
            *[process_with_semaphore(record) for record in records]
        )

        # Filter out errors
        results = [r for r in results if r is not None]
        errors = len(records) - len(results)

        elapsed = time.time() - start_time

        print(f"✅ Batch processing complete:")
        print(f"   • Processed: {len(results)} records")
        print(f"   • Errors: {errors} records")
        print(f"   • Duration: {elapsed:.2f}s")
        print(f"   • Throughput: {len(results)/elapsed:.1f} records/second")

        return results

    def save_results(self, results: List[Dict], output_path: str):
        """Save transformed results (simulated)."""
        import json

        print(f"\n💾 Saving {len(results)} transformed records...")
        print(f"   Output path: {output_path}")

        # In production, this would write to:
        # - Delta table
        # - Parquet files
        # - Data warehouse
        # - Message queue

        # For demo, just show first few records
        print(f"\n📊 Sample transformed records:")
        for i, record in enumerate(results[:3], 1):
            print(f"   {i}. Order {record['order_id']}: "
                  f"${record['original_amount']:,.2f} → "
                  f"${record.get('final_amount', 0):,.2f} "
                  f"({record.get('discount_percentage', 0)}% discount)")

        print(f"   ... and {len(results) - 3} more records")


async def run_pipeline_demo():
    """Run data pipeline demo with sample data."""
    print("=" * 70)
    print("Data Pipeline Demo - Universal MCP Client Pattern")
    print("=" * 70)
    print()
    print("This demo shows batch processing with UC Functions via the")
    print("universal MCP client. Notice:")
    print("  • Same UC Function as REST API uses (code reuse)")
    print("  • Same universal client (consistency)")
    print("  • Different execution pattern (batch vs single)")
    print()

    # Initialize pipeline
    pipeline = DataPipeline()

    # Sample data (simulates reading from data lake, database, etc.)
    sample_records = [
        {"order_id": "ORD-001", "amount": 50000.00, "segment": "Enterprise"},
        {"order_id": "ORD-002", "amount": 25000.00, "segment": "Mid-Market"},
        {"order_id": "ORD-003", "amount": 75000.00, "segment": "Enterprise"},
        {"order_id": "ORD-004", "amount": 5000.00, "segment": "SMB"},
        {"order_id": "ORD-005", "amount": 500.00, "segment": "Individual"},
        {"order_id": "ORD-006", "amount": 15000.00, "segment": "Mid-Market"},
        {"order_id": "ORD-007", "amount": 100000.00, "segment": "Enterprise"},
        {"order_id": "ORD-008", "amount": 2500.00, "segment": "SMB"},
        {"order_id": "ORD-009", "amount": 35000.00, "segment": "Mid-Market"},
        {"order_id": "ORD-010", "amount": 800.00, "segment": "Individual"},
    ]

    print(f"📥 Input: {len(sample_records)} orders to process")

    # Process batch
    transformed_records = await pipeline.process_batch(sample_records)

    # Save results
    pipeline.save_results(transformed_records, "s3://bucket/transformed/")

    print()
    print("=" * 70)
    print("Demo Complete")
    print("=" * 70)
    print()
    print("Key Takeaways:")
    print("  • Universal MCP client works in batch context")
    print("  • UC Function reused from REST API (no duplicate logic)")
    print("  • Batch processing with concurrency control")
    print("  • Same governance, audit trail, and access control")


async def single_record_demo():
    """Process a single record (useful for testing)."""
    pipeline = DataPipeline()

    test_record = {
        "order_id": "TEST-001",
        "amount": 50000.00,
        "segment": "Enterprise"
    }

    print(f"Processing test record: {test_record}")
    result = await pipeline.process_record(test_record)
    print(f"Result: {result}")


if __name__ == "__main__":
    if len(sys.argv) > 1 and sys.argv[1] == "test":
        # Test mode: process single record
        asyncio.run(single_record_demo())
    else:
        # Demo mode: process batch
        asyncio.run(run_pipeline_demo())
