"""
Slack bot using Databricks Genie MCP.

Notice: 80% of the logic is in shared/mcp_client.py!
This is just a thin wrapper around the universal MCP client.

Deployment: Databricks Apps (no Azure needed!)
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler

from shared.mcp_client import create_mcp_client
from shared.config import (
    SLACK_BOT_TOKEN,
    SLACK_APP_TOKEN,
    GENIE_SPACE_ID,
    VECTOR_SEARCH_INDEX_ID,
    UC_FUNCTION_NAME,
    validate_config
)
from shared.genie_formatter import format_genie_response, format_uc_function_response
import json

# Initialize Slack app
app = AsyncApp(token=SLACK_BOT_TOKEN)

# Initialize MCP client - THE SHARED INTEGRATION!
mcp_client = create_mcp_client()

# Store conversation contexts per thread
conversations = {}


# REMOVED: format_genie_response() - now imported from shared.genie_formatter
# REMOVED: format_uc_function_response() - now imported from shared.genie_formatter
# This eliminates code duplication and ensures both Slack and Teams bots use the same formatting logic


def format_vector_search_response(raw_response: str):
    """
    Parse and format Vector Search JSON response into Slack blocks.

    Returns tuple of (formatted_text, blocks) for rich display.
    """
    try:
        # Parse JSON array
        if raw_response.strip().startswith('['):
            results = json.loads(raw_response)
        else:
            # Maybe wrapped in an object
            data = json.loads(raw_response)
            results = data.get('results', data.get('data', []))

        if not results:
            return "_No results found for your search._", None

        # Build blocks for rich formatting
        blocks = []
        text_parts = []

        for i, doc in enumerate(results[:3], 1):  # Show top 3
            if isinstance(doc, dict):
                title = doc.get('title', 'Untitled')
                content = doc.get('content', '')
                category = doc.get('category', '')

                # Add to text fallback
                text_parts.append(f"{i}. {title}")

                # Create a block for this result
                result_text = f"*{i}. {title}*\n"
                if category:
                    result_text += f"_{category}_\n\n"

                # Add excerpt (first 200 chars for cleaner display)
                if content:
                    excerpt = content[:200].strip()
                    if len(content) > 200:
                        excerpt += "..."
                    result_text += excerpt

                blocks.append({
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": result_text}
                })

        return "\n".join(text_parts), blocks

    except json.JSONDecodeError:
        return f"Raw response: {raw_response[:300]}", None
    except Exception as e:
        return f"Error: {str(e)}", None


@app.event("app_mention")
async def handle_mention(event, say):
    """
    Handle @mentions in channels.
    
    Example:
        @Genie Bot what was Q4 revenue?
        @Genie Bot search for MCP documentation
        @Genie Bot calculate discount 50000 Enterprise
    """
    # Extract question (remove bot mention)
    question = event["text"].split(">", 1)[-1].strip()
    thread_ts = event.get("thread_ts") or event["ts"]
    
    # Determine command type
    if question.lower().startswith("list clusters"):
        # Databricks CLI: List clusters
        try:
            response = await mcp_client.invoke_databricks_cli("clusters", ["list"])
            prefix = "🖥️ *Clusters:*"
        except Exception as e:
            response = f"Error listing clusters: {str(e)}"
            prefix = "❌ *Error:*"

    elif question.lower().startswith("list jobs"):
        # Databricks CLI: List jobs
        try:
            response = await mcp_client.invoke_databricks_cli("jobs", ["list"])
            prefix = "⚙️ *Jobs:*"
        except Exception as e:
            response = f"Error listing jobs: {str(e)}"
            prefix = "❌ *Error:*"

    elif question.lower().startswith("list warehouses"):
        # Databricks CLI: List warehouses
        try:
            response = await mcp_client.invoke_databricks_cli("warehouses", ["list"])
            prefix = "🏢 *Warehouses:*"
        except Exception as e:
            response = f"Error listing warehouses: {str(e)}"
            prefix = "❌ *Error:*"

    elif question.lower().startswith("explore workspace") or question.lower() == "explore":
        # Databricks CLI: Explore workspace
        try:
            response = await mcp_client.explore_workspace()
            prefix = "🔍 *Workspace Info:*"
        except Exception as e:
            response = f"Error exploring workspace: {str(e)}"
            prefix = "❌ *Error:*"

    elif question.lower().startswith("search "):
        # Vector Search
        query = question[7:]
        try:
            response = await mcp_client.search_docs(
                VECTOR_SEARCH_INDEX_ID,
                query,
                num_results=3
            )
            # Check if response indicates an error
            if response.startswith("Error:"):
                await say(
                    blocks=[
                        {"type": "section", "text": {"type": "mrkdwn", "text": f"*Q:* {question}"}},
                        {"type": "divider"},
                        {"type": "section", "text": {"type": "mrkdwn", "text": f"⚠️ *Vector Search Error*\n\n{response}"}}
                    ],
                    text=f"Error: {response}",
                    thread_ts=thread_ts
                )
                return
            else:
                # Format the vector search response into blocks
                text_fallback, result_blocks = format_vector_search_response(response)

                # Build message blocks
                message_blocks = [
                    {"type": "section", "text": {"type": "mrkdwn", "text": f"*Q:* {question}"}},
                    {"type": "divider"},
                    {"type": "section", "text": {"type": "mrkdwn", "text": "📚 *Search Results:*"}}
                ]

                if result_blocks:
                    message_blocks.extend(result_blocks)
                else:
                    message_blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": text_fallback}})

                await say(
                    blocks=message_blocks,
                    text=f"Search Results: {text_fallback}",
                    thread_ts=thread_ts
                )
                return

        except Exception as e:
            await say(
                blocks=[
                    {"type": "section", "text": {"type": "mrkdwn", "text": f"*Q:* {question}"}},
                    {"type": "divider"},
                    {"type": "section", "text": {"type": "mrkdwn", "text": f"⚠️ *Vector Search Error*\n\nCouldn't complete search: {str(e)}"}}
                ],
                text=f"Error: {str(e)}",
                thread_ts=thread_ts
            )
            return

    elif question.lower().startswith("calculate ") or question.lower().startswith("discount "):
        # UC Function
        try:
            parts = question.split()
            amount = float(parts[1])
            segment = parts[2]
            response = await mcp_client.call_function(
                UC_FUNCTION_NAME,
                {"order_amount": amount, "customer_segment": segment}
            )
            # Format the UC function response using shared formatter
            response = format_uc_function_response(response, platform="slack")
            prefix = "💰 *Calculation:*"
        except (IndexError, ValueError):
            response = "Usage: calculate <amount> <segment>\nExample: calculate 50000 Enterprise"
            prefix = "❌ *Error:*"
    
    else:
        # Default: Genie analytics
        conv_id = conversations.get(thread_ts)
        response, new_conv_id = await mcp_client.ask_genie(
            GENIE_SPACE_ID,
            question,
            conv_id
        )
        conversations[thread_ts] = new_conv_id
        # Format the Genie response nicely using shared formatter
        response = format_genie_response(response, platform="slack")
        prefix = "🧞 *Genie:*"
    
    # Send response in thread with proper text fallback
    await say(
        blocks=[
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"*Q:* {question}"}
            },
            {"type": "divider"},
            {
                "type": "section",
                "text": {"type": "mrkdwn", "text": f"{prefix}\n{response}"}
            }
        ],
        text=f"{prefix}\n{response}",  # Proper text fallback
        thread_ts=thread_ts
    )


@app.event("message")
async def handle_dm(event, say):
    """
    Handle direct messages.
    
    Users can chat with bot in DMs for private queries.
    """
    if event.get("channel_type") == "im" and not event.get("subtype"):
        question = event["text"]
        ts = event["ts"]
        
        # Reset command
        if question.lower() in ['/reset', 'reset', 'new']:
            conversations.pop(ts, None)
            await say("🔄 Conversation reset! Start fresh with a new question.")
            return
        
        # Help command
        if question.lower() in ['/help', 'help']:
            await say("""*Databricks Genie Bot Commands:*

