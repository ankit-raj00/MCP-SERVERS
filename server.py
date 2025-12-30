"""
Gmail MCP Server - Remote MCP server (Minimal Test).
"""
from fastmcp import FastMCP

# Create a minimal server for connectivity testing
mcp = FastMCP("Gmail MCP Server (Test)")

@mcp.tool
def ping() -> str:
    """Basic connectivity test."""
    return "Pong! Server is live and reachable."

if __name__ == "__main__":
    # Ensure transport is HTTP for Cloud deployment
    mcp.run(transport="http", host="0.0.0.0", port=8000)
