# Step 4: Implement the Bot

Now you'll write the Slack bot code that connects to Genie via MCP.

## Project Structure

```
tutorials/genie-integration/05-slack-integration/
├── code/
│   ├── slack_bot.py          # Main bot code
│   └── requirements.txt       # Dependencies
└── [tutorial files]
```

## Step 1: Create Requirements File

Create `code/requirements.txt`:

```txt
slack-bolt>=1.18.0
databricks-sdk>=0.20.0
databricks-mcp>=0.1.0
python-dotenv>=1.0.0
aiohttp>=3.9.0
```

## Step 2: Create the Bot Code

Create `code/slack_bot.py`:

```python
"""
Slack bot using Databricks Genie MCP.

Notice: 80% of the logic is in shared/mcp_client.py!
This is just a thin wrapper around the universal MCP client.
"""

import asyncio
import os
import sys
from pathlib import Path

# Add project root to path (adjust if needed)
project_root = Path(__file__).parent.parent.parent.parent
sys.path.insert(0, str(project_root))

from slack_bolt.async_app import AsyncApp
from slack_bolt.adapter.socket_mode.async_handler import AsyncSocketModeHandler
from shared.mcp_client import create_mcp_client
from shared.config import (
    SLACK_BOT_TOKEN,
    SLACK_APP_TOKEN,
    GENIE_SPACE_ID
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
            formatted.append(f"*SQL Query:*\n```{data['query']}```\n")
        
        # Extract and format results
        if "statement_response" in data and "result" in data["statement_response"]:
            result = data["statement_response"]["result"]
            manifest = data["statement_response"]["manifest"]
            
            if "data_array" in result and result["data_array"]:
                columns = [col["name"] for col in manifest["schema"]["columns"]]
                formatted.append("*Results:*")
                
                for row in result["data_array"]:
                    values = row.get("values", [])
                    row_text = []
                    for i, col_name in enumerate(columns):
                        if i < len(values):
                            value = values[i].get("string_value", "N/A")
                            row_text.append(f"• *{col_name}:* {value}")
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


@app.event("app_mention")
async def handle_mention(event, say):
    """
    Handle @mentions in channels.
    
    Example:
        @Genie Bot what was Q4 revenue?
    """
    # Extract question (remove bot mention)
    question = event["text"].split(">", 1)[-1].strip()
    thread_ts = event.get("thread_ts") or event["ts"]
    
    # Get conversation context
    conv_id = conversations.get(thread_ts)
    
    try:
        # Query Genie via MCP
        response, new_conv_id = await mcp_client.ask_genie(
            GENIE_SPACE_ID,
            question,
            conv_id
        )
        
        # Store conversation ID for context
        conversations[thread_ts] = new_conv_id
        
        # Format response
        formatted_response = format_genie_response(response)
        
        # Send response in thread
        await say(
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"*Q:* {question}"}
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"*Genie:*\n{formatted_response}"}
                }
            ],
            text=f"Genie: {formatted_response}",
            thread_ts=thread_ts
        )
        
    except Exception as e:
        await say(
            blocks=[
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"*Q:* {question}"}
                },
                {"type": "divider"},
                {
                    "type": "section",
                    "text": {"type": "mrkdwn", "text": f"*Error*\n\nSorry, I encountered an error: {str(e)}"}
                }
            ],
            text=f"Error: {str(e)}",
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
        
        # Commands
        if question.lower() in ['/reset', 'reset', 'new']:
            conversations.pop(ts, None)
            await say("Conversation reset! Start fresh with a new question.")
            return
        
        if question.lower() in ['/help', 'help']:
            await say("""*Databricks Genie Bot Commands:*

*Analytics (Genie):*
Ask natural language questions:
• "What was Q4 revenue?"
• "Show me top 5 customers"
• "Compare Q3 vs Q4 performance"

*Commands:*
• `reset` - Start new conversation
• `help` - Show this message

*Tips:*
• Ask follow-up questions to maintain context
• Use @Genie Bot in channels to share with team""")
            return
        
        # Get conversation context
        conv_id = conversations.get(ts)
        
        try:
            # Query Genie via MCP
            response, new_conv_id = await mcp_client.ask_genie(
                GENIE_SPACE_ID,
                question,
                conv_id
            )
            
            # Store conversation ID
            conversations[ts] = new_conv_id
            
            # Format and send response
            formatted_response = format_genie_response(response)
            
            if not formatted_response or not formatted_response.strip():
                formatted_response = "I received your question but got an empty response. Please try again."
            
            await say(text=formatted_response, mrkdwn=True)
            
        except Exception as e:
            await say(f"Sorry, I encountered an error: {str(e)}")


async def main():
    """Start the Slack bot with Socket Mode"""
    print("=" * 60)
    print("Starting Slack Genie Bot...")
    print("=" * 60)
    
    if not SLACK_BOT_TOKEN or not SLACK_APP_TOKEN:
        print("Missing Slack tokens in .env file")
        return
    
    if not GENIE_SPACE_ID:
        print("Missing GENIE_SPACE_ID in .env file")
        return
    
    print("Configuration valid")
    print(f"Genie Space: {GENIE_SPACE_ID}")
    print()
    print("Bot is running... Send a DM or @mention me in a channel!")
    print("Press Ctrl+C to stop")
    print("=" * 60)
    
    handler = AsyncSocketModeHandler(app, SLACK_APP_TOKEN)
    await handler.start_async()


if __name__ == "__main__":
    asyncio.run(main())
```

