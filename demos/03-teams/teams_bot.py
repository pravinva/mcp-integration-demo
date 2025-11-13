"""
Microsoft Teams bot using Databricks Genie MCP.

Notice: Uses the SAME shared/mcp_client.py as Slack bot!
This demonstrates 80% code reuse.

Testing: Microsoft 365 Agents Playground (recommended)
         Bot Framework Emulator (deprecated, retiring 2025)
Production: Azure Functions (requires Azure subscription)
"""

import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from aiohttp import web
from botbuilder.core import (
    BotFrameworkAdapter,
    BotFrameworkAdapterSettings,
    TurnContext
)
from botbuilder.schema import Activity, ActivityTypes
import asyncio

from shared.mcp_client import create_mcp_client
from shared.config import (
    MICROSOFT_APP_ID,
    MICROSOFT_APP_PASSWORD,
    GENIE_SPACE_ID,
    VECTOR_SEARCH_INDEX_ID,
    UC_FUNCTION_NAME
)
from shared.genie_formatter import format_genie_response, format_uc_function_response, format_vector_search_response

# Bot Framework Adapter
SETTINGS = BotFrameworkAdapterSettings(
    MICROSOFT_APP_ID or "",  # Empty for local testing
    MICROSOFT_APP_PASSWORD or ""
)
# Set service URL for Agents Playground (required for local testing)
SETTINGS.service_url = "http://localhost:3978"
ADAPTER = BotFrameworkAdapter(SETTINGS)

# MCP client - THE SAME ONE as Slack!
mcp_client = create_mcp_client()

# Conversation storage
conversations = {}


async def on_message_activity(turn_context: TurnContext):
    """
    Handle incoming messages from Teams.
    
    Supports:
    - Analytics questions (Genie)
    - Document search (Vector Search)
    - Function execution (UC Functions)
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

**🔍 Search Docs (Vector Search):**
Start with "search":
- "search how to create Genie space"
- "search MCP tutorial"

**💰 Calculate (UC Functions):**
Start with "calculate":
- "calculate 50000 Enterprise"
- "calculate 25000 SMB"

**Commands:**
- `/reset` - New conversation
- `/help` - This message"""
        
        await turn_context.send_activity(help_text)
        return
    
    # Show typing indicator
    await turn_context.send_activity(Activity(type=ActivityTypes.typing))
    
    # Initialize response variables
    response = None
    prefix = None
    
    try:
        # Route based on message content
        if user_message.lower().startswith("search "):
            # Vector Search
            try:
                query = user_message[7:]
                raw_response = await mcp_client.search_docs(
                    VECTOR_SEARCH_INDEX_ID,
                    query,
                    num_results=3
                )
                # Format the vector search response using shared formatter
                response = format_vector_search_response(raw_response, platform="teams")
                prefix = "📚 **Search Results:**\n\n"
            except Exception as search_error:
                import traceback
                print(f"❌ Error in search: {str(search_error)}")
                traceback.print_exc()
                response = f"Error searching: {str(search_error)}"
                prefix = "❌ **Error:**\n\n"
        
        elif user_message.lower().startswith(("calculate ", "discount ")):
            # UC Function
            try:
                parts = user_message.split()
                amount = float(parts[1])
                segment = parts[2]
                raw_response = await mcp_client.call_function(
                    UC_FUNCTION_NAME,
                    {"order_amount": amount, "customer_segment": segment}
                )
                # Format the UC function response using shared formatter
                response = format_uc_function_response(raw_response, platform="teams")
                prefix = "💰 **Calculation:**\n\n"
            except (IndexError, ValueError) as parse_error:
                response = "Usage: calculate <amount> <segment>\nExample: calculate 50000 Enterprise"
                prefix = "❌ **Error:**\n\n"
            except Exception as func_error:
                import traceback
                print(f"❌ Error calling function: {str(func_error)}")
                traceback.print_exc()
                response = f"Error calling function: {str(func_error)}"
                prefix = "❌ **Error:**\n\n"
        
        else:
            # Default: Genie analytics
            print(f"🔍 Querying Genie: {user_message}")
            print(f"📊 Genie Space ID: {GENIE_SPACE_ID}")
            conv_id = conversations.get(conv_key)
            
            try:
                raw_response, new_conv_id = await mcp_client.ask_genie(
                    GENIE_SPACE_ID,
                    user_message,
                    conv_id
                )
                conversations[conv_key] = new_conv_id
                
                # Check if response is an error
                if raw_response.startswith("Error:"):
                    response = raw_response
                    prefix = "❌ **Error:**\n\n"
                else:
                    # Format the Genie response using shared formatter
                    response = format_genie_response(raw_response, platform="teams")
                    prefix = "🧞 **Genie:**\n\n"
                
                print(f"✅ Got Genie response: {raw_response[:100]}...")
                print(f"✅ Formatted response: {response[:100]}...")
            except Exception as genie_error:
                import traceback
                error_details = traceback.format_exc()
                print(f"❌ Error querying Genie: {str(genie_error)}")
                print(error_details)
                response = f"Error querying Genie: {str(genie_error)}"
                prefix = "❌ **Error:**\n\n"
        
        # Ensure we have a response
        if response is None or prefix is None:
            response = "Sorry, I couldn't process your request. Please try again."
            prefix = "❌ **Error:**\n\n"
        
        # Format and send response
        full_response = prefix + response
        print(f"📤 Sending response: {full_response[:100]}...")
        
        try:
            await turn_context.send_activity(full_response)
        except Exception as send_error:
            import traceback
            send_error_details = traceback.format_exc()
            print(f"❌ Error sending activity: {str(send_error)}")
            print(send_error_details)
            # Try to send a simpler error message
            try:
                await turn_context.send_activity(f"❌ Error sending response: {str(send_error)}")
            except:
                print("❌ Failed to send error message - check service_url configuration")
        
    except Exception as e:
        import traceback
        error_details = traceback.format_exc()
        print(f"❌ Error in on_message_activity: {str(e)}")
        print(error_details)
        try:
            error_msg = f"❌ Sorry, I encountered an error: {str(e)}\n\nPlease check the bot logs for details."
            await turn_context.send_activity(error_msg)
        except Exception as send_error:
            print(f"❌ Failed to send error message: {str(send_error)}")


