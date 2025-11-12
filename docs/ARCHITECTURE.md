# Architecture - Universal MCP Client Pattern

## Table of Contents

1. [Overview](#overview)
2. [Design Philosophy](#design-philosophy)
3. [Architecture Diagram](#architecture-diagram)
4. [Universal Client Design](#universal-client-design)
5. [Platform Adapter Pattern](#platform-adapter-pattern)
6. [Authentication & Security](#authentication--security)
7. [Error Handling & Retry Logic](#error-handling--retry-logic)
8. [Protocol Negotiation](#protocol-negotiation)
9. [Comparison: Traditional vs Universal Client](#comparison-traditional-vs-universal-client)
10. [Design Trade-offs](#design-trade-offs)
11. [Performance Considerations](#performance-considerations)
12. [Future Extensions](#future-extensions)

## Overview

This repository demonstrates the **universal client pattern** for Databricks Model Context Protocol (MCP) integration. The pattern centralizes all Databricks communication in a single, reusable client while platform implementations focus exclusively on their application-specific concerns.

### Key Insight

Instead of each platform implementing its own Databricks integration logic, we implement **one universal client** that handles:
- Authentication
- Protocol negotiation
- Error handling
- Retry logic
- Response parsing
- Logging

Platform implementations become **thin adapters** focused on:
- Platform-specific UI/API patterns
- Application business logic
- User interaction handling

## Design Philosophy

### Separation of Concerns

```
┌─────────────────────────────────────────────────────┐
│           What Changes Frequently                    │
│  • UI frameworks (Slack SDK updates)                 │
│  • Business logic (new features)                     │
│  • Platform APIs (FastAPI versions)                  │
│                                                       │
│  These belong in PLATFORM ADAPTERS                   │
└─────────────────────────────────────────────────────┘

┌─────────────────────────────────────────────────────┐
│           What Changes Infrequently                  │
│  • Databricks authentication                         │
│  • MCP protocol communication                        │
│  • Error handling patterns                           │
│                                                       │
│  These belong in UNIVERSAL CLIENT                    │
└─────────────────────────────────────────────────────┘
```

### Single Responsibility Principle

**Universal Client Responsibility:**
- "How do I communicate with Databricks MCP?"
- Authentication, protocol, retries, parsing

**Platform Adapter Responsibility:**
- "How do I serve my users?"
- UI, routing, business logic, platform-specific patterns

## Architecture Diagram

```
┌─────────────────────────────────────────────────────────────────┐
│                    Application Layer                             │
│                                                                   │
│  ┌──────────────┐  ┌──────────────┐  ┌──────────────┐          │
│  │  Slack Bot   │  │  RAG App     │  │  REST API    │          │
│  │              │  │              │  │              │          │
│  │  • Socket    │  │  • Async     │  │  • FastAPI   │          │
│  │    Mode      │  │    Python    │  │  • HTTP      │          │
│  │  • Slack UI  │  │  • Document  │  │  • JSON      │          │
│  │  • Events    │  │    Retrieval │  │  • Endpoints │          │
│  │              │  │              │  │              │          │
│  │ 350 lines    │  │ 280 lines    │  │ 220 lines    │          │
│  └──────┬───────┘  └──────┬───────┘  └──────┬───────┘          │
└─────────┼──────────────────┼──────────────────┼─────────────────┘
          │                  │                  │
          │  import          │  import          │  import
          │  create_mcp_     │  create_mcp_     │  create_mcp_
          │  client()        │  client()        │  client()
          │                  │                  │
          └──────────────────┴──────────────────┘
                             │
┌────────────────────────────┴──────────────────────────────────────┐
│              Universal MCP Client (329 lines)                      │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  Core Capabilities                                           │ │
│  │  • ask_genie(space_id, question)                            │ │
│  │  • search_docs(index_id, query, num_results)                │ │
│  │  • call_function(function_name, parameters)                 │ │
│  └──────────────────────────────────────────────────────────────┘ │
│                                                                    │
│  ┌──────────────────────────────────────────────────────────────┐ │
│  │  Cross-Cutting Concerns                                      │ │
│  │  • Authentication (Databricks CLI/Token/OAuth)              │ │
│  │  • Protocol Negotiation (MCP handshake)                     │ │
│  │  • Error Handling (retries, timeouts, parsing)              │ │
│  │  • Response Parsing (unified format)                        │ │
│  │  • Logging & Observability                                  │ │
│  └──────────────────────────────────────────────────────────────┘ │
└────────────────────────────────────────────────────────────────────┘
                             │
         ┌───────────────────┼───────────────────┐
         │                   │                   │
         ▼                   ▼                   ▼
┌────────────────┐  ┌────────────────┐  ┌────────────────┐
│  Genie MCP     │  │ Vector Search  │  │ UC Functions   │
│  Server        │  │ MCP Server     │  │ MCP Server     │
│                │  │                │  │                │
│ • Natural      │  │ • Semantic     │  │ • Governed     │
│   Language     │  │   Search       │  │   Business     │
│   Analytics    │  │ • Document     │  │   Logic        │
│                │  │   Retrieval    │  │                │
└────────────────┘  └────────────────┘  └────────────────┘
```

## Universal Client Design

### Interface

The universal client exposes a clean, capability-based interface:

```python
from shared.mcp_client import create_mcp_client

# Single client handles all Databricks capabilities
mcp_client = create_mcp_client()

# Genie: Natural language analytics
response = await mcp_client.ask_genie(
    space_id="genie_space_123",
    question="What were sales last quarter?"
)

# Vector Search: Document retrieval
docs = await mcp_client.search_docs(
    index_id="main.docs.technical_index",
    query="databricks authentication",
    num_results=5
)

# UC Functions: Governed business logic
result = await mcp_client.call_function(
    function_name="demo_retail.ecommerce.calculate_discount",
    parameters={"order_amount": 50000.0, "customer_segment": "Enterprise"}
)
```

### Internal Structure

```
shared/mcp_client.py (329 lines)
├── create_mcp_client()              # Factory function
├── UniversalMCPClient               # Main client class
│   ├── __init__()                   # Initialize with config
│   ├── _authenticate()              # Handle auth (CLI/Token/OAuth)
│   ├── _connect()                   # Establish MCP connection
│   ├── ask_genie()                  # Genie capability
│   ├── search_docs()                # Vector Search capability
│   ├── call_function()              # UC Functions capability
│   ├── _execute_with_retry()        # Retry logic
│   ├── _handle_error()              # Error handling
│   └── _parse_response()            # Response parsing
└── Configuration                     # Settings management
```

### Key Design Decisions

**1. Async/Await Native**

The client is built with async/await from the ground up:

```python
class UniversalMCPClient:
    async def ask_genie(self, space_id: str, question: str) -> str:
        """Async by default - works in any async context."""
        response = await self._execute_with_retry(...)
        return self._parse_response(response)
```

**Why:** All MCP operations are I/O-bound. Async patterns enable:
- Concurrent requests in batch processing
- Non-blocking operations in web servers
- Natural fit with modern Python frameworks

**2. Capability-Based Methods**

Rather than exposing low-level MCP protocol:

```python
# ❌ Low-level (bad)
response = await client.call_tool("genie_ask", {"space": "...", "q": "..."})

# ✅ Capability-based (good)
response = await client.ask_genie(space_id="...", question="...")
```

**Why:**
- Type hints and IDE autocomplete
- Self-documenting interface
- Abstraction shields from protocol changes

**3. Centralized Error Handling**

All errors flow through unified handling:

```python
async def _execute_with_retry(self, operation, max_retries=3):
    for attempt in range(max_retries):
        try:
            return await operation()
        except MCPConnectionError:
            # Retry with exponential backoff
            await asyncio.sleep(2 ** attempt)
        except MCPAuthError:
            # Don't retry auth errors
            raise
        except Exception as e:
            # Log and handle unexpected errors
            self._handle_error(e)
```

**Why:**
- Consistent retry behavior across all operations
- Single place to add observability
- Platform adapters don't reimplement retry logic

**4. Configuration from Environment**

Client reads configuration from standard locations:

```python
def create_mcp_client():
    config = {
        "host": os.getenv("DATABRICKS_HOST"),
        "token": os.getenv("DATABRICKS_TOKEN"),
        # Or use Databricks CLI profile
        "profile": os.getenv("DATABRICKS_CONFIG_PROFILE", "DEFAULT")
    }
    return UniversalMCPClient(config)
```

**Why:**
- Works with existing Databricks authentication
- No custom credential management
- Secure by default (no hardcoded credentials)

## Platform Adapter Pattern

### Structure

Each platform implementation follows this structure:

```
demos/XX-platform-name/
├── platform_specific.py       # Main application logic
├── README.md                  # Platform-specific docs
├── requirements.txt           # Platform dependencies
└── .env.example              # Configuration template
```

### Example: REST API Adapter

```python
# demos/03-rest-api/api_server.py

from fastapi import FastAPI, HTTPException
from shared.mcp_client import create_mcp_client

app = FastAPI()

# Universal client initialized once at startup
mcp_client = create_mcp_client()

@app.post("/calculate-discount")
async def calculate_discount(request: DiscountRequest):
    """
    REST API concerns:
    - HTTP routing and request validation
    - JSON serialization
    - Error response formatting
    """
    try:
        # Single line for Databricks integration
        result = await mcp_client.call_function(
            "demo_retail.ecommerce.calculate_discount",
            {"order_amount": request.amount, "customer_segment": request.segment}
        )
        return parse_and_format(result)
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))
```

**Notice:**
- 220 total lines in this file
- Only ~10 lines are Databricks-specific (5%)
- 95% is FastAPI routing, validation, error handling
- Business logic lives in UC Function (not duplicated here)

### Example: Data Pipeline Adapter

```python
# demos/04-data-pipeline/pipeline_example.py

import asyncio
from shared.mcp_client import create_mcp_client

class DataPipeline:
    def __init__(self):
        self.mcp_client = create_mcp_client()

    async def process_batch(self, records):
        """
        Pipeline concerns:
        - Batch processing
        - Concurrency control
        - Progress tracking
        - Error handling for individual records
        """
        semaphore = asyncio.Semaphore(10)  # Limit concurrent requests

        async def process_with_semaphore(record):
            async with semaphore:
                return await self.process_record(record)

        # Process all records concurrently
        results = await asyncio.gather(
            *[process_with_semaphore(r) for r in records]
        )
        return results

    async def process_record(self, record):
        # Same UC Function as REST API uses (code reuse!)
        result = await self.mcp_client.call_function(
            "demo_retail.ecommerce.calculate_discount",
            {"order_amount": record["amount"], "customer_segment": record["segment"]}
        )
        return self._parse_result(result)
```

**Notice:**
- 190 total lines
- Only ~10 lines are Databricks-specific (5%)
- 95% is batch processing, concurrency, error handling
- Uses same UC Function as REST API (no duplication)

## Authentication & Security

### Supported Authentication Methods

The universal client supports all standard Databricks authentication:

**1. Databricks CLI Profile (Recommended)**

```bash
databricks configure --token
# Enter host and token when prompted

# Client automatically uses default profile
mcp_client = create_mcp_client()
```

**2. Environment Variables**

```bash
export DATABRICKS_HOST="https://your-workspace.databricks.com"
export DATABRICKS_TOKEN="dapi..."

# Client reads from environment
mcp_client = create_mcp_client()
```

**3. Explicit Configuration**

```python
mcp_client = create_mcp_client(
    host="https://your-workspace.databricks.com",
    token="dapi..."
)
```

### Security Best Practices

**1. Never Hardcode Credentials**

```python
# ❌ NEVER do this
token = "dapi1234567890abcdef"

# ✅ Use environment or CLI profile
token = os.getenv("DATABRICKS_TOKEN")
```

**2. Use Service Principals in Production**

```bash
# Create service principal
databricks service-principals create --display-name "mcp-client-prod"

# Generate token for service principal
databricks tokens create --lifetime-seconds 31536000 --comment "Production MCP"

# Store securely (AWS Secrets Manager, Azure Key Vault, etc.)
```

**3. Rotate Tokens Regularly**

The universal client handles token refresh transparently:

```python
class UniversalMCPClient:
    async def _authenticate(self):
        # Check token expiry
        if self._token_expired():
            # Automatically refresh
            self.token = await self._refresh_token()
```

## Error Handling & Retry Logic

### Error Categories

The universal client distinguishes between:

**1. Transient Errors (Retryable)**
- Network timeouts
- Rate limiting (429)
- Temporary service unavailability (503)

**2. Permanent Errors (Not Retryable)**
- Authentication failures (401, 403)
- Resource not found (404)
- Invalid parameters (400)

### Retry Strategy

```python
async def _execute_with_retry(self, operation, max_retries=3):
    """Exponential backoff with jitter."""
    for attempt in range(max_retries):
        try:
            return await operation()
        except TransientError as e:
            if attempt == max_retries - 1:
                raise
            # Exponential backoff: 1s, 2s, 4s
            delay = (2 ** attempt) + random.uniform(0, 1)
            await asyncio.sleep(delay)
        except PermanentError:
            # Don't retry permanent errors
            raise
```

### Error Context

Errors include rich context for debugging:

```python
try:
    result = await mcp_client.call_function("invalid.function", {})
except MCPError as e:
    print(e.message)        # "Function 'invalid.function' not found"
    print(e.error_code)     # "FUNCTION_NOT_FOUND"
    print(e.request_id)     # "req-123456"
    print(e.workspace)      # "https://workspace.databricks.com"
```

## Protocol Negotiation

### MCP Handshake

The universal client handles MCP protocol negotiation:

```
1. Client → Server: Initialize
   {
     "protocol_version": "2024-11-05",
     "capabilities": ["tools"],
     "client_info": {"name": "universal-mcp-client", "version": "1.0.0"}
   }

2. Server → Client: Initialized
   {
     "protocol_version": "2024-11-05",
     "capabilities": ["tools"],
     "server_info": {"name": "databricks-genie-mcp", "version": "1.2.0"}
   }

3. Client → Server: List Tools
   {
     "method": "tools/list"
   }

4. Server → Client: Available Tools
   {
     "tools": [
       {"name": "ask", "description": "Ask Genie a question", ...},
       {"name": "create_space", ...}
     ]
   }
```

### Version Compatibility

The client negotiates compatible protocol versions:

```python
class UniversalMCPClient:
    SUPPORTED_VERSIONS = ["2024-11-05", "2024-10-01"]

    async def _negotiate_version(self, server_versions):
        # Find highest compatible version
        for version in self.SUPPORTED_VERSIONS:
            if version in server_versions:
                return version
        raise IncompatibleVersionError()
```

## Comparison: Traditional vs Universal Client

### Traditional Approach: M × N Integrations

```
Slack Bot Implementation (Scenario A):
├── slack_bot.py (800 lines)
│   ├── Slack SDK integration (200 lines)
│   ├── Databricks authentication (100 lines)
│   ├── Genie MCP integration (150 lines)
│   ├── Error handling & retries (100 lines)
│   ├── Response parsing (80 lines)
│   └── Business logic (170 lines)

REST API Implementation (Scenario B):
├── api_server.py (750 lines)
│   ├── FastAPI setup (150 lines)
│   ├── Databricks authentication (100 lines)  ← Duplicated
│   ├── UC Functions MCP integration (180 lines)
│   ├── Error handling & retries (100 lines)   ← Duplicated
│   ├── Response parsing (70 lines)            ← Duplicated
│   └── Business logic (150 lines)

Data Pipeline Implementation (Scenario C):
├── pipeline.py (900 lines)
│   ├── Batch processing (250 lines)
│   ├── Databricks authentication (100 lines)  ← Duplicated
│   ├── UC Functions MCP integration (180 lines) ← Duplicated
│   ├── Error handling & retries (120 lines)   ← Duplicated
│   ├── Response parsing (70 lines)            ← Duplicated
│   ├── Business logic in Python (180 lines)   ← Duplicated with REST API
```

**Total: 2,450 lines**
**Duplicated integration code: ~1,000 lines (41%)**

### Universal Client Approach: M + N Architecture

```
Universal Client (shared/):
└── mcp_client.py (329 lines)
    ├── Authentication (60 lines)
    ├── Protocol negotiation (40 lines)
    ├── Error handling & retries (80 lines)
    ├── Response parsing (50 lines)
    ├── Genie integration (30 lines)
    ├── Vector Search integration (30 lines)
    └── UC Functions integration (39 lines)

Slack Bot (demos/01-slack-bot/):
└── slack_bot.py (350 lines)
    ├── Slack SDK integration (200 lines)
    ├── Import mcp_client (1 line)
    └── Business logic (149 lines)

REST API (demos/03-rest-api/):
└── api_server.py (220 lines)
    ├── FastAPI setup (150 lines)
    ├── Import mcp_client (1 line)
    └── Business logic (69 lines)

Data Pipeline (demos/04-data-pipeline/):
└── pipeline.py (190 lines)
    ├── Batch processing (130 lines)
    ├── Import mcp_client (1 line)
    └── Business logic (59 lines)

UC Function (Unity Catalog):
└── calculate_discount (SQL function)
    └── Business logic (40 lines) ← Used by both REST API and Pipeline
```

**Total: 1,089 lines**
**Shared integration code: 329 lines (reused 3×)**
**No duplicated integration logic**

### Maintenance Scenarios

**Scenario: Databricks Updates MCP Protocol**

Traditional Approach:
1. Update Slack bot authentication (2 hours)
2. Update REST API authentication (2 hours)
3. Update Pipeline authentication (2 hours)
4. Test all three (3 hours)
**Total: 9 hours**

Universal Client Approach:
1. Update universal client authentication (2 hours)
2. Test with all platforms (2 hours)
**Total: 4 hours (56% reduction)**

**Scenario: Add New Platform (Mobile App)**

Traditional Approach:
1. Research Databricks integration (4 hours)
2. Implement authentication (4 hours)
3. Implement MCP communication (6 hours)
4. Implement error handling (4 hours)
5. Implement business logic (8 hours)
**Total: 26 hours**

Universal Client Approach:
1. Import universal client (5 minutes)
2. Implement platform UI (6 hours)
3. Implement business logic (6 hours)
**Total: 12 hours (54% reduction)**

## Design Trade-offs

### Upfront Cost vs Long-Term Benefit

**Upfront:**
- Universal client adds 329 lines initially
- ~7% more code than most direct integration for single platform

**Long-term:**
- 40-50% reduction in maintenance effort (API updates)
- 50-60% faster development of new platforms
- Elimination of duplicated integration logic

**Break-even:** Adding 2nd platform

### Abstraction vs Control

**Universal Client:**
- ✅ Consistent interface across all platforms
- ✅ Single place to add observability, caching, etc.
- ❌ Abstraction may hide some protocol details

**Direct Integration:**
- ✅ Full control over every protocol detail
- ❌ Inconsistent patterns across platforms
- ❌ Repeated implementation of cross-cutting concerns

**Decision:** Abstraction wins for enterprise context with multiple platforms and teams.

### Flexibility vs Standardization

**Universal Client:**
- ✅ Enforces consistent authentication, error handling
- ✅ Easy to add organization-wide policies (rate limiting, audit logging)
- ❌ Less flexibility for one-off custom integrations

**Custom Per-Platform:**
- ✅ Each platform can implement exactly what it needs
- ❌ Divergent patterns make system harder to reason about
- ❌ Organizational policies applied inconsistently

**Decision:** Standardization preferred for maintainability and governance.

## Performance Considerations

### Connection Pooling

The universal client reuses connections:

```python
class UniversalMCPClient:
    def __init__(self):
        self._connection_pool = ConnectionPool(max_size=10)

    async def ask_genie(self, space_id, question):
        async with self._connection_pool.get() as conn:
            return await conn.execute(...)
```

**Benefit:** Avoid connection overhead (~50-100ms) per request

### Concurrent Requests

All methods are async-native for concurrency:

```python
# Process 100 records concurrently
results = await asyncio.gather(*[
    mcp_client.call_function("discount", {"amount": r.amount})
    for r in records
])
```

**Benchmark:** Data Pipeline demo processes 8-10 records/second with 10 concurrent requests.

### Response Caching

Optional caching for read-heavy workloads:

```python
mcp_client = create_mcp_client(
    enable_cache=True,
    cache_ttl=300  # 5 minutes
)

# First call: hits Databricks
docs = await mcp_client.search_docs(index, query)

# Second call (within 5 min): served from cache
docs = await mcp_client.search_docs(index, query)
```

### Resource Usage

| Component | Memory | CPU | Network |
|-----------|--------|-----|---------|
| Universal Client | ~5 MB | Minimal | Per-request |
| Connection Pool | ~2 MB per connection | None | Persistent |
| Response Cache | Configurable (default: 50 MB) | Minimal | Reduced |

## Future Extensions

### 1. Observability Integration

Add OpenTelemetry tracing:

```python
from opentelemetry import trace

class UniversalMCPClient:
    async def ask_genie(self, space_id, question):
        with trace.get_tracer(__name__).start_as_current_span("ask_genie"):
            span = trace.get_current_span()
            span.set_attribute("space_id", space_id)
            span.set_attribute("question_length", len(question))
            result = await self._execute(...)
            span.set_attribute("response_length", len(result))
            return result
```

### 2. Rate Limiting

Add client-side rate limiting:

```python
from aiolimiter import AsyncLimiter

class UniversalMCPClient:
    def __init__(self):
        # Limit to 100 requests per minute
        self._rate_limiter = AsyncLimiter(100, 60)

    async def call_function(self, name, params):
        async with self._rate_limiter:
            return await self._execute(...)
```

### 3. Circuit Breaker

Add circuit breaker for fault tolerance:

```python
from pycircuitbreaker import CircuitBreaker

class UniversalMCPClient:
    def __init__(self):
        self._circuit_breaker = CircuitBreaker(
            fail_max=5,
            timeout_duration=60
        )

    @circuit_breaker
    async def call_function(self, name, params):
        return await self._execute(...)
```

### 4. Metrics & Monitoring

Expose Prometheus metrics:

```python
from prometheus_client import Counter, Histogram

requests_total = Counter('mcp_requests_total', 'Total MCP requests', ['capability'])
request_duration = Histogram('mcp_request_duration_seconds', 'Request duration')

class UniversalMCPClient:
    async def ask_genie(self, space_id, question):
        requests_total.labels(capability='genie').inc()
        with request_duration.time():
            return await self._execute(...)
```

### 5. Additional Capabilities

As Databricks adds MCP servers, extend the client:

```python
class UniversalMCPClient:
    # Existing capabilities
    async def ask_genie(self, ...): ...
    async def search_docs(self, ...): ...
    async def call_function(self, ...): ...

    # Future capabilities
    async def query_delta_table(self, table: str, filters: Dict): ...
    async def run_notebook(self, path: str, params: Dict): ...
    async def schedule_job(self, job_config: Dict): ...
```

## Conclusion

The universal client pattern provides:

1. **Consistency:** All platforms use identical Databricks integration
2. **Maintainability:** Single codebase for all MCP communication
3. **Velocity:** New platforms integrate in hours, not days
4. **Quality:** Centralized testing and error handling
5. **Governance:** Unified observability and policy enforcement

While it requires modest upfront investment (~7% more initial code), the pattern delivers significant long-term benefits in maintenance efficiency (40-50% reduction) and development velocity (50-60% faster new platforms).

This is the M+N architecture: one universal client + N platform adapters, rather than M×N custom integrations.
