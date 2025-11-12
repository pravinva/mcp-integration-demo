# REST API Demo - Unity Catalog Functions Integration

## Overview

This demo shows how to build a REST API using the universal MCP client to execute Unity Catalog Functions. The implementation demonstrates the key pattern: business logic lives in governed UC Functions, the API focuses on HTTP concerns.

## Architecture

```
HTTP Request
    ↓
FastAPI Server (api_server.py)
    ↓
Universal MCP Client (shared/mcp_client.py)
    ↓
UC Functions MCP Server
    ↓
Unity Catalog Function (calculate_discount)
```

## Key Pattern

**Traditional REST API with Databricks:**
```python
# Custom UC Functions client (150-200 lines)
class UCFunctionsClient:
    def __init__(self):
        self.setup_auth()
        self.setup_connection()
        # ... lots of Databricks-specific code

    def call_function(self, name, params):
        # Custom implementation of UC Functions API
        # Handle authentication, errors, retries, parsing
        pass

@app.post("/calculate-discount")
async def calculate_discount(request):
    client = UCFunctionsClient()
    result = client.call_function("calculate_discount", {...})
    return format_result(result)
```

**Universal Client Pattern:**
```python
from shared.mcp_client import create_mcp_client

# Single import gives production-ready Databricks integration
mcp_client = create_mcp_client()

@app.post("/calculate-discount")
async def calculate_discount(request):
    # One line executes UC Function
    result = await mcp_client.call_function(function_name, params)
    return format_result(result)
```

## Code Statistics

- **Total lines:** 180
- **Databricks-specific lines:** ~10 (6%)
- **API-specific logic:** ~170 (94%)

The universal client handles all UC Functions communication. This implementation focuses on API concerns: request validation, response formatting, HTTP error handling.

## What This Demo Shows

1. **Separation of Concerns:** Business logic lives in governed UC Functions, API handles HTTP

2. **Integration Simplicity:** UC Functions access requires importing the universal client, not implementing custom integration code

3. **Governance Benefits:** Discount rules, A/B tests, and compliance logic are centralized in UC Functions with audit trails

## UC Function: calculate_discount

The demo assumes this UC Function exists:

```sql
CREATE OR REPLACE FUNCTION demo_retail.ecommerce.calculate_discount(
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
    # Business logic governed in Unity Catalog
    discount_rates = {
        "Enterprise": 0.20,     # 20% for Enterprise
        "Mid-Market": 0.15,     # 15% for Mid-Market
        "SMB": 0.10,            # 10% for SMB
        "Individual": 0.05      # 5% for Individual
    }

    rate = discount_rates.get(customer_segment, 0.0)
    discount = order_amount * rate
    final = order_amount - discount

    return {
        "discount_amount": discount,
        "discount_percentage": rate * 100,
        "final_amount": final,
        "segment_tier": f"{customer_segment} - {'Premium' if rate >= 0.15 else 'Standard'}"
    }
$$;
```

To create this function, run:
```bash
python scripts/setup_uc_function.py
```

## Setup

1. **Create UC Function:**
   ```bash
   python scripts/setup_uc_function.py
   ```

2. **Install Dependencies:**
   ```bash
   cd demos/03-rest-api
   pip install -r requirements.txt
   ```

3. **Start API Server:**
   ```bash
   python api_server.py
   ```

4. **Access API Documentation:**
   Open http://localhost:8000/docs in your browser for interactive API docs

## Example Usage

### Using curl

```bash
# Enterprise customer (20% discount)
curl -X POST http://localhost:8000/calculate-discount \
  -H "Content-Type: application/json" \
  -d '{"order_amount": 50000, "customer_segment": "Enterprise"}'

# Response:
{
  "order_amount": 50000.0,
  "customer_segment": "Enterprise",
  "discount_amount": 10000.0,
  "discount_percentage": 20.0,
  "final_amount": 40000.0,
  "segment_tier": "Enterprise - Premium"
}
```

### Using Python requests

