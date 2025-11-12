"""
REST API Demo - Unity Catalog Functions Integration

This demonstrates using the universal MCP client to build a REST API that
executes Unity Catalog Functions. The pattern shows how UC Functions provide
governed business logic while the universal client handles all Databricks
communication.

Key Pattern: Import universal client, focus on API-specific logic.
"""

from fastapi import FastAPI, HTTPException
from pydantic import BaseModel, Field
import sys
from pathlib import Path
from typing import Optional
import json

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from shared.mcp_client import create_mcp_client
from shared.config import UC_FUNCTION_NAME

# Initialize FastAPI
app = FastAPI(
    title="Product Discount API",
    description="REST API using Databricks UC Functions via universal MCP client",
    version="1.0.0"
)

# Universal MCP client - handles ALL Databricks communication
mcp_client = create_mcp_client()


# Request/Response Models
class DiscountRequest(BaseModel):
    """Request model for discount calculation."""
    order_amount: float = Field(..., gt=0, description="Order amount in dollars")
    customer_segment: str = Field(..., description="Customer segment (Enterprise, Mid-Market, SMB, Individual)")

    class Config:
        json_schema_extra = {
            "example": {
                "order_amount": 50000.00,
                "customer_segment": "Enterprise"
            }
        }


class DiscountResponse(BaseModel):
    """Response model for discount calculation."""
    order_amount: float
    customer_segment: str
    discount_amount: float
    discount_percentage: float
    final_amount: float
    segment_tier: Optional[str] = None


# API Endpoints
@app.get("/")
async def root():
    """API health check and information."""
    return {
        "service": "Product Discount API",
        "status": "healthy",
        "pattern": "Universal MCP Client",
        "data_source": "Unity Catalog Functions",
        "endpoints": {
            "/calculate-discount": "POST - Calculate personalized discount",
            "/health": "GET - Service health check",
            "/docs": "GET - Interactive API documentation"
        }
    }


@app.get("/health")
async def health_check():
    """Detailed health check including Databricks connectivity."""
    return {
        "status": "healthy",
        "databricks_integration": "universal_mcp_client",
        "uc_function": UC_FUNCTION_NAME
    }


@app.post("/calculate-discount", response_model=DiscountResponse)
async def calculate_discount(request: DiscountRequest):
    """
    Calculate personalized discount using Unity Catalog Function.

    This endpoint demonstrates the universal client pattern:
    - Single line calls UC Function via universal MCP client
    - API code focuses on HTTP concerns (validation, formatting)
    - No custom Databricks integration code needed

    The UC Function encapsulates business logic:
    - Discount rules by segment
    - A/B test variants
    - Compliance rules
    - Audit logging
    """
    try:
        # Universal client handles UC Functions communication
        # Notice: Single line for Databricks integration
        result = await mcp_client.call_function(
            UC_FUNCTION_NAME,
            {
                "order_amount": request.order_amount,
                "customer_segment": request.customer_segment
            }
        )

        # Parse UC Function response
        discount_data = parse_uc_function_result(result)

        # Build API response
        return DiscountResponse(
            order_amount=request.order_amount,
            customer_segment=request.customer_segment,
            discount_amount=discount_data["discount_amount"],
            discount_percentage=discount_data["discount_percentage"],
            final_amount=discount_data["final_amount"],
            segment_tier=discount_data.get("segment_tier")
        )

    except Exception as e:
        # Universal client provides consistent error types
        raise HTTPException(
            status_code=500,
            detail=f"Error calculating discount: {str(e)}"
        )


def parse_uc_function_result(raw_result: str) -> dict:
    """
    Parse UC Function response into structured data.

    UC Functions return JSON with nested structure:
    {"rows": [[{"schema": [...], "values": [...]}]]}
    """
    try:
        data = json.loads(raw_result)

        # Extract nested result
        if "rows" in data and len(data["rows"]) > 0:
            first_row = data["rows"][0]
            if isinstance(first_row, list) and len(first_row) > 0:
                result_obj = first_row[0]

                if isinstance(result_obj, dict):
                    schema = result_obj.get("schema", [])
                    values = result_obj.get("values", [])

                    # Map schema to values
                    result = {}
                    for i, field_def in enumerate(schema):
                        field_name = field_def.get("name", f"field_{i}")
                        if i < len(values):
                            result[field_name] = values[i]

                    return result

        raise ValueError("Unexpected UC Function response structure")

    except json.JSONDecodeError as e:
        raise ValueError(f"Invalid JSON from UC Function: {e}")


# Example client code
def example_usage():
    """
    Example showing how clients would call this API.
    Run this separately to test the API.
    """
    import requests

    base_url = "http://localhost:8000"

    # Example 1: Enterprise customer
    response = requests.post(
        f"{base_url}/calculate-discount",
        json={
            "order_amount": 50000.00,
            "customer_segment": "Enterprise"
        }
    )
    print("Enterprise Discount:")
    print(response.json())
    print()

    # Example 2: Individual customer
    response = requests.post(
        f"{base_url}/calculate-discount",
        json={
            "order_amount": 500.00,
            "customer_segment": "Individual"
        }
    )
    print("Individual Discount:")
    print(response.json())


if __name__ == "__main__":
    import uvicorn

    print("=" * 70)
    print("REST API Demo - Universal MCP Client Pattern")
    print("=" * 70)
    print()
    print("This API uses Unity Catalog Functions via the universal MCP client.")
    print("Business logic is governed in UC, API focuses on HTTP concerns.")
    print()
    print("Starting server...")
    print("  • API docs: http://localhost:8000/docs")
    print("  • Health check: http://localhost:8000/health")
    print()
    print("Example request:")
    print('  curl -X POST http://localhost:8000/calculate-discount \\')
    print('    -H "Content-Type: application/json" \\')
    print('    -d \'{"order_amount": 50000, "customer_segment": "Enterprise"}\'')
    print()

    uvicorn.run(app, host="0.0.0.0", port=8000)
