"""
Configuration management for MCP showcase.
Supports multiple authentication methods:
1. ~/.databrickscfg (easiest for testing)
2. Environment variables (.env file)
3. OAuth credentials
"""

import os
from databricks.sdk import WorkspaceClient
from databricks.sdk.core import Config
from dotenv import load_dotenv
import logging

load_dotenv()
logging.basicConfig(level=logging.INFO)
logger = logging.getLogger(__name__)

# Databricks Configuration
DATABRICKS_HOST = os.getenv("DATABRICKS_HOST")
GENIE_SPACE_ID = os.getenv("GENIE_SPACE_ID")
VECTOR_SEARCH_INDEX_ID = os.getenv("VECTOR_SEARCH_INDEX_ID", "demo_retail.ecommerce.documentation_index")
VECTOR_SEARCH_ENDPOINT = os.getenv("VECTOR_SEARCH_ENDPOINT", "one-env-shared-endpoint-10")
UC_FUNCTION_NAME = os.getenv("UC_FUNCTION_NAME", "demo_retail.ecommerce.calculate_discount")

# OAuth Configuration (optional)
OAUTH_CLIENT_ID = os.getenv("DATABRICKS_OAUTH_CLIENT_ID")
OAUTH_CLIENT_SECRET = os.getenv("DATABRICKS_OAUTH_CLIENT_SECRET")

# Databricks CLI profile (from ~/.databrickscfg)
DATABRICKS_PROFILE = os.getenv("DATABRICKS_PROFILE", "DEFAULT")

# Slack Configuration
SLACK_BOT_TOKEN = os.getenv("SLACK_BOT_TOKEN")
SLACK_APP_TOKEN = os.getenv("SLACK_APP_TOKEN")

# Teams Configuration
MICROSOFT_APP_ID = os.getenv("MICROSOFT_APP_ID")
MICROSOFT_APP_PASSWORD = os.getenv("MICROSOFT_APP_PASSWORD")

# Feature Flags
USE_MOCK_MCP = os.getenv("USE_MOCK_MCP", "false").lower() == "true"


# Databricks CLI MCP Server URL
DATABRICKS_CLI_MCP_URL = os.getenv(
    "DATABRICKS_CLI_MCP_URL",
    "https://databricks-cli-mcp-1444828305810485.aws.databricksapps.com"
)

# MCP Server URLs - Just configuration!
MCP_SERVERS = {
    "genie": {
        "url": f"{DATABRICKS_HOST}/api/2.0/mcp/genie/{GENIE_SPACE_ID}" if DATABRICKS_HOST else None,
        "tools": ["ask_question", "list_conversations", "provide_feedback"],
        "description": "Natural language analytics"
    },
    "vector_search": {
        # URL format: /api/2.0/mcp/vector-search/{catalog}/{schema}
        # Extract catalog.schema from VECTOR_SEARCH_INDEX_ID
        "url": (f"{DATABRICKS_HOST}/api/2.0/mcp/vector-search/{VECTOR_SEARCH_INDEX_ID.split('.')[0]}/{VECTOR_SEARCH_INDEX_ID.split('.')[1]}" 
                if DATABRICKS_HOST and '.' in VECTOR_SEARCH_INDEX_ID else None),
        "tools": ["similarity_search", "get_vectors"],
        "description": "Semantic search for RAG"
    },
    "uc_functions": {
        # URL format: /api/2.0/mcp/functions/{catalog}/{schema}
        # Extract catalog.schema from UC_FUNCTION_NAME
        "url": (f"{DATABRICKS_HOST}/api/2.0/mcp/functions/{UC_FUNCTION_NAME.split('.')[0]}/{UC_FUNCTION_NAME.split('.')[1]}"
                if DATABRICKS_HOST and '.' in UC_FUNCTION_NAME else None),
        "tools": ["execute", "describe"],
        "description": "Execute governed Python/SQL functions"
    },
    "databricks_cli": {
        "url": DATABRICKS_CLI_MCP_URL,
        "tools": ["explore_workspace", "invoke_databricks_cli", "query_sql"],
        "description": "Execute Databricks CLI commands and SQL queries"
    }
}


