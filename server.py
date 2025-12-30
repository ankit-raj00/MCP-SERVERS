"""
Gmail MCP Server - Remote MCP server with Google OAuth and Gmail tools.

This server provides Gmail functionality (send email) through the MCP protocol.
Users authenticate via Google OAuth to access their Gmail account.
"""

import os
from dotenv import load_dotenv

# Load environment variables
load_dotenv()

from fastmcp import FastMCP
from fastmcp.server.auth.providers.google import GoogleProvider

# Configure Google OAuth with Gmail scopes
auth = GoogleProvider(
    client_id=os.environ["GOOGLE_CLIENT_ID"],
    client_secret=os.environ["GOOGLE_CLIENT_SECRET"],
    base_url=os.environ.get("BASE_URL", "http://localhost:8000"),
    required_scopes=[
        "openid",
        "https://www.googleapis.com/auth/userinfo.email",
        "https://www.googleapis.com/auth/userinfo.profile",
        "https://www.googleapis.com/auth/gmail.send",  # For sending emails
    ],
)

# Create FastMCP server with Google authentication
mcp = FastMCP(
    name="Gmail MCP Server",
    auth=auth,
    instructions="""
    This MCP server provides Gmail functionality for authenticated users.
    
    Available tools:
    - send_email: Send an email using your authenticated Gmail account
    - get_my_email: Get your authenticated email address and profile info
    
    Users must authenticate with Google OAuth before using these tools.
    """
)

# Import and register Gmail tools
from gmail_tools import register_tools
register_tools(mcp)


if __name__ == "__main__":
    # Run with HTTP transport for remote access
    mcp.run(transport="http", host="0.0.0.0", port=8000)
