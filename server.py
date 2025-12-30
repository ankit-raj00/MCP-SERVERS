"""
Gmail MCP Server - Connectivity Test.
"""
from fastmcp import FastMCP

# Create a basic server - NO Auth, just to test connection
mcp = FastMCP("Google MCP Test")

@mcp.tool
def ping() -> str:
    return "Pong from FastMCP Cloud!"

if __name__ == "__main__":
    # Ensure we bind to 0.0.0.0 for Cloud containers
    # The timeout often happens if it defaults to 127.0.0.1
    mcp.run(transport="http", host="0.0.0.0", port=8000)
