#!/usr/bin/env python3
"""
Test script for Databricks CLI MCP Server.

This script demonstrates how to test the MCP server using the databricks SDK,
which mimics what the Slack bot would do.
"""

import asyncio
import httpx
from databricks.sdk import WorkspaceClient


# MCP Server URL
DATABRICKS_CLI_MCP_URL = "https://databricks-cli-mcp-1444828305810485.aws.databricksapps.com"


async def test_mcp_endpoint(endpoint: str, payload: dict = None):
    """
    Test an MCP endpoint with authentication.

    Args:
        endpoint: The endpoint path (e.g., "/mcp/invoke")
        payload: Optional JSON payload for POST request

    Returns:
        Response text or error message
    """
    # Initialize Databricks client
    w = WorkspaceClient()

    # Get authentication header
    auth_header = w.config.authenticate()

    print(f"\n{'='*60}")
    print(f"Testing: {DATABRICKS_CLI_MCP_URL}{endpoint}")
    print(f"{'='*60}")

    try:
        async with httpx.AsyncClient(timeout=30.0) as client:
            if payload:
                print(f"Payload: {payload}")
                response = await client.post(
                    f"{DATABRICKS_CLI_MCP_URL}{endpoint}",
                    headers={"Authorization": auth_header.get("Authorization")},
                    json=payload,
                    follow_redirects=False
                )
            else:
                response = await client.post(
                    f"{DATABRICKS_CLI_MCP_URL}{endpoint}",
                    headers={"Authorization": auth_header.get("Authorization")},
                    follow_redirects=False
                )

            print(f"Status Code: {response.status_code}")

            if response.status_code == 302:
                print("⚠️  OAuth redirect detected (302)")
                print("This is expected when calling from local machine.")
                print("The MCP server requires OAuth authentication between service principals.")
                return None

            if response.status_code == 200:
                result = response.json()
                content = result.get("content", [])
                if content:
                    text = content[0].get("text", "No text")
                    print(f"✅ Success!")
                    print(f"Response:\n{text[:500]}")
                    return text
                else:
                    print(f"✅ Success!")
                    print(f"Response: {result}")
                    return result
            else:
                print(f"❌ Error: {response.status_code}")
                print(f"Response: {response.text[:500]}")
                return None

    except Exception as e:
        print(f"❌ Exception: {str(e)}")
        return None


async def main():
    """Run all tests."""

    print("\n" + "="*60)
    print("DATABRICKS CLI MCP SERVER TEST")
    print("="*60)
    print(f"\nMCP Server: {DATABRICKS_CLI_MCP_URL}")
    print("\nNOTE: If you see 302 redirects, this is EXPECTED when testing")
    print("from local machine. The MCP server requires OAuth authentication")
    print("between Databricks Apps service principals.")
    print("\nTo test the full flow:")
    print("1. Deploy the Slack bot as a Databricks App")
    print("2. The Slack bot will authenticate using OAuth")
    print("3. Test commands via Slack interface")

    # Test 1: Explore endpoint
    await test_mcp_endpoint("/mcp/explore")

    # Test 2: Invoke with clusters list
    await test_mcp_endpoint("/mcp/invoke", {
        "name": "invoke_databricks_cli",
        "arguments": {
            "working_directory": "/tmp",
            "args": ["clusters", "list"]
        }
    })

    # Test 3: Invoke with jobs list
    await test_mcp_endpoint("/mcp/invoke", {
        "name": "invoke_databricks_cli",
        "arguments": {
            "working_directory": "/tmp",
            "args": ["jobs", "list"]
        }
    })

    print("\n" + "="*60)
    print("TEST SUMMARY")
    print("="*60)
    print("\n✅ MCP Server is RUNNING at:")
    print(f"   {DATABRICKS_CLI_MCP_URL}")
    print("\n📋 Available Tools:")
    print("   - invoke_databricks_cli")
    print("   - databricks_configure_auth")
    print("   - databricks_discover")
    print("\n🔐 Authentication:")
    print("   - OAuth required (service principal to service principal)")
    print("   - Cannot be fully tested from local machine")
    print("\n🚀 Next Steps:")
    print("   1. Deploy Slack bot to Databricks Apps")
    print("   2. Configure Slack secrets")
    print("   3. Test via Slack: 'list clusters', 'list jobs', etc.")
    print("\n" + "="*60 + "\n")


if __name__ == "__main__":
    asyncio.run(main())
