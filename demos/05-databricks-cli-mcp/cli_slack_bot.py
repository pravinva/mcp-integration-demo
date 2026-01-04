"""
Minimal Slack bot for Databricks CLI MCP only.
No Genie, no Vector Search - just CLI commands.
"""

import asyncio
import os
from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
import httpx
from databricks.sdk import WorkspaceClient

# Initialize Slack app
app = AsyncApp(token=os.getenv("SLACK_BOT_TOKEN"))

# Databricks CLI MCP URL
DATABRICKS_CLI_MCP_URL = os.getenv(
    "DATABRICKS_CLI_MCP_URL",
    "https://databricks-cli-mcp-1444828305810485.aws.databricksapps.com"
)

# Initialize Databricks client
w = WorkspaceClient()


async def call_cli_mcp(endpoint: str, payload: dict = None):
    """Call the Databricks CLI MCP server."""
    auth_header = w.config.authenticate()

    async with httpx.AsyncClient(timeout=30.0) as client:
        if payload:
            response = await client.post(
                f"{DATABRICKS_CLI_MCP_URL}{endpoint}",
                headers={"Authorization": auth_header.get("Authorization")},
                json=payload
            )
        else:
            response = await client.post(
                f"{DATABRICKS_CLI_MCP_URL}{endpoint}",
                headers={"Authorization": auth_header.get("Authorization")}
            )
        response.raise_for_status()
        result = response.json()
        return result.get("content", [{}])[0].get("text", "No output")


@app.event("app_mention")
async def handle_mention(event, say):
    """Handle @mentions in channels."""
    question = event["text"].split(">", 1)[-1].strip()
    thread_ts = event.get("thread_ts") or event["ts"]

    try:
        if question.lower().startswith("list clusters"):
            response = await call_cli_mcp("/mcp/invoke", {
                "name": "invoke_databricks_cli",
                "arguments": {"category": "clusters", "args": ["list"]}
            })
            prefix = "🖥️ *Clusters:*"

        elif question.lower().startswith("list jobs"):
            response = await call_cli_mcp("/mcp/invoke", {
                "name": "invoke_databricks_cli",
                "arguments": {"category": "jobs", "args": ["list"]}
            })
            prefix = "⚙️ *Jobs:*"

        elif question.lower().startswith("list warehouses"):
            response = await call_cli_mcp("/mcp/invoke", {
                "name": "invoke_databricks_cli",
                "arguments": {"category": "warehouses", "args": ["list"]}
            })
            prefix = "🏢 *Warehouses:*"

        elif question.lower().startswith("explore") or question.lower().startswith("explore workspace"):
            response = await call_cli_mcp("/mcp/explore")
            prefix = "🔍 *Workspace:*"

        else:
            response = "Available commands:\n• list clusters\n• list jobs\n• list warehouses\n• explore workspace"
            prefix = "ℹ️ *Help:*"

        await say(
            blocks=[
                {"type": "section", "text": {"type": "mrkdwn", "text": f"*Q:* {question}"}},
                {"type": "divider"},
                {"type": "section", "text": {"type": "mrkdwn", "text": f"{prefix}\n```{response[:2000]}```"}}
            ],
            text=f"{prefix}\n{response[:500]}",
            thread_ts=thread_ts
        )
    except Exception as e:
        await say(
            text=f"Error: {str(e)}",
            thread_ts=thread_ts
        )


@app.event("message")
async def handle_dm(event, say):
    """Handle direct messages."""
    if event.get("channel_type") == "im" and not event.get("subtype"):
        question = event["text"]

        if question.lower() in ["help", "/help"]:
            await say("""*Databricks CLI Bot Commands:*

🖥️ *Cluster Commands:*
• list clusters - Show all compute clusters

⚙️ *Job Commands:*
• list jobs - Show all workflow jobs

🏢 *Warehouse Commands:*
• list warehouses - Show SQL warehouses

🔍 *Workspace Commands:*
• explore workspace - Get workspace overview""")
            return

        try:
            if question.lower().startswith("list clusters"):
                response = await call_cli_mcp("/mcp/invoke", {
                    "name": "invoke_databricks_cli",
                    "arguments": {"category": "clusters", "args": ["list"]}
                })

            elif question.lower().startswith("list jobs"):
                response = await call_cli_mcp("/mcp/invoke", {
                    "name": "invoke_databricks_cli",
                    "arguments": {"category": "jobs", "args": ["list"]}
                })

            elif question.lower().startswith("list warehouses"):
                response = await call_cli_mcp("/mcp/invoke", {
                    "name": "invoke_databricks_cli",
                    "arguments": {"category": "warehouses", "args": ["list"]}
                })

            elif question.lower().startswith("explore"):
                response = await call_cli_mcp("/mcp/explore")

            else:
                response = "I don't understand. Type 'help' for available commands."

            await say(f"```{response[:3000]}```")

        except Exception as e:
            await say(f"Error: {str(e)}")


async def main():
    """Start the Slack bot."""
    print("=" * 60)
    print("🤖 Starting Databricks CLI MCP Slack Bot...")
    print(f"📡 MCP Server: {DATABRICKS_CLI_MCP_URL}")
    print("=" * 60)

    handler = AsyncSocketModeHandler(app, os.getenv("SLACK_APP_TOKEN"))
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(main())
