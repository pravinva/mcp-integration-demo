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
import json

# Initialize Slack app
app = AsyncApp(token=SLACK_BOT_TOKEN)

# Initialize MCP client - THE SHARED INTEGRATION!
mcp_client = create_mcp_client()

# Store conversation contexts per thread
conversations = {}


def format_genie_response(raw_response: str) -> str:
    """
    Parse and format Genie's JSON response into human-readable text.

    Genie MCP returns nested JSON: {"content": "{...escaped JSON...}"}
    We need to unpack this double encoding.
    """
    try:
        # First parse - outer JSON with "content" field
        outer = json.loads(raw_response)

        # Extract the content field which contains the actual Genie response as a JSON string
        if "content" in outer:
            # Second parse - the actual Genie data
            data = json.loads(outer["content"])
        else:
            # If no content field, assume it's already the inner data
            data = outer

        formatted = []

        # Show the SQL query that was generated
        if "query" in data:
            formatted.append(f"📊 *SQL Query:*\n```{data['query']}```\n")

        # Extract and format the results
        if "statement_response" in data and "result" in data["statement_response"]:
            result = data["statement_response"]["result"]
            manifest = data["statement_response"]["manifest"]

            if "data_array" in result and result["data_array"]:
                # Get column names
                columns = [col["name"] for col in manifest["schema"]["columns"]]

                formatted.append("*Results:*")

                # Format each row
                for row in result["data_array"]:
                    values = row.get("values", [])
                    row_text = []
                    for i, col_name in enumerate(columns):
                        if i < len(values):
                            value = values[i].get("string_value", "N/A")
                            row_text.append(f"• *{col_name}:* {value}")
                    formatted.append("\n".join(row_text))

                # Add row count
                total_rows = manifest.get("total_row_count", 0)
                formatted.append(f"\n_({total_rows} row{'s' if total_rows != 1 else ''} returned)_")
            else:
                formatted.append("_No results found_")

        result_text = "\n".join(formatted)

        # Safety check - ensure we return something valid
        if not result_text or result_text.strip() == "":
            return f"Received response but couldn't format it. Raw: {raw_response[:200]}"

        return result_text

    except json.JSONDecodeError as e:
        # If it's not JSON, return as-is (might be an error message)
        if raw_response and raw_response.strip():
            return f"_JSON parse error: {str(e)}_\n{raw_response[:300]}"
        return "Empty response from Genie"
    except Exception as e:
        # If formatting fails, return the original with a note
        return f"_Note: Unable to format response: {str(e)}_\n\n{raw_response[:500]}"


def format_uc_function_response(raw_response: str) -> str:
    """
    Parse and format UC Function JSON response into human-readable text.

    UC Functions return JSON with nested structure:
    {"columns": ["output"], "rows": [[{"schema": [...], "values": [...]}]]}
    """
    try:
        data = json.loads(raw_response)

        formatted = ["*Function Result:*"]

        # UC Functions wrap results in rows -> [0] -> schema + values
        if "rows" in data and len(data["rows"]) > 0:
            # Get the first (and usually only) row
            first_row = data["rows"][0]

            if isinstance(first_row, list) and len(first_row) > 0:
                # The actual result is in first_row[0]
                result_obj = first_row[0]

                if isinstance(result_obj, dict):
                    # Extract schema and values
                    schema = result_obj.get("schema", [])
                    values = result_obj.get("values", [])

                    # Format each field
                    for i, field_def in enumerate(schema):
                        field_name = field_def.get("name", f"field_{i}")
                        if i < len(values):
                            value = values[i]
                            # Format the value nicely
                            if isinstance(value, float):
                                # Format numbers nicely
                                if field_name.endswith("percentage"):
                                    formatted.append(f"• *{field_name}:* {value}%")
                                elif "amount" in field_name.lower():
                                    formatted.append(f"• *{field_name}:* ${value:,.2f}")
                                else:
                                    formatted.append(f"• *{field_name}:* {value}")
                            else:
                                formatted.append(f"• *{field_name}:* {value}")

                    return "\n".join(formatted)

        # If we couldn't parse the structure, return a generic success message
        formatted.append("_Function executed successfully_")
        return "\n".join(formatted)

    except json.JSONDecodeError as e:
        # Not JSON, return as-is
        return raw_response
    except Exception as e:
        # Show error for debugging
        return f"_Unable to format response: {str(e)}_\n\n```{raw_response[:300]}```"


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
    if question.lower().startswith("search "):
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
            # Format the UC function response
            response = format_uc_function_response(response)
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
        # Format the Genie response nicely
        response = format_genie_response(response)
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
                # Format the UC function response
                response = format_uc_function_response(response)
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
            # Format the Genie response nicely
            response = format_genie_response(response)

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

