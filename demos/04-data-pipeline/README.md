# Data Pipeline Demo - Batch Unity Catalog Functions Integration

## Overview

This demo shows how to use the universal MCP client in a data pipeline context to execute Unity Catalog Functions for batch transformations. The key insight: the same UC Function used by the REST API is reused here, demonstrating genuine code reuse and consistency.

## Architecture

```
Batch Data
    ↓
Data Pipeline (pipeline_example.py)
    ↓
Universal MCP Client (shared/mcp_client.py)
    ↓
UC Functions MCP Server
    ↓
Unity Catalog Function (calculate_discount) ← Same as REST API uses!
```

## Key Pattern: Code Reuse Across Execution Contexts

**REST API (demos/03-rest-api/):**
```python
# Single record, synchronous context
result = await mcp_client.call_function(
    UC_FUNCTION_NAME,
    {"order_amount": request.order_amount, "customer_segment": request.segment}
)
```

**Data Pipeline (this demo):**
```python
# Batch records, concurrent processing
result = await mcp_client.call_function(
    UC_FUNCTION_NAME,  # Same function!
    {"order_amount": record["amount"], "customer_segment": record["segment"]}
)
```

Both use:
- Same UC Function (business logic not duplicated)
- Same universal client (integration code not duplicated)
- Same governance, audit trails, and access control

## Code Statistics

- **Total lines:** 190
- **Databricks-specific lines:** ~10 (5%)
- **Pipeline-specific logic:** ~180 (95%)

The universal client handles all UC Functions communication. This implementation focuses on pipeline concerns: batch processing, concurrency control, error handling, progress tracking.

## What This Demo Shows

1. **Code Reuse:** UC Function used by REST API is reused in pipeline without modification

2. **Consistency:** Same universal client provides identical integration experience across contexts

3. **Batch Processing:** Demonstrates concurrent execution with semaphore-based concurrency control

4. **Error Handling:** Shows graceful degradation when individual records fail

## Setup

1. **Create UC Function:**
   ```bash
   python scripts/setup_uc_function.py
   ```
   (Same function used by REST API - only needs to be created once)

2. **Install Dependencies:**
   ```bash
   cd demos/04-data-pipeline
   pip install -r requirements.txt
   ```

3. **Run Demo:**
   ```bash
   python pipeline_example.py
   ```

4. **Test Single Record:**
   ```bash
   python pipeline_example.py test
   ```

## Example Output

```
Data Pipeline Demo - Universal MCP Client Pattern

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
```

## Integration Code

The entire Databricks integration consists of:

```python
from shared.mcp_client import create_mcp_client

mcp_client = create_mcp_client()

result = await mcp_client.call_function(
    UC_FUNCTION_NAME,
    {"order_amount": amount, "customer_segment": segment}
)
```

Identical to REST API integration. No batch-specific Databricks code needed.

## Why This Pattern Matters

### Traditional Approach Without UC Functions

**REST API Implementation:**
```python
# api_server.py
def calculate_discount(amount, segment):
    if segment == "Enterprise":
        return amount * 0.20
    elif segment == "Mid-Market":
        return amount * 0.15
    # ... business logic duplicated
```

**Pipeline Implementation:**
```python
# pipeline.py
def calculate_discount(amount, segment):
    if segment == "Enterprise":
        return amount * 0.20
    elif segment == "Mid-Market":
        return amount * 0.15
    # ... business logic DUPLICATED again
```

**Problems:**
- Business logic duplicated across codebases
- Changes require updating both implementations
- Testing requires separate test suites
- No governance or audit trail

### Universal Client + UC Functions

**UC Function (once):**
```sql
CREATE FUNCTION calculate_discount(...)
RETURNS ...
AS $$ ... business logic ... $$;
```

**REST API:**
```python
result = await mcp_client.call_function("calculate_discount", {...})
```

**Pipeline:**
```python
result = await mcp_client.call_function("calculate_discount", {...})
```