## Step 3: Configure Event Subscriptions

In your Slack app settings:

1. Go to **"Event Subscriptions"**
2. Enable **"Enable Events"**
3. Under **"Subscribe to bot events"**, add:
   - `app_mention` - For @mentions
   - `message.im` - For direct messages
4. Save changes

**Note:** With Socket Mode, you don't need to set a Request URL.

## Step 4: Install Dependencies

```bash
cd code
pip install -r requirements.txt
```

## Step 5: Update .env File

Make sure your `.env` has:

```bash
# Databricks
DATABRICKS_HOST=https://your-workspace.cloud.databricks.com
GENIE_SPACE_ID=your-space-id
DATABRICKS_TOKEN=your-token

# Slack
SLACK_BOT_TOKEN=xoxb-your-bot-token
SLACK_APP_TOKEN=xapp-your-app-token
```

## Step 6: Run the Bot

```bash
python code/slack_bot.py
```

You should see:
```
============================================================
Starting Slack Genie Bot...
============================================================
Configuration valid
Genie Space: 01f0be3dcc771e60ada71b6ec9f61870

Bot is running... Send a DM or @mention me in a channel!
Press Ctrl+C to stop
============================================================
```

## Step 7: Test the Bot

### Test in Direct Message

1. Open Slack
2. Find your bot in the app list
3. Send a DM: `What tables are available?`
4. Bot should respond with Genie results!

### Test in Channel

1. Go to any channel
2. Type: `@Genie Bot what was Q4 revenue?`
3. Bot should respond in a thread!

## Code Explanation

### Key Components

1. **MCP Client Initialization:**
   ```python
   mcp_client = create_mcp_client()
   ```
   Uses the shared MCP client - same code works for Teams!

2. **Genie Query:**
   ```python
   response, new_conv_id = await mcp_client.ask_genie(
       GENIE_SPACE_ID,
       question,
       conv_id
   )
   ```
   Single method call handles all Genie communication.

3. **Response Formatting:**
   ```python
   formatted_response = format_genie_response(response)
   ```
   Parses Genie's JSON response into Slack-friendly format.

### Conversation Context

The bot maintains conversation context per thread:
- Each thread/DM gets a unique conversation ID
- Follow-up questions use the same conversation ID
- Genie maintains context across turns

## Next Steps

- [Deploy to Databricks Apps](05-deploy-databricks-apps.md) - Production deployment
- [Testing](06-testing.md) - Comprehensive testing guide

