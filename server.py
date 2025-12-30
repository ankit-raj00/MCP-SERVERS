"""
Gmail MCP Server - Remote MCP server (Minimal Test).
"""
from fastmcp import FastMCP

mcp = FastMCP("Gmail MCP Server (Test)")

@mcp.tool
def ping() -> str:
    """Basic connectivity test."""
    return "Pong! Server is live and reachable."

if __name__ == "__main__":
    # ✅ REQUIRED for cloud deployment
    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=8000,
        path="/mcp"   # important
    )
