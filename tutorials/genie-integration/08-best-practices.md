# Best Practices

Production-ready practices for Genie MCP integrations.

## Security

### Credential Management

**Recommended Practices:**
- Store credentials in environment variables
- Use `.env` file for local development only
- Add `.env` to `.gitignore` to prevent credential exposure
- Use Azure Key Vault or similar secure storage for production
- Implement regular token rotation schedules

**Avoid:**
- Committing credentials to version control
- Hardcoding tokens directly in application code
- Sharing tokens through messaging or email
- Using identical tokens across development, staging, and production environments

**Example:**
```python
# Recommended approach
import os
token = os.getenv("DATABRICKS_TOKEN")

# Avoid this approach
token = "dapi1234567890abcdef"
```

### Authentication

**Recommended Practices:**
- Use OAuth 2.0 for production environments
- Implement token refresh mechanisms
- Validate tokens before use
- Use service principals for automation and deployments

**Avoid:**
- Personal Access Tokens in production systems
- Storing tokens in plain text
- Sharing credentials across different environments

### Input Validation

**Recommended Practices:**
- Validate all user input
- Sanitize query strings to prevent injection attacks
- Limit query length to prevent resource exhaustion
- Implement checks for SQL injection attempts

**Example:**
```python
def validate_query(query: str) -> bool:
    if len(query) > 1000:
        return False
    # Add additional validation logic
    return True
```

## Error Handling

### Graceful Degradation

**Recommended Practices:**
- Catch and handle all exceptions appropriately
- Provide clear, user-friendly error messages
- Log errors with sufficient context for debugging
- Implement retry logic for transient failures

**Example:**
```python
try:
    response = await mcp_client.ask_genie(space_id, question)
except Exception as e:
    logger.error(f"Genie query failed: {e}", exc_info=True)
    await say("Sorry, I encountered an error. Please try again.")
```

### Retry Logic

**Recommended Practices:**
- Implement exponential backoff for retries
- Distinguish between transient and permanent errors
- Set reasonable maximum retry attempts
- Log all retry attempts for troubleshooting

**Example:**
```python
import asyncio
from tenacity import retry, stop_after_attempt, wait_exponential

@retry(
    stop=stop_after_attempt(3),
    wait=wait_exponential(multiplier=1, min=2, max=10)
)
async def query_with_retry(space_id, question):
    return await mcp_client.ask_genie(space_id, question)
```

## Performance

### Caching

**Recommended Practices:**
- Cache results from frequent queries
- Implement TTL (time-to-live) for cached entries
- Invalidate cache when underlying data updates

**Example:**
```python
from functools import lru_cache
from datetime import datetime, timedelta

cache = {}
CACHE_TTL = timedelta(minutes=5)

def get_cached_response(question: str):
    if question in cache:
        response, timestamp = cache[question]
        if datetime.now() - timestamp < CACHE_TTL:
            return response
    return None
```

### Async Operations

**Recommended Practices:**
- Properly implement async/await patterns
- Avoid blocking operations in async contexts
- Use connection pooling for efficiency
- Process requests concurrently

**Example:**
```python
# Recommended - async/await
async def handle_message(message):
    response = await mcp_client.ask_genie(space_id, message)
    return response

# Avoid - blocking call
def handle_message(message):
    response = mcp_client.ask_genie(space_id, message)  # Blocking!
    return response
```

### Timeouts

**Recommended Practices:**
- Set timeouts for all network requests
- Handle timeout errors appropriately
- Provide user feedback for long-running queries

**Example:**
```python
import asyncio

try:
    response = await asyncio.wait_for(
        mcp_client.ask_genie(space_id, question),
        timeout=30.0
    )
except asyncio.TimeoutError:
    await say("Query is taking longer than expected. Please try again.")
```

## Conversation Management

### Context Storage

**Recommended Practices:**
- Maintain conversation IDs per user/thread
- Limit conversation history to prevent memory growth
- Clean up stale conversations regularly
- Use persistent storage in production environments

**Example:**
```python
# Development (in-memory)
conversations = {}

# Production (persistent storage)
import redis
redis_client = redis.Redis()

def get_conversation_id(user_id):
    return redis_client.get(f"conv:{user_id}")

def set_conversation_id(user_id, conv_id):
    redis_client.setex(f"conv:{user_id}", 3600, conv_id)  # 1 hour TTL
```

### Rate Limiting

**Recommended Practices:**
- Implement rate limiting on a per-user basis
- Prevent abuse and resource exhaustion
- Return clear error messages when limits are exceeded