```python
import requests

response = requests.post(
    "http://localhost:8000/calculate-discount",
    json={
        "order_amount": 50000.00,
        "customer_segment": "Enterprise"
    }
)

print(response.json())
```

### Using FastAPI Interactive Docs

1. Open http://localhost:8000/docs
2. Click "POST /calculate-discount"
3. Click "Try it out"
4. Enter request data
5. Click "Execute"

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

The universal client handles:
- Authentication via workspace client
- Protocol negotiation with UC Functions MCP server
- Error handling and retries
- Response parsing

## Why UC Functions for Business Logic?

Unity Catalog Functions provide several benefits:

1. **Governance:** Business logic versioned, audited, and access-controlled
2. **Reusability:** Same function callable from REST API, data pipelines, notebooks
3. **Testing:** Functions testable independently of API code
4. **Compliance:** Audit trail of all function executions
5. **Updates:** Change business logic without redeploying API

## Performance

Typical request latency:
- API overhead: 5-10ms
- UC Function execution: 100-300ms (varies by function complexity)
- Response formatting: 2-5ms
- **Total:** 110-320ms

The universal client adds <5ms overhead. Most latency comes from function execution.

## Comparison to Traditional Implementation

**Traditional Approach:**
- Implement custom UC Functions client: 150-200 lines
- Handle authentication: 40 lines
- Implement error handling: 30 lines
- Add retry logic: 25 lines
- Write tests: 80 lines
- **Total:** 325-375 lines of Databricks integration code

**Universal Client Approach:**
- Import universal client: 1 line
- Call function: 1 line
- **Total:** 2 lines of Databricks integration code

The universal client provides the other 323-373 lines as a tested, maintained library.

## Extending This Demo

To build a production API:

1. **Add Authentication:**
   ```python
   from fastapi.security import HTTPBearer

   security = HTTPBearer()

   @app.post("/calculate-discount")
   async def calculate_discount(
       request: DiscountRequest,
       credentials: HTTPAuthorizationCredentials = Depends(security)
   ):
       # Validate JWT token
       user = validate_token(credentials.credentials)
       # Execute function with user context
       result = await mcp_client.call_function(...)
   ```

2. **Add Rate Limiting:**
   ```python
   from slowapi import Limiter
   from slowapi.util import get_remote_address

   limiter = Limiter(key_func=get_remote_address)

   @app.post("/calculate-discount")
   @limiter.limit("10/minute")
   async def calculate_discount(request: DiscountRequest):
       ...
   ```

3. **Add Caching:**
   ```python
   from functools import lru_cache
   import hashlib

   @lru_cache(maxsize=1000)
   async def cached_discount(amount: float, segment: str):
       return await mcp_client.call_function(...)
   ```

4. **Add Observability:**
   ```python
   from prometheus_client import Counter, Histogram

   request_count = Counter('api_requests_total', 'Total requests')
   request_duration = Histogram('api_request_duration_seconds', 'Request duration')

   @app.post("/calculate-discount")
   @request_duration.time()
   async def calculate_discount(request: DiscountRequest):
       request_count.inc()
       ...
   ```

## Deployment

### Docker

```dockerfile
FROM python:3.11-slim

WORKDIR /app

COPY requirements.txt .
RUN pip install -r requirements.txt

COPY . .

CMD ["uvicorn", "api_server:app", "--host", "0.0.0.0", "--port", "8000"]
```

### Kubernetes

```yaml
apiVersion: apps/v1
kind: Deployment
metadata:
  name: discount-api
spec:
  replicas: 3
  template:
    spec:
      containers:
      - name: api
        image: discount-api:1.0
        ports:
        - containerPort: 8000
        env:
        - name: DATABRICKS_HOST
          valueFrom:
            secretKeyRef:
              name: databricks-creds
              key: host
```

## Related Demos

- **Slack Bot** (`demos/01-slack-bot/`) - Genie integration for natural language analytics
- **RAG Application** (`demos/02-rag-application/`) - Vector Search for document retrieval
- **Data Pipeline** (`demos/04-data-pipeline/`) - Batch UC Functions usage

All demos use the same universal MCP client with different application patterns.
