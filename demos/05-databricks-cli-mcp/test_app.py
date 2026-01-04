"""
Test the deployed Databricks CLI MCP app.

This script tests the app by making HTTP requests to verify it's working.
"""

import asyncio
import httpx
import os
from databricks.sdk import WorkspaceClient


async def test_mcp_app():
    """Test the Databricks CLI MCP app endpoints."""

    APP_URL = "https://databricks-cli-mcp-1444828305810485.aws.databricksapps.com"

    print("=" * 60)
    print("Testing Databricks CLI MCP App")
    print("=" * 60)
    print(f"App URL: {APP_URL}")
    print()

    # Get authentication token
    w = WorkspaceClient(profile="DEFAULT")
    auth_header = w.config.authenticate()
    headers = {
        "Authorization": auth_header.get("Authorization"),
        "Content-Type": "application/json"
    }

    print(f"✅ Authenticated as: {w.current_user.me().user_name}")
    print()

    async with httpx.AsyncClient(timeout=60.0, follow_redirects=True) as client:
        # Test 1: Health check
        print("Test 1: Health Check")
        print("-" * 40)
        try:
            response = await client.get(f"{APP_URL}/health")
            print(f"Status: {response.status_code}")
            print(f"Response: {response.text}")
            print("✅ Health check passed\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")

        # Test 2: List MCP tools
        print("Test 2: List MCP Tools")
        print("-" * 40)
        try:
            response = await client.get(f"{APP_URL}/mcp/tools", headers=headers)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                print(f"Available tools: {len(data.get('tools', []))}")
                for tool in data.get("tools", []):
                    print(f"  - {tool.get('name')}: {tool.get('description')[:60]}...")
                print("✅ Tools listed successfully\n")
            else:
                print(f"Response: {response.text[:200]}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")

        # Test 3: Explore workspace
        print("Test 3: Explore Workspace")
        print("-" * 40)
        try:
            response = await client.post(f"{APP_URL}/mcp/explore", headers=headers)
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                content = data.get("content", [{}])[0].get("text", "")
                print(f"Response length: {len(content)} chars")
                print(f"Preview: {content[:200]}...")
                print("✅ Explore workspace successful\n")
            else:
                print(f"Response: {response.text[:200]}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")

        # Test 4: List clusters
        print("Test 4: List Clusters")
        print("-" * 40)
        try:
            response = await client.post(
                f"{APP_URL}/mcp/invoke",
                headers=headers,
                json={
                    "name": "invoke_databricks_cli",
                    "arguments": {
                        "category": "clusters",
                        "args": ["list"]
                    }
                }
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                content = data.get("content", [{}])[0].get("text", "")
                print(f"Response length: {len(content)} chars")
                print(f"Preview: {content[:200]}...")
                print("✅ List clusters successful\n")
            else:
                print(f"Response: {response.text[:200]}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")

        # Test 5: List jobs
        print("Test 5: List Jobs")
        print("-" * 40)
        try:
            response = await client.post(
                f"{APP_URL}/mcp/invoke",
                headers=headers,
                json={
                    "name": "invoke_databricks_cli",
                    "arguments": {
                        "category": "jobs",
                        "args": ["list"]
                    }
                }
            )
            print(f"Status: {response.status_code}")
            if response.status_code == 200:
                data = response.json()
                content = data.get("content", [{}])[0].get("text", "")
                print(f"Response length: {len(content)} chars")
                print(f"Preview: {content[:200]}...")
                print("✅ List jobs successful\n")
            else:
                print(f"Response: {response.text[:200]}\n")
        except Exception as e:
            print(f"❌ Error: {e}\n")

    print("=" * 60)
    print("Testing Complete!")
    print("=" * 60)


if __name__ == "__main__":
    asyncio.run(test_mcp_app())