async def on_members_added_activity(members_added, turn_context: TurnContext):
    """Welcome message when bot is added"""
    for member in members_added:
        if member.id != turn_context.activity.recipient.id:
            welcome = """👋 **Welcome to Databricks Genie!**

I can help you with:
📊 Data analytics (ask natural language questions)
🔍 Documentation search (start with "search")
💰 Calculations (start with "calculate")

Try asking:
- "What was our revenue last quarter?"
- "search MCP integration guide"
- "calculate 50000 Enterprise"

Type `/help` for more information."""
            
            await turn_context.send_activity(welcome)


async def health_check(req: web.Request) -> web.Response:
    """Health check endpoint - responds to GET requests"""
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
    
    # Set service URL for Agents Playground (required for local testing)
    if not activity.service_url:
        activity.service_url = "http://localhost:3978"
    
    auth_header = req.headers.get("Authorization", "")
    
    async def aux_func(turn_context: TurnContext):
        # Ensure service URL is set for Agents Playground
        if not turn_context.activity.service_url:
            turn_context.activity.service_url = "http://localhost:3978"
        
        try:
            if turn_context.activity.type == ActivityTypes.message:
                await on_message_activity(turn_context)
            elif turn_context.activity.type == ActivityTypes.conversation_update:
                if turn_context.activity.members_added:
                    await on_members_added_activity(
                        turn_context.activity.members_added,
                        turn_context
                    )
        except Exception as e:
            # Catch any errors in the async handler
            import traceback
            error_details = traceback.format_exc()
            print(f"❌ Error in aux_func: {str(e)}")
            print(error_details)
            # Don't re-raise - let Bot Framework handle it
            try:
                await turn_context.send_activity(
                    f"❌ Sorry, I encountered an error: {str(e)}\n\nPlease check the bot logs for details."
                )
            except Exception as send_error:
                print(f"❌ Failed to send error message: {str(send_error)}")
            # Re-raise to let Bot Framework know there was an error
            raise
    
    try:
        await ADAPTER.process_activity(activity, auth_header, aux_func)
        return web.Response(status=200)
    except Exception as e:
        print(f"❌ Error processing activity: {str(e)}")
        import traceback
        traceback.print_exc()
        return web.Response(status=500, text=str(e))


def init_func():
    """Initialize the web application"""
    app = web.Application()
    app.router.add_get("/", health_check)  # Health check endpoint
    app.router.add_get("/api/messages", health_check)  # Health check for GET requests
    app.router.add_post("/api/messages", messages)  # Bot Framework endpoint
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
    print("1. Open Bot Framework Emulator")
    print(f"2. Connect to: http://localhost:{port}/api/messages")
    print("3. Start chatting!")
    print()
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    web.run_app(app, port=port)