**Example:**
```python
from collections import defaultdict
from datetime import datetime, timedelta

user_requests = defaultdict(list)
RATE_LIMIT = 10  # requests per minute

def check_rate_limit(user_id):
    now = datetime.now()
    user_requests[user_id] = [
        req_time for req_time in user_requests[user_id]
        if now - req_time < timedelta(minutes=1)
    ]
    return len(user_requests[user_id]) < RATE_LIMIT
```

## Logging and Monitoring

### Structured Logging

**Recommended Practices:**
- Implement structured logging with context information
- Include relevant details (user_id, query, timestamp, etc.)
- Use appropriate log levels (DEBUG, INFO, WARNING, ERROR)
- Use log aggregation tools for centralized analysis

**Example:**
```python
import logging
import json

logger = logging.getLogger(__name__)

logger.info("Genie query", extra={
    "user_id": user_id,
    "question": question,
    "space_id": space_id,
    "response_time_ms": response_time
})
```

### Monitoring

**Recommended Practices:**
- Monitor error rates and error types
- Track query response times
- Monitor MCP connection availability
- Configure alerts for anomalies

**Example:**
```python
from prometheus_client import Counter, Histogram

query_counter = Counter('genie_queries_total', 'Total Genie queries')
query_duration = Histogram('genie_query_duration_seconds', 'Genie query duration')

@query_duration.time()
async def query_genie(space_id, question):
    query_counter.inc()
    return await mcp_client.ask_genie(space_id, question)
```

## Code Organization

### Separation of Concerns

**Recommended Practices:**
- Separate MCP client logic from platform-specific code
- Create reusable utility modules
- Minimize platform-specific customizations
- Follow single responsibility principle

**Example:**
```python
# Recommended - separation of concerns
# shared/mcp_client.py - MCP protocol logic
# slack_bot.py - Slack-specific implementation
# teams_bot.py - Teams-specific implementation

# Avoid - monolithic design
# bot.py - all logic mixed together
```

### Configuration Management

**Recommended Practices:**
- Use configuration files or environment-based configuration
- Support environment-specific configurations (dev/staging/prod)
- Validate configuration parameters at startup
- Provide sensible defaults

**Example:**
```python
from dataclasses import dataclass
from typing import Optional

@dataclass
class Config:
    databricks_host: str
    genie_space_id: str
    databricks_token: Optional[str] = None
    
    @classmethod
    def from_env(cls):
        return cls(
            databricks_host=os.getenv("DATABRICKS_HOST"),
            genie_space_id=os.getenv("GENIE_SPACE_ID"),
            databricks_token=os.getenv("DATABRICKS_TOKEN")
        )
    
    def validate(self):
        if not self.databricks_host:
            raise ValueError("DATABRICKS_HOST required")
        # ... more validation
```

## Testing

### Unit Tests

**Recommended Practices:**
- Test MCP client functionality independently
- Mock external dependencies appropriately
- Test error handling and edge cases
- Maintain adequate test coverage

**Example:**
```python
import pytest
from unittest.mock import AsyncMock, patch

@pytest.mark.asyncio
async def test_ask_genie():
    with patch('shared.mcp_client.DatabricksMCPClient') as mock_client:
        mock_client.return_value.call_tool = AsyncMock(return_value=MockResponse())
        client = create_mcp_client()
        response, _ = await client.ask_genie("space-id", "test")
        assert response is not None
```

### Integration Tests

**Recommended Practices:**
- Test complete end-to-end workflows
- Use staging MCP servers for testing
- Validate error scenarios
- Performance test critical paths

## Deployment

### Environment Management

**Recommended Practices:**
- Maintain separate environments (development, staging, production)
- Use environment-specific configurations
- Validate environment setup at startup
- Implement feature flags for gradual rollout

### Pre-Deployment Checklist

Review the following before production deployment:
- All unit and integration tests pass
- Environment variables properly configured
- Logging and monitoring systems operational
- Error handling and recovery tested
- Performance benchmarks within acceptable ranges
- Security controls reviewed and validated

## Documentation

**Recommended Practices:**
- Document all configuration options and their purposes
- Document API endpoints and integration points
- Document error codes and resolution steps
- Maintain up-to-date README documentation
- Document deployment and operational procedures

## Summary

Implementing these best practices ensures:
- Secure and compliant production deployments
- Reliable error handling and recovery
- Optimal application performance
- Maintainable and extensible codebase
- Effective troubleshooting and monitoring

## Next Steps

- Review platform-specific implementation guides
- Configure monitoring and alerting infrastructure
- Plan for scaling and high availability
- Document your deployment procedures