**Benefits:**
- Business logic defined once, used everywhere
- Single source of truth for discount calculation
- Unified governance and audit trail
- One test suite validates behavior for all consumers

## Performance Considerations

### Throughput

Demo achieves ~8 records/second with:
- UC Function execution: ~100-300ms per record
- 10 concurrent requests (semaphore limit)

Production optimizations:
- Increase concurrency (adjust semaphore)
- Batch calls (if UC Function supports batch)
- Cache frequently-used results
- Use async/await patterns effectively

### Concurrency Control

```python
semaphore = asyncio.Semaphore(10)  # Limit concurrent requests

async def process_with_semaphore(record):
    async with semaphore:
        return await self.process_record(record)
```

This prevents overwhelming Databricks with simultaneous requests while maintaining high throughput.

## Production Enhancements

### 1. Read from Data Lake

```python
import pandas as pd

# Read from Delta table
df = spark.read.table("bronze.orders")

# Convert to records
records = df.select("order_id", "amount", "segment").collect()
records = [row.asDict() for row in records]

# Process
results = await pipeline.process_batch(records)
```

### 2. Write to Delta Table

```python
from pyspark.sql import SparkSession

def save_results(self, results: List[Dict]):
    spark = SparkSession.builder.getOrCreate()

    # Convert to DataFrame
    df = spark.createDataFrame(results)

    # Write to Delta
    df.write.format("delta") \
        .mode("append") \
        .option("mergeSchema", "true") \
        .saveAsTable("silver.orders_with_discounts")
```

### 3. Add Checkpointing

```python
class DataPipeline:
    def __init__(self, checkpoint_path: str):
        self.mcp_client = create_mcp_client()
        self.checkpoint_path = checkpoint_path

    async def process_batch(self, records):
        # Load checkpoint
        processed_ids = self.load_checkpoint()

        # Filter already-processed records
        records = [r for r in records if r["order_id"] not in processed_ids]

        # Process
        results = []
        for record in records:
            result = await self.process_record(record)
            results.append(result)

            # Checkpoint after each successful record
            self.save_checkpoint(record["order_id"])

        return results
```

### 4. Add Monitoring

```python
from prometheus_client import Counter, Histogram

records_processed = Counter('pipeline_records_processed_total', 'Total records processed')
processing_duration = Histogram('pipeline_record_processing_seconds', 'Record processing duration')

async def process_record(self, record):
    with processing_duration.time():
        result = await mcp_client.call_function(...)
        records_processed.inc()
        return result
```

## Comparison: REST API vs Pipeline

Both use the same UC Function and universal client, but serve different purposes:

| Aspect | REST API | Data Pipeline |
|--------|----------|---------------|
| **Execution** | Single record on demand | Batch processing scheduled |
| **Latency** | Low (100-300ms) | Higher acceptable (batch) |
| **Throughput** | Moderate (requests/sec) | High (records/second) |
| **Concurrency** | Per-request | Controlled batch concurrency |
| **Error Handling** | Return HTTP error | Skip and log errors |
| **Output** | JSON response | Delta table / files |

Despite these differences, **both use identical Databricks integration code** (the universal client).

## Related Demos

- **Slack Bot** (`demos/01-slack-bot/`) - Genie integration for natural language analytics
- **RAG Application** (`demos/02-rag-application/`) - Vector Search for document retrieval
- **REST API** (`demos/03-rest-api/`) - UC Functions for single-record processing

All demos use the same universal MCP client, demonstrating genuine code reuse across diverse application patterns.

## Key Takeaway

The universal client pattern enables:
- **Code reuse:** Same UC Function accessed from REST API and pipeline
- **Consistency:** Identical integration experience across execution contexts
- **Governance:** Unified audit trail for all UC Function executions
- **Simplicity:** Pipeline developers import a client, don't implement Databricks integration

This is the M+N architecture in action: one universal client serves multiple platforms (REST API, pipeline, Slack bot, RAG app) accessing multiple capabilities (Genie, Vector Search, UC Functions).
