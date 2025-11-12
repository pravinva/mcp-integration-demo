"""
Full CLI demonstrating ALL 3 MCP servers with ONE client!

This is the complete M×N demonstration:
- 1 platform (CLI)
- 3 data sources (Genie, Vector Search, UC Functions)
- 1 integration (shared/mcp_client.py)
"""

import asyncio
import sys
from pathlib import Path

# Add project root to path
project_root = Path(__file__).parent.parent.parent
sys.path.insert(0, str(project_root))

from shared.mcp_client import create_mcp_client
from shared.config import (
    GENIE_SPACE_ID, 
    VECTOR_SEARCH_INDEX_ID, 
    UC_FUNCTION_NAME,
    validate_config
)


async def main():
    print("=" * 70)
    print("�� Databricks MCP - Multi-Service Demo")
    print("=" * 70)
    print()
    print("This demo shows ONE MCP client talking to THREE data sources!")
    print()
    print("Available commands:")
    print("  /genie <question>    - Ask Genie about your data")
    print("  /search <query>      - Search documentation (Vector Search)")
    print("  /function <params>   - Execute UC Function")
    print("  /demo                - Run full demo sequence")
    print("  /exit                - Quit")
    print("-" * 70)
    
    try:
        validate_config()
    except ValueError as e:
        print(f"❌ Configuration error: {e}")
        print("\nSet USE_MOCK_MCP=true in .env to run without Databricks")
        return
    
    client = create_mcp_client()
    conversation_id = None
    
    while True:
        try:
            command = input("\n🧑 You: ").strip()
            
            if not command:
                continue
            
            if command.lower() in ['/exit', 'exit', 'quit']:
                print("👋 Goodbye!")
                break
            
            # Demo sequence - shows all 3 data sources!
            if command.lower() == '/demo':
                print("\n" + "=" * 70)
                print("📺 RUNNING FULL DEMO - ONE CLIENT, THREE DATA SOURCES")
                print("=" * 70 + "\n")
                
                # 1. Query Genie (Analytics)
                print("1️⃣  GENIE - Natural Language Analytics")
                print("-" * 70)
                print("Asking: 'What was our total revenue in Q4 2024?'\n")
                
                response, conversation_id = await client.ask_genie(
                    GENIE_SPACE_ID,
                    "What was our total revenue in Q4 2024?"
                )
                print(f"🧞 Genie Response:")
                print(response[:300] + "...\n" if len(response) > 300 else response + "\n")
                
                # 2. Search docs (Vector Search)
                print("\n2️⃣  VECTOR SEARCH - Documentation Retrieval")
                print("-" * 70)
                print("Searching: 'How to create a Genie space?'\n")
                
                docs = await client.search_docs(
                    VECTOR_SEARCH_INDEX_ID,
                    "How to create a Genie space?",
                    num_results=2
                )
                print(f"📚 Search Results:")
                print(docs[:300] + "...\n" if len(docs) > 300 else docs + "\n")
                
                # 3. Call function (UC Functions)
                print("\n3️⃣  UC FUNCTIONS - Governed Code Execution")
                print("-" * 70)
                print("Executing: calculate_discount(50000, 'Enterprise')\n")
                
                result = await client.call_function(
                    UC_FUNCTION_NAME,
                    {"order_amount": 50000.0, "customer_segment": "Enterprise"}
                )
                print(f"💰 Function Result:")
                print(result + "\n")
                
                print("=" * 70)
                print("✅ DEMO COMPLETE!")
                print("=" * 70)
                print("\nKey Insight: The SAME client (shared/mcp_client.py) talked to")
                print("all three data sources. That's M+N in action!\n")
                continue
            
            # Genie query
            if command.startswith('/genie '):
                question = command[7:]
                print("🤔 Asking Genie...")
                response, conversation_id = await client.ask_genie(
                    GENIE_SPACE_ID, 
                    question, 
                    conversation_id
                )
                print(f"\n🧞 Genie:\n{response}")
            
            # Vector search
            elif command.startswith('/search '):
                query = command[8:]
                print("🔍 Searching documentation...")
                results = await client.search_docs(
                    VECTOR_SEARCH_INDEX_ID, 
                    query,
                    num_results=3
                )
                print(f"\n📚 Search Results:\n{results}")
            
            # UC Function
            elif command.startswith('/function '):
                # Parse: /function 50000 Enterprise
                parts = command[10:].split()
                if len(parts) >= 2:
                    amount = float(parts[0])
                    segment = parts[1]
                    print("⚙️ Executing function...")
                    result = await client.call_function(
                        UC_FUNCTION_NAME,
                        {"order_amount": amount, "customer_segment": segment}
                    )
                    print(f"\n💰 Result:\n{result}")
                else:
                    print("Usage: /function <amount> <segment>")
                    print("Example: /function 50000 Enterprise")
            
            else:
                # Default to Genie
                print("🤔 Asking Genie...")
                response, conversation_id = await client.ask_genie(
                    GENIE_SPACE_ID, 
                    command,
                    conversation_id
                )
                print(f"\n🧞 Genie:\n{response}")
                
        except KeyboardInterrupt:
            print("\n\n👋 Goodbye!")
            break
        except Exception as e:
            print(f"\n❌ Error: {str(e)}")


if __name__ == "__main__":
    asyncio.run(main())

