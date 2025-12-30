"""
Gmail MCP Server - Simplified Configuration.
"""

from fastmcp import FastMCP
import os

# Create FastMCP server (No Auth for debugging)
mcp = FastMCP("Gmail MCP Server")

@mcp.tool
def debug_ping() -> str:
    """Simple ping to verify server connectivity."""
    return "Pong! Server is reachable."

@mcp.tool
def get_env_info() -> dict:
    """Check environment variables."""
    return {
        "google_client_id_set": bool(os.environ.get("GOOGLE_CLIENT_ID")),
        "base_url": os.environ.get("BASE_URL")
    }

if __name__ == "__main__":
    # Default to HTTP host 0.0.0.0 for cloud compatibility
    mcp.run(transport="http", host="0.0.0.0", port=8000)