def get_workspace_client() -> WorkspaceClient:
    """
    Create authenticated Databricks workspace client.
    
    Authentication priority:
    1. OAuth credentials (if provided in .env)
    2. Profile from ~/.databrickscfg (easiest for CLI testing)
    3. Environment variables (DATABRICKS_HOST + DATABRICKS_TOKEN)
    
    Returns:
        WorkspaceClient: Authenticated client
    """
    if USE_MOCK_MCP:
        logger.info("🧪 Using MOCK mode - no real Databricks connection")
        return None
    
    # Option 1: OAuth (best for production)
    if OAUTH_CLIENT_ID and OAUTH_CLIENT_SECRET:
        logger.info("🔐 Using OAuth authentication")
        if not DATABRICKS_HOST:
            raise ValueError("DATABRICKS_HOST required for OAuth authentication")
        return WorkspaceClient(
            host=DATABRICKS_HOST,
            client_id=OAUTH_CLIENT_ID,
            client_secret=OAUTH_CLIENT_SECRET
        )
    
    # Option 2: Profile from ~/.databrickscfg (easiest for testing!)
    if not DATABRICKS_HOST or not OAUTH_CLIENT_ID:
        logger.info(f"🔑 Using Databricks CLI profile: {DATABRICKS_PROFILE}")
        logger.info(f"📁 Reading from: ~/.databrickscfg")
        
        try:
            # Let SDK read from ~/.databrickscfg automatically
            client = WorkspaceClient(profile=DATABRICKS_PROFILE)
            
            # Verify connection
            current_user = client.current_user.me()
            logger.info(f"✅ Connected as: {current_user.user_name}")
            logger.info(f"📍 Workspace: {client.config.host}")
            
            # Update DATABRICKS_HOST if not set
            if not DATABRICKS_HOST:
                # Use module-level variable update
                import shared.config as config_module
                config_module.DATABRICKS_HOST = client.config.host
                logger.info(f"🔄 Auto-detected host: {client.config.host}")
            
            return client
            
        except Exception as e:
            logger.error(f"❌ Failed to connect using profile '{DATABRICKS_PROFILE}'")
            logger.error(f"Error: {str(e)}")
            logger.info("\n💡 Quick Fix:")
            logger.info("1. Run: databricks configure --token")
            logger.info("2. Or create ~/.databrickscfg manually (see docs/setup-guide.md)")
            raise
    
    # Option 3: Explicit credentials (fallback)
    if DATABRICKS_HOST and os.getenv("DATABRICKS_TOKEN"):
        logger.info("🔑 Using explicit token from environment")
        return WorkspaceClient(
            host=DATABRICKS_HOST,
            token=os.getenv("DATABRICKS_TOKEN")
        )
    
    raise ValueError(
        "No authentication method available!\n"
        "Options:\n"
        "1. Use ~/.databrickscfg (run: databricks configure --token)\n"
        "2. Set DATABRICKS_OAUTH_CLIENT_ID + DATABRICKS_OAUTH_CLIENT_SECRET\n"
        "3. Set DATABRICKS_HOST + DATABRICKS_TOKEN\n"
        "4. Set USE_MOCK_MCP=true for offline testing"
    )


def validate_config():
    """Validate required configuration on startup"""
    
    if USE_MOCK_MCP:
        logger.info("🧪 Mock mode enabled - skipping validation")
        return
    
    # Check if we can connect
    try:
        client = get_workspace_client()
        
        # Validate Genie Space ID is set
        if not GENIE_SPACE_ID:
            logger.warning("⚠️  GENIE_SPACE_ID not set - you'll need this for Genie queries")
            logger.info("Set it in .env or pass as argument")
        
        logger.info("✅ Configuration valid and connected!")
        
    except Exception as e:
        logger.error(f"❌ Configuration validation failed: {str(e)}")
        raise

