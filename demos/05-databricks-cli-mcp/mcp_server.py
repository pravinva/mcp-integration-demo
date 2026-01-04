"""
Databricks CLI MCP Server - HTTP wrapper for official MCP.

Exposes the official Databricks CLI MCP server via HTTP for Databricks Apps deployment.
This enables Slack/Teams bots to access full Databricks CLI functionality.
"""

import asyncio
import json
import os
import subprocess
from typing import Any, Dict
from fastapi import FastAPI, HTTPException
from fastapi.responses import JSONResponse
from pydantic import BaseModel
from databricks.sdk import WorkspaceClient
import uvicorn


app = FastAPI(
    title="Databricks CLI MCP Server",
    description="HTTP endpoint for Databricks CLI MCP operations",
    version="1.0.0"
)

# Initialize Databricks client
w = WorkspaceClient()


class ExploreRequest(BaseModel):
    """Request to explore workspace resources."""
    pass


class InvokeCLIRequest(BaseModel):
    """Request to invoke Databricks CLI command."""
    command: str
    args: list[str] = []


@app.get("/health")
async def health_check():
    """Health check endpoint."""
    return {"status": "healthy", "service": "databricks-cli-mcp"}


@app.post("/mcp/explore")
async def explore_workspace(request: ExploreRequest):
    """
    Explore Databricks workspace resources.

    Returns workspace configuration, available resources, and command examples.
    """
    try:
        # Get workspace info
        current_user = w.current_user.me()

        # Get catalogs
        catalogs = []
        try:
            for catalog in w.catalogs.list():
                catalogs.append({
                    "name": catalog.name,
                    "comment": catalog.comment
                })
        except Exception as e:
            catalogs = [{"error": str(e)}]

        # Get warehouses
        warehouses = []
        try:
            for wh in w.warehouses.list():
                warehouses.append({
                    "id": wh.id,
                    "name": wh.name,
                    "state": wh.state.value if wh.state else "UNKNOWN",
                    "cluster_size": wh.cluster_size
                })
        except Exception as e:
            warehouses = [{"error": str(e)}]

        # Get clusters (limit to 10)
        clusters = []
        try:
            for cluster in list(w.clusters.list())[:10]:
                clusters.append({
                    "id": cluster.cluster_id,
                    "name": cluster.cluster_name,
                    "state": cluster.state.value if cluster.state else "UNKNOWN"
                })
        except Exception as e:
            clusters = [{"error": str(e)}]

        # Build exploration response
        exploration = {
            "workspace": {
                "host": w.config.host,
                "user": current_user.user_name
            },
            "resources": {
                "catalogs": catalogs,
                "warehouses": warehouses,
                "clusters": clusters
            },
            "examples": {
                "query_data": "databricks sql query --warehouse-id <id> 'SELECT * FROM catalog.schema.table LIMIT 10'",
                "list_jobs": "databricks jobs list",
                "create_cluster": "databricks clusters create --json-file cluster-config.json",
                "deploy_bundle": "databricks bundle deploy -t dev"
            }
        }

        return JSONResponse(content=exploration)

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mcp/invoke")
async def invoke_cli(request: InvokeCLIRequest):
    """
    Invoke a Databricks CLI command.

    Examples:
    - command: "catalogs", args: ["list"]
    - command: "jobs", args: ["list", "--limit", "10"]
    - command: "clusters", args: ["get", "--cluster-id", "abc-123"]
    - command: "sql", args: ["query", "--warehouse-id", "xyz", "SELECT 1"]
    """
    try:
        # Build full command
        cmd = ["databricks", request.command] + request.args

        # Execute command
        result = subprocess.run(
            cmd,
            capture_output=True,
            text=True,
            timeout=60
        )

        # Parse result
        if result.returncode == 0:
            # Try to parse as JSON if possible
            output = result.stdout.strip()
            try:
                parsed = json.loads(output)
                return JSONResponse(content={
                    "status": "success",
                    "data": parsed
                })
            except json.JSONDecodeError:
                return JSONResponse(content={
                    "status": "success",
                    "output": output
                })
        else:
            return JSONResponse(
                status_code=400,
                content={
                    "status": "error",
                    "error": result.stderr.strip(),
                    "command": " ".join(cmd)
                }
            )

    except subprocess.TimeoutExpired:
        raise HTTPException(status_code=408, detail="Command execution timeout")
    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.post("/mcp/query")
async def query_sql(
    warehouse_id: str,
    query: str
):
    """
    Execute SQL query using Databricks SQL warehouse.

    Simplified endpoint for common use case.
    """
    try:
        # Execute SQL statement
        statement = w.statement_execution.execute_statement(
            warehouse_id=warehouse_id,
            statement=query,
            wait_timeout="30s"
        )

        # Format results
        if statement.result and statement.result.data_array:
            columns = [col.name for col in statement.manifest.schema.columns]

            results = []
            for row in statement.result.data_array[:1000]:  # Limit to 1000 rows
                results.append(dict(zip(columns, row)))

            return JSONResponse(content={
                "status": "success",
                "columns": columns,
                "row_count": len(results),
                "data": results
            })
        else:
            return JSONResponse(content={
                "status": "success",
                "message": "Query executed successfully, no results returned"
            })

    except Exception as e:
        raise HTTPException(status_code=500, detail=str(e))


@app.get("/mcp/tools")
async def list_tools():
    """
    List all available MCP tools.

    Returns tool definitions for MCP clients.
    """
    tools = [
        {
            "name": "explore",
            "description": "Explore Databricks workspace resources and get command examples",
            "parameters": {}
        },
        {
            "name": "invoke_databricks_cli",
            "description": "Execute any Databricks CLI command (catalogs, jobs, clusters, bundles, apps, etc.)",
            "parameters": {
                "command": "CLI command (e.g., 'catalogs', 'jobs', 'clusters')",
                "args": "Command arguments (e.g., ['list'], ['get', '--job-id', '123'])"
            }
        },
        {
            "name": "query_sql",
            "description": "Execute SQL query against Databricks warehouse",
            "parameters": {
                "warehouse_id": "SQL Warehouse ID",
                "query": "SQL query to execute"
            }
        }
    ]

    return JSONResponse(content={"tools": tools})


if __name__ == "__main__":
    port = int(os.getenv("DATABRICKS_APP_PORT", "8000"))
    uvicorn.run(app, host="0.0.0.0", port=port)
