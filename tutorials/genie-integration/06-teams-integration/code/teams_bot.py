"""
Microsoft Teams bot using Databricks Genie MCP.

Notice: Uses the SAME shared/mcp_client.py as Slack bot!
This demonstrates 80% code reuse - the M+N pattern!
"""

import sys
from pathlib import Path

# Add project root to path (adjust based on your structure)
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from aiohttp import web
from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    TurnContext
)
from botbuilder.schema import Activity, ActivityTypes

from shared.mcp_client import create_mcp_client
from shared.config import (
    MICROSOFT_APP_ID,
    MICROSOFT_APP_PASSWORD,
    GENIE_SPACE_ID
)
import json

# Bot Framework Adapter
# For local testing with Agents Playground, leave App ID/Password empty
SETTINGS = BotFrameworkAdapterSettings(
    MICROSOFT_APP_ID or "",  # Empty for local testing
    MICROSOFT_APP_PASSWORD or ""
)
ADAPTER = BotFrameworkAdapter(SETTINGS)

# MCP client - THE SAME ONE as Slack!
mcp_client = create_mcp_client()

# Conversation storage
conversations = {}


def format_genie_response(raw_response: str) -> str:
    """
    Parse and format Genie's JSON response into human-readable text.
    """
    try:
        # Parse nested JSON response
        outer = json.loads(raw_response)
        
        if "content" in outer:
            data = json.loads(outer["content"])
        else:
            data = outer
        
        formatted = []
        
        # Show SQL query if available
        if "query" in data:
            formatted.append(f"📊 **SQL Query:**\n```sql\n{data['query']}\n```\n")
        
        # Extract and format results
        if "statement_response" in data and "result" in data["statement_response"]:
            result = data["statement_response"]["result"]
            manifest = data["statement_response"]["manifest"]
            
            if "data_array" in result and result["data_array"]:
                columns = [col["name"] for col in manifest["schema"]["columns"]]
                formatted.append("**Results:**\n")
                
                for row in result["data_array"]:
                    values = row.get("values", [])
                    row_text = []
                    for i, col_name in enumerate(columns):
                        if i < len(values):
                            value = values[i].get("string_value", "N/A")
                            row_text.append(f"• **{col_name}:** {value}")
                    formatted.append("\n".join(row_text))
                
                total_rows = manifest.get("total_row_count", 0)
                formatted.append(f"\n_({total_rows} row{'s' if total_rows != 1 else ''} returned)_")
            else:
                formatted.append("_No results found_")
        
        result_text = "\n".join(formatted)
        
        if not result_text or result_text.strip() == "":
            return f"Received response but couldn't format it. Raw: {raw_response[:200]}"
        
        return result_text
        
    except json.JSONDecodeError as e:
        if raw_response and raw_response.strip():
            return f"_JSON parse error: {str(e)}_\n{raw_response[:300]}"
        return "Empty response from Genie"
    except Exception as e:
        return f"_Note: Unable to format response: {str(e)}_\n\n{raw_response[:500]}"


async def on_message_activity(turn_context: TurnContext):
    """
    Handle incoming messages from Teams.
    
    Supports:
    - Analytics questions (Genie)
    - Commands (/help, /reset)
    """
    user_message = turn_context.activity.text.strip()
    conv_key = turn_context.activity.conversation.id
    
    # Commands
    if user_message.lower() in ['/reset', 'reset']:
        conversations.pop(conv_key, None)
        await turn_context.send_activity("🔄 Conversation reset!")
        return
    
    if user_message.lower() in ['/help', 'help']:
        help_text = """**Databricks Genie Bot Help**

**📊 Analytics (Genie):**
Just ask questions naturally:
- "What was Q4 revenue?"
- "Show me top customers"
- "Compare Q3 vs Q4"

**Commands:**
- `/reset` - New conversation
- `/help` - This message"""
        
        await turn_context.send_activity(help_text)
        return
    
    # Show typing indicator
    await turn_context.send_activity(Activity(type=ActivityTypes.typing))
    
    try:
        # Get conversation context
        conv_id = conversations.get(conv_key)
        
        # Query Genie via MCP
        response, new_conv_id = await mcp_client.ask_genie(
            GENIE_SPACE_ID,
            user_message,
            conv_id
        )
        
        # Store conversation ID
        conversations[conv_key] = new_conv_id
        
        # Format response
        formatted_response = format_genie_response(response)
        
        # Send response
        await turn_context.send_activity(f"🧞 **Genie:**\n\n{formatted_response}")
        
    except Exception as e:
        error_msg = f"❌ Sorry, I encountered an error: {str(e)}"
        await turn_context.send_activity(error_msg)


async def on_members_added_activity(members_added, turn_context: TurnContext):
    """Welcome message when bot is added"""
    for member in members_added:
        if member.id != turn_context.activity.recipient.id:
            welcome = """👋 **Welcome to Databricks Genie!**

I can help you with:
📊 Data analytics (ask natural language questions)

Try asking:
- "What was our revenue last quarter?"
- "Show me top customers"

Type `/help` for more information."""
            
            await turn_context.send_activity(welcome)


async def health_check(req: web.Request) -> web.Response:
    """Health check endpoint"""
    return web.Response(
        text="Teams Bot is running! Use POST /api/messages for Bot Framework requests.",
        status=200
    )


async def messages(req: web.Request) -> web.Response:
    """
    Handle incoming HTTP requests from Teams/Agents Playground.
    This is the webhook endpoint.
    """
    if req.method != "POST":
        return web.Response(status=405)
    
    body = await req.json()
    activity = Activity().deserialize(body)
    auth_header = req.headers.get("Authorization", "")
    
    async def aux_func(turn_context: TurnContext):
        if turn_context.activity.type == ActivityTypes.message:
            await on_message_activity(turn_context)
        elif turn_context.activity.type == ActivityTypes.conversation_update:
            if turn_context.activity.members_added:
                await on_members_added_activity(
                    turn_context.activity.members_added,
                    turn_context
                )
    
    try:
        await ADAPTER.process_activity(activity, auth_header, aux_func)
        return web.Response(status=200)
    except Exception as e:
        print(f"❌ Error processing activity: {str(e)}")
        return web.Response(status=500, text=str(e))


def init_func():
    """Initialize the web application"""
    app = web.Application()
    app.router.add_get("/", health_check)
    app.router.add_get("/api/messages", health_check)
    app.router.add_post("/api/messages", messages)
    return app


if __name__ == "__main__":
    app = init_func()
    port = 3978
    
    print("=" * 60)
    print("🤖 Teams Bot Running")
    print("=" * 60)
    print(f"📍 Listening on: http://localhost:{port}/api/messages")
    print()
    print("🧪 To test:")
    print("1. Open Agents Playground")
    print(f"2. Connect to: http://localhost:{port}/api/messages")
    print("3. Start chatting!")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    web.run_app(app, port=port)