📊 *Analytics (Genie):*
Just ask natural language questions:
• "What was Q4 revenue?"
• "Show me top 5 customers"
• "Compare Q3 vs Q4 performance"
• "What's the average order value?"

🔍 *Search Docs (Vector Search):*
Start with "search" to find documentation:

*Getting Started:*
• "search how to get started with Genie"
• "search creating a Genie space"
• "search vector search RAG"

*Troubleshooting:*
• "search Genie troubleshooting"
• "search timeout errors"
• "search query returns incorrect results"

*Best Practices:*
• "search Genie space best practices"
• "search optimizing Genie"
• "search metadata tips"

*Integration:*
• "search building Slack bots"
• "search MCP integration"
• "search Socket Mode setup"

💰 *Calculate (UC Functions):*
Start with "calculate" or "discount":
• "calculate 50000 Enterprise"
• "discount 25000 Mid-Market"

⚙️ *Other Commands:*
• `reset` - Start new conversation
• `help` - Show this message

*Tips:*
• Ask follow-up questions in threads to maintain context
• Use @Genie Bot in channels to share with team
• Be specific with search queries for better results""")
            return
        
        # Route based on command
        if question.lower().startswith("search "):
            query = question[7:]
            response = await mcp_client.search_docs(
                VECTOR_SEARCH_INDEX_ID,
                query,
                num_results=3
            )
            # Format the vector search response into blocks
            text_fallback, result_blocks = format_vector_search_response(response)

            # Build message blocks
            message_blocks = [{"type": "section", "text": {"type": "mrkdwn", "text": "📚 *Search Results:*"}}]

            if result_blocks:
                message_blocks.extend(result_blocks)
            else:
                message_blocks.append({"type": "section", "text": {"type": "mrkdwn", "text": text_fallback}})

            await say(blocks=message_blocks, text=f"Search Results: {text_fallback}")
            return
        elif question.lower().startswith(("calculate ", "discount ")):
            try:
                parts = question.split()
                amount = float(parts[1])
                segment = parts[2]
                response = await mcp_client.call_function(
                    UC_FUNCTION_NAME,
                    {"order_amount": amount, "customer_segment": segment}
                )
                # Format the UC function response using shared formatter
                response = format_uc_function_response(response, platform="slack")
            except (IndexError, ValueError):
                response = "Usage: calculate <amount> <segment>\nExample: calculate 50000 Enterprise"
        else:
            # Default: Genie
            conv_id = conversations.get(ts)
            response, new_conv_id = await mcp_client.ask_genie(
                GENIE_SPACE_ID,
                question,
                conv_id
            )
            conversations[ts] = new_conv_id
            # Format the Genie response nicely using shared formatter
            response = format_genie_response(response, platform="slack")

        # Safety check - ensure response is not empty
        if not response or not response.strip():
            response = "I received your question but got an empty response. Please try again."

        # Send response with text fallback for Slack API
        await say(text=response, mrkdwn=True)


@app.event("app_home_opened")
async def update_home_tab(client, event):
    """
    Customize the Home tab view.
    """
    await client.views_publish(
        user_id=event["user"],
        view={
            "type": "home",
            "blocks": [
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Welcome to Databricks Genie Bot! 🧞*\n\nI can help you analyze data, search documentation, and execute calculations."
                    }
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*What I can do:*\n\n📊 *Analytics*\nAsk me questions about your data in natural language\n\n🔍 *Search*\nFind documentation and guides\n\n💰 *Calculate*\nExecute business functions and calculations"
                    }
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {
                        "type": "mrkdwn",
                        "text": "*Try asking:*\n• What was revenue last quarter?\n• search MCP integration\n• calculate 50000 Enterprise"
                    }
                }
            ]
        }
    )


async def main():
    """Start the Slack bot with Socket Mode"""
    print("=" * 60)
    print("🤖 Starting Slack Genie Bot...")
    print("=" * 60)
    
    try:
        validate_config()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        return
    
    print("✅ Configuration valid")
    print(f"📊 Genie Space: {GENIE_SPACE_ID}")
    print(f"🔍 Vector Search: {VECTOR_SEARCH_INDEX_ID}")
    print(f"⚙️ UC Function: {UC_FUNCTION_NAME}")
    print()
    print("🚀 Bot is running... Send a DM or @mention me in a channel!")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    handler = AsyncSocketModeHandler(app, SLACK_APP_TOKEN)
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(main())

