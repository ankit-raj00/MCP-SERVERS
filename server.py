"""
Minimal MCP server — FastMCP hosted safe
"""
import os
from fastmcp import FastMCP

mcp = FastMCP("Gmail MCP Server")

@mcp.tool
def ping() -> str:
    return "Pong!"

if __name__ == "__main__":
    PORT = int(os.environ.get("PORT", 8000))
    print(f"🚀 MCP starting on port {PORT}")

    mcp.run(
        transport="sse",
        host="0.0.0.0",
        port=PORT,
        path="/mcp"
    )
