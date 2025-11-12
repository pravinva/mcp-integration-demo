"""
Simple CLI to demo Genie MCP.
Run this FIRST to verify MCP connection works!
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from shared.mcp_client import create_mcp_client
from shared.config import GENIE_SPACE_ID, validate_config


async def main():
    print("=" * 60)
    print("🧞 Databricks Genie MCP - Command Line Interface")
    print("=" * 60)
    print()
    
    # Validate configuration
    try:
        validate_config()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nCreate a .env file based on .env.example")
        return
    
    # Create MCP client
    client = create_mcp_client()
    
    print("✅ Connected to Databricks")
    print(f"📊 Genie Space: {GENIE_SPACE_ID}")
    print()
    print("Type your questions (or 'exit' to quit, 'reset' for new conversation):")
    print("-" * 60)
    
    conversation_id = None
    
    while True:
        try:
            # Get user input
            question = input("\n🧑 You: ").strip()
            
            if not question:
                continue
            
            if question.lower() in ['exit', 'quit', 'q']:
                print("\n👋 Goodbye!")
                break
            
            if question.lower() in ['reset', 'new']:
                conversation_id = None
                print("🔄 Conversation reset")
                continue
            
            # Query Genie via MCP
            print("🤔 Thinking...")
            response, conversation_id = await client.ask_genie(
                GENIE_SPACE_ID,
                question,
                conversation_id
            )
            
            # Display response
            print(f"\n🧞 Genie:\n{response}")
            
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())

