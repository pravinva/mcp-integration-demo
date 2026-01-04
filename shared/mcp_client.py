"""
Universal Databricks MCP Client

THE CORE INTEGRATION - This ONE file talks to ALL Databricks MCP servers!

Used by:
- CLI (demos/01-cli/)
- Claude Desktop (demos/04-claude/)
- Slack bot (demos/02-slack/)
- Teams bot (demos/03-teams/)

This is the M+N solution: ONE integration, MULTIPLE platforms!
"""

from typing import Optional, Dict, Any
from databricks.sdk import WorkspaceClient
from databricks_mcp import DatabricksMCPClient
import logging

logger = logging.getLogger(__name__)


class UniversalMCPClient:
    """
    The MAGIC: This ONE class talks to ALL Databricks MCP servers.

    Supports:
    - Genie (analytics)
    - Vector Search (RAG)
    - Unity Catalog Functions (actions)

    Same query() method works for all three!

    Example:
        client = UniversalMCPClient(workspace_client)

        # Query Genie
        result = await client.ask_genie(space_id, "What was revenue?")

        # Search docs
        docs = await client.search_docs(index_id, "MCP tutorial")

        # Execute function
        output = await client.call_function(func_name, {"param": "value"})
    """

    def __init__(self, workspace_client: WorkspaceClient):
        """
        Initialize with authenticated workspace client.

        Args:
            workspace_client: WorkspaceClient with OAuth or PAT auth
        """
        self.workspace_client = workspace_client
        # Use asyncio.Lock to serialize MCP requests and prevent TaskGroup conflicts
        # This ensures only one MCP call happens at a time, avoiding background task interference
        import asyncio
        self._lock = asyncio.Lock()
        logger.info("✅ Universal MCP Client initialized")
    
    async def query(
        self, 
        server_url: str, 
        tool_name: str, 
        arguments: Dict[str, Any]
    ) -> str:
        """
        Universal query method - works with ANY MCP server!
        
        This is the breakthrough: SAME method for Genie, Vector Search, UC Functions.
        Only the server_url and tool_name change - the protocol is identical.
        
        Args:
            server_url: MCP server endpoint
            tool_name: Tool to call (e.g., "ask_question", "similarity_search")
            arguments: Tool-specific arguments
            
        Returns:
            Response text from MCP server
            
        Examples:
            # Query Genie
            await query(
                "https://xxx.databricks.com/api/2.0/mcp/genie/space123",
                "ask_question",
                {"question": "What was revenue?"}
            )
            
            # Search docs (Vector Search)
            await query(
                "https://xxx.databricks.com/api/2.0/mcp/vector-search/catalog/schema",
                "similarity_search",
                {"query": "How to deploy?", "num_results": 3}
            )
            
            # Execute function (UC Functions)
            await query(
                "https://xxx.databricks.com/api/2.0/mcp/functions/catalog/schema",
                "execute",
                {"param1": "value1"}
            )
        """
        # CRITICAL: Use lock to serialize all MCP requests
        # This prevents TaskGroup conflicts when multiple requests overlap
        # The anyio TaskGroups used by the MCP library don't handle concurrent cleanup well
        async with self._lock:
            logger.debug("🔒 Acquired MCP lock")
            mcp_client = None
            try:
                logger.info(f"🔍 Querying {tool_name} on {server_url}")

                # Create a NEW MCP client for each request
                # This avoids async context issues that occur when reusing cached clients
                # The DatabricksMCPClient internally uses async operations that don't
                # play well with thread pool executors when reused
                logger.debug(f"Creating new MCP client for {server_url}")
                mcp_client = DatabricksMCPClient(
                    server_url=server_url,
                    workspace_client=self.workspace_client
                )

                # For Genie, the tool name might be dynamically generated
                # Try to discover tools if the tool_name doesn't work
                # NOTE: Skip tool discovery to avoid async context issues - use constructed names instead
                if tool_name.startswith("ask_question") or tool_name == "ask_question":
                    # Construct tool name from space_id in URL instead of discovering
                    if "/mcp/genie/" in server_url:
                        space_id = server_url.split("/mcp/genie/")[-1]
                        tool_name = f"query_space_{space_id}"
                        logger.info(f"🔄 Using constructed tool name: {tool_name}")

                # For Vector Search and UC Functions, use the provided tool_name
                # Skip discovery to avoid async context issues with list_tools()
                # The tool_name should already be in the correct format: catalog__schema__function_name
                if tool_name in ["similarity_search", "execute"]:
                    logger.debug(f"⚠️ Generic tool name '{tool_name}' - tool discovery skipped to avoid async issues")
                    logger.debug(f"   Make sure tool_name is fully qualified (e.g., catalog__schema__function)")

                # Execute query via MCP protocol
                # The databricks_mcp library has both sync and async methods:
                # - call_tool() is sync but internally calls asyncio.run() which fails in async contexts
                # - _call_tools_async() is the actual async implementation
                # We need to call the async method directly since we're already in an async function
                #
                # IMPORTANT: Wrap in wait_for with timeout to ensure proper completion
                # and handle TaskGroup errors that can occur with background tasks
                logger.debug(f"Calling tool async: {tool_name}")

                try:
                    import asyncio
                    # Use wait_for with a reasonable timeout (60 seconds for Genie queries)
                    # This ensures the call completes and background tasks are properly cleaned up
                    result = await asyncio.wait_for(
                        mcp_client._call_tools_async(tool_name, arguments),
                        timeout=60.0
                    )
                except asyncio.TimeoutError:
                    logger.error("❌ MCP call timed out after 60 seconds")
                    return "Error: Query timed out after 60 seconds. Please try a simpler question."
                except asyncio.CancelledError:
                    logger.warning("⚠️ MCP call was cancelled")
                    raise
                except Exception as call_error:
                    # Log the detailed error
                    logger.error(f"❌ Error calling _call_tools_async: {call_error}")
                    import traceback
                    logger.error(traceback.format_exc())
                    raise
                finally:
                    # Give a small delay to allow background cleanup tasks to complete
                    # This helps prevent TaskGroup errors on subsequent calls
                    await asyncio.sleep(0.1)

                # Extract response
                if result.content and len(result.content) > 0:
                    response_text = result.content[0].text
                    logger.info(f"✅ Got response ({len(response_text)} chars)")
                    logger.debug("🔓 Releasing MCP lock")
                    return response_text
                else:
                    logger.warning("⚠️ Empty response from MCP server")
                    logger.debug("🔓 Releasing MCP lock")
                    return "No response received"

            except Exception as e:
                error_msg = str(e)
                logger.error(f"❌ MCP query failed: {error_msg}")
                logger.debug("🔓 Releasing MCP lock (error path)")
                import traceback
                full_traceback = traceback.format_exc()
                logger.debug(full_traceback)

                # Extract the actual MCP error from nested exception groups
                # Python 3.11+ wraps exceptions in ExceptionGroup/TaskGroup
                actual_error = e
                if hasattr(e, 'exceptions') and e.exceptions:
                    # Unwrap ExceptionGroup to find the root cause
                    for nested_exc in e.exceptions:
                        if hasattr(nested_exc, 'exceptions') and nested_exc.exceptions:
                            # Nested exception group - go deeper
                            for inner_exc in nested_exc.exceptions:
                                actual_error = inner_exc
                                break
                        else:
                            actual_error = nested_exc
                        break

                # Check if it's an MCP error with a better message
                actual_msg = str(actual_error)
                if "McpError" in actual_msg or "PERMISSION_DENIED" in actual_msg:
                    # Extract the specific error message
                    if "does not own conversation" in actual_msg:
                        return "Error: Conversation expired. Please start a new conversation."
                    else:
                        return f"Error: {actual_msg}"

                # Try to extract more details from the exception
                if hasattr(e, '__cause__') and e.__cause__:
                    error_msg += f"\nCause: {str(e.__cause__)}"
                return f"Error: {error_msg}"
    
    # Convenience methods for each data source
    # These just wrap query() with the right URLs and arguments
    
    async def ask_genie(
        self, 
        space_id: str, 
        question: str, 
        conversation_id: Optional[str] = None
    ) -> tuple[str, str]:
        """
        Query Genie for analytics.
        
        Args:
            space_id: Genie space ID
            question: Natural language question
            conversation_id: Optional conversation ID for multi-turn context
            
        Returns:
            (response_text, conversation_id)
        """
        from shared.config import DATABRICKS_HOST
        
        server_url = f"{DATABRICKS_HOST}/api/2.0/mcp/genie/{space_id}"
        
        # The actual tool name is dynamically generated: query_space_{space_id}
        tool_name = f"query_space_{space_id}"
        
        # Genie MCP uses "query" parameter, not "question"
        arguments = {"query": question}
        if conversation_id:
            arguments["conversation_id"] = conversation_id
        
        # Uses the universal query() method!
        response = await self.query(server_url, tool_name, arguments)

        # Extract conversation ID from Genie response
        # Genie responses are JSON with a "conversation_id" field
        try:
            import json
            response_json = json.loads(response)
            new_conv_id = response_json.get("conversation_id")
            logger.debug(f"Extracted conversation ID: {new_conv_id}")
        except (json.JSONDecodeError, AttributeError, KeyError):
            # If response is not JSON or doesn't have conversation_id, don't use one
            # This makes each query independent (stateless)
            logger.warning("Could not extract conversation ID from response - using stateless mode")
            new_conv_id = None

        return response, new_conv_id
    
    async def search_docs(
        self, 
        index_id: str, 
        query: str, 
        num_results: int = 3
    ) -> str:
        """
        Search documentation using Vector Search.
        
        Args:
            index_id: Vector Search index ID (can be full name like "catalog.schema.index" 
                     or just catalog.schema - catalog and schema will be extracted)
            query: Search query
            num_results: Number of results to return
            
        Returns:
            Formatted search results
        """
        from shared.config import DATABRICKS_HOST
        
        # Extract catalog and schema from index_id
        # Format: catalog.schema.index or catalog.schema
        parts = index_id.split('.')
        if len(parts) >= 2:
            catalog = parts[0]
            schema = parts[1]
            index_name = parts[2] if len(parts) > 2 else None
        else:
            raise ValueError(f"Invalid index_id format: {index_id}. Expected 'catalog.schema' or 'catalog.schema.index'")
        
        # Correct URL format: /api/2.0/mcp/vector-search/{catalog}/{schema}
        server_url = f"{DATABRICKS_HOST}/api/2.0/mcp/vector-search/{catalog}/{schema}"
        
        # The tool name is dynamically generated: catalog__schema__index_name
        # We'll discover it, but if index name is provided, construct it
        if index_name:
            # Convert catalog.schema.index to catalog__schema__index format
            tool_name = f"{catalog}__{schema}__{index_name}"
        else:
            # Use "similarity_search" as placeholder - will be discovered
            tool_name = "similarity_search"
        
        arguments = {
            "query": query,
            "num_results": num_results
        }
        
        # Uses the SAME query() method!
        return await self.query(server_url, tool_name, arguments)
    
    async def call_function(
        self, 
        function_name: str, 
        parameters: Dict[str, Any]
    ) -> str:
        """
        Execute Unity Catalog Function.
        
        Args:
            function_name: Fully qualified function name (catalog.schema.function)
                          catalog and schema will be extracted for the URL
                          The actual tool name will be discovered dynamically
            parameters: Function parameters
            
        Returns:
            Function execution result
        """
        from shared.config import DATABRICKS_HOST
        
        # Extract catalog and schema from function_name
        # Format: catalog.schema.function
        parts = function_name.split('.')
        if len(parts) >= 2:
            catalog = parts[0]
            schema = parts[1]
            function = parts[2] if len(parts) > 2 else None
        else:
            raise ValueError(f"Invalid function_name format: {function_name}. Expected 'catalog.schema.function'")
        
        # Correct URL format: /api/2.0/mcp/functions/{catalog}/{schema}
        server_url = f"{DATABRICKS_HOST}/api/2.0/mcp/functions/{catalog}/{schema}"
        
        # The tool name is dynamically generated: catalog__schema__function_name
        # We'll discover it, but if function name is provided, construct it
        if function:
            # Convert catalog.schema.function to catalog__schema__function format
            tool_name = f"{catalog}__{schema}__{function}"
        else:
            # Use "execute" as placeholder - will be discovered
            tool_name = "execute"
        
        # Uses the SAME query() method again!
        return await self.query(server_url, tool_name, parameters)

    async def explore_workspace(self) -> str:
        """
        Explore Databricks workspace to discover available resources.

        Returns:
            JSON string with workspace information including:
            - Catalogs and schemas
            - Clusters
            - Jobs
            - SQL Warehouses
        """
        from shared.config import DATABRICKS_CLI_MCP_URL
        import httpx

        logger.info("🔍 Exploring Databricks workspace...")

        try:
            # Get auth token from workspace client
            auth_header = self.workspace_client.config.authenticate()

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{DATABRICKS_CLI_MCP_URL}/mcp/explore",
                    headers={"Authorization": auth_header.get("Authorization")},
                    timeout=30.0
                )
                response.raise_for_status()
                result = response.json()

                logger.info(f"✅ Workspace explored successfully")
                return result.get("content", [{}])[0].get("text", "No data")

        except Exception as e:
            logger.error(f"❌ Failed to explore workspace: {str(e)}")
            return f"Error exploring workspace: {str(e)}"

    async def invoke_databricks_cli(
        self,
        category: str,
        args: list[str]
    ) -> str:
        """
        Execute Databricks CLI commands.

        Args:
            category: CLI category (e.g., "clusters", "jobs", "warehouses")
            args: Command arguments (e.g., ["list"], ["get", "--id", "123"])

        Returns:
            CLI command output

        Examples:
            # List clusters
            await invoke_databricks_cli("clusters", ["list"])

            # Get job details
            await invoke_databricks_cli("jobs", ["get", "--id", "123"])

            # List SQL warehouses
            await invoke_databricks_cli("warehouses", ["list"])
        """
        from shared.config import DATABRICKS_CLI_MCP_URL
        import httpx

        logger.info(f"🔧 Invoking Databricks CLI: {category} {' '.join(args)}")

        try:
            # Get auth token from workspace client
            auth_header = self.workspace_client.config.authenticate()

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{DATABRICKS_CLI_MCP_URL}/mcp/invoke",
                    headers={"Authorization": auth_header.get("Authorization")},
                    json={
                        "name": "invoke_databricks_cli",
                        "arguments": {
                            "category": category,
                            "args": args
                        }
                    },
                    timeout=30.0
                )
                response.raise_for_status()
                result = response.json()

                logger.info(f"✅ CLI command executed successfully")
                return result.get("content", [{}])[0].get("text", "No output")

        except Exception as e:
            logger.error(f"❌ CLI command failed: {str(e)}")
            return f"Error: {str(e)}"

    async def query_sql(
        self,
        warehouse_id: str,
        query: str
    ) -> str:
        """
        Execute SQL query using SQL Warehouse.

        Args:
            warehouse_id: SQL Warehouse ID
            query: SQL query to execute

        Returns:
            Query results as formatted string

        Example:
            await query_sql("abc123", "SELECT * FROM main.sales LIMIT 10")
        """
        from shared.config import DATABRICKS_CLI_MCP_URL
        import httpx

        logger.info(f"🗃️ Executing SQL query: {query[:100]}...")

        try:
            # Get auth token from workspace client
            auth_header = self.workspace_client.config.authenticate()

            async with httpx.AsyncClient() as client:
                response = await client.post(
                    f"{DATABRICKS_CLI_MCP_URL}/mcp/invoke",
                    headers={"Authorization": auth_header.get("Authorization")},
                    json={
                        "name": "execute_parameterized_sql",
                        "arguments": {
                            "warehouse_id": warehouse_id,
                            "query": query
                        }
                    },
                    timeout=60.0
                )
                response.raise_for_status()
                result = response.json()

                logger.info(f"✅ SQL query executed successfully")
                return result.get("content", [{}])[0].get("text", "No results")

        except Exception as e:
            logger.error(f"❌ SQL query failed: {str(e)}")
            return f"Error: {str(e)}"


def create_mcp_client() -> UniversalMCPClient:
    """
    Factory function to create MCP client with proper auth.
    
    Returns:
        Configured UniversalMCPClient or MockMCPClient (if USE_MOCK_MCP=true)
    """
    from shared.config import USE_MOCK_MCP, get_workspace_client
    
    if USE_MOCK_MCP:
        logger.info("🧪 Creating MOCK MCP client")
        from shared.mock_mcp_client import MockMCPClient
        return MockMCPClient()
    
    workspace_client = get_workspace_client()
    return UniversalMCPClient(workspace_client)

