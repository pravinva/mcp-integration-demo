"""
Shared MCP integration components.
This is where the M×N → M+N transformation happens!
"""

from .mcp_client import UniversalMCPClient, create_mcp_client
from .config import MCP_SERVERS, get_workspace_client

__all__ = [
    'UniversalMCPClient',
    'create_mcp_client',
    'MCP_SERVERS',
    'get_workspace_client'
]

