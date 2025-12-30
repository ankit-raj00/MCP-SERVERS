"""
Gmail MCP Server - Remote MCP server with Google OAuth and Gmail tools.

This server provides Gmail functionality (send email) through the MCP protocol.
Users authenticate via Google OAuth to access their Gmail account.
"""

import os
from dotenv import load_dotenv
from fastmcp import FastMCP

# Load environment variables
load_dotenv()

# Check for required credentials
client_id = os.environ.get("GOOGLE_CLIENT_ID")
client_secret = os.environ.get("GOOGLE_CLIENT_SECRET")
base_url = os.environ.get("BASE_URL", "http://localhost:8000")

if client_id and client_secret:
    # -------------------------------------------------------------------------
    # AUTHENTICATION ENABLED
    # -------------------------------------------------------------------------
    try:
        from fastmcp.server.auth.providers.google import GoogleProvider
        
        print(f"Starting with Google OAuth. Base URL: {base_url}")
        
        auth = GoogleProvider(
            client_id=client_id,
            client_secret=client_secret,
            base_url=base_url,
            required_scopes=[
                "openid",
                "https://www.googleapis.com/auth/userinfo.email",
                "https://www.googleapis.com/auth/userinfo.profile",
                "https://www.googleapis.com/auth/gmail.send",
            ],
        )
        
        mcp = FastMCP(
            name="Gmail MCP Server",
            auth=auth,
            instructions="Authenticate with Google to use Gmail tools."
        )
        
    except Exception as e:
        print(f"Error initializing auth: {e}")
        # Fallback to no-auth for diagnostics
        mcp = FastMCP("Gmail Server (Auth Failed)")
else:
    # -------------------------------------------------------------------------
    # AUTHENTICATION DISABLED (Diagnostics Mode)
    # -------------------------------------------------------------------------
    print("WARNING: GOOGLE_CLIENT_ID or GOOGLE_CLIENT_SECRET not set.")
    print("Starting in diagnostic mode without authentication.")
    mcp = FastMCP("Gmail Server (No Auth)")

# Import and register Gmail tools
from gmail_tools import register_tools
register_tools(mcp)


@mcp.tool
def debug_status() -> dict:
    """Check server status and environment configuration."""
    return {
        "status": "messaging_online",
        "auth_enabled": bool(client_id and client_secret),
        "base_url": base_url,
        "env_check": {
            "has_client_id": bool(client_id),
            "has_client_secret": bool(client_secret)
        }
    }

if __name__ == "__main__":
    # Run with HTTP transport for remote access
    mcp.run(transport="http", host="0.0.0.0", port=8000)
