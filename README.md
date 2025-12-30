# Gmail MCP Server

A remote MCP (Model Context Protocol) server that provides Gmail functionality through Google OAuth authentication. Users can send emails using their authenticated Gmail account via AI agents.

## Features

- 🔐 **Google OAuth Authentication** - Secure authentication via Google OAuth 2.0
- 📧 **Send Emails** - Send emails through Gmail API on behalf of authenticated users
- 👤 **User Profile** - Retrieve authenticated user's email and profile info
- ☁️ **Cloud Ready** - Designed for deployment on FastMCP Cloud

## Available Tools

| Tool | Description |
|------|-------------|
| `send_email` | Send an email using the authenticated user's Gmail account |
| `get_my_email` | Get the authenticated user's email address and profile info |

## Local Development

### Prerequisites

- Python 3.10+
- Google Cloud Console project with OAuth 2.0 credentials
- Gmail API enabled in your Google Cloud project

### Setup

1. **Clone the repository**
   ```bash
   git clone https://github.com/your-username/gmail-mcp-server.git
   cd gmail-mcp-server
   ```

2. **Install dependencies**
   ```bash
   pip install -r requirements.txt
   ```

3. **Configure environment variables**
   ```bash
   cp .env.example .env
   # Edit .env with your Google OAuth credentials
   ```

4. **Configure Google Cloud Console**
   - Go to [Google Cloud Console](https://console.cloud.google.com/apis/credentials)
   - Create OAuth 2.0 Client ID (Web application)
   - Add authorized redirect URI: `http://localhost:8000/auth/callback`
   - Enable Gmail API in your project

5. **Run the server**
   ```bash
   # Using FastMCP CLI
   fastmcp run server.py:mcp --transport http --port 8000
   
   # Or directly with Python
   python server.py
   ```

### Testing with FastMCP Client

```python
from fastmcp import Client
import asyncio

async def main():
    async with Client("http://localhost:8000/mcp", auth="oauth") as client:
        # First connection opens Google login in browser
        
        # Get user info
        user = await client.call_tool("get_my_email")
        print(f"Logged in as: {user['email']}")
        
        # Send a test email
        result = await client.call_tool("send_email", {
            "to": "recipient@example.com",
            "subject": "Test from Gmail MCP",
            "body": "Hello! This email was sent via Gmail MCP Server."
        })
        print(f"Email sent! Message ID: {result['message_id']}")

asyncio.run(main())
```

## FastMCP Cloud Deployment

### Step 1: Push to GitHub

```bash
git init
git add .
git commit -m "Initial commit - Gmail MCP Server"
git remote add origin https://github.com/your-username/gmail-mcp-server.git
git push -u origin main
```

### Step 2: Deploy on FastMCP Cloud

1. Go to [fastmcp.cloud](https://fastmcp.cloud)
2. Sign in with your GitHub account
3. Create a new project:
   - **Name**: `gmail-mcp-server` (or your preferred name)
   - **Repository**: Select your GitHub repository
   - **Entrypoint**: `server.py:mcp`

### Step 3: Configure Environment Variables

In the FastMCP Cloud dashboard, add these environment variables:

| Variable | Value |
|----------|-------|
| `GOOGLE_CLIENT_ID` | Your Google OAuth Client ID |
| `GOOGLE_CLIENT_SECRET` | Your Google OAuth Client Secret |
| `BASE_URL` | `https://your-project.fastmcp.app` |

### Step 4: Update Google OAuth Redirect URI

Add the production redirect URI in Google Cloud Console:
```
https://your-project.fastmcp.app/auth/callback
```

### Step 5: Connect to Your Server

Your server is now available at:
```
https://your-project.fastmcp.app/mcp
```

## Tool Reference

### send_email

Send an email using the authenticated user's Gmail account.

**Parameters:**
| Parameter | Type | Required | Description |
|-----------|------|----------|-------------|
| `to` | string | Yes | Recipient email address |
| `subject` | string | Yes | Email subject line |
| `body` | string | Yes | Email body content |
| `cc` | string | No | CC recipients (comma-separated) |
| `bcc` | string | No | BCC recipients (comma-separated) |
| `is_html` | boolean | No | Set to true for HTML body (default: false) |

**Returns:**
```json
{
  "status": "sent",
  "message_id": "abc123...",
  "thread_id": "xyz789...",
  "to": "recipient@example.com",
  "subject": "Your subject"
}
```

### get_my_email

Get the authenticated user's email address and profile information.

**Parameters:** None

**Returns:**
```json
{
  "email": "user@gmail.com",
  "name": "John Doe",
  "picture": "https://...",
  "email_verified": true
}
```

## Security Considerations

- OAuth tokens are managed by FastMCP's built-in token handling
- Never commit `.env` file or expose credentials in code
- Use environment variables for all sensitive configuration
- For production, consider using encrypted token storage (Redis with Fernet)

## License

MIT License

## Contributing

Contributions are welcome! Please open an issue or submit a pull request.
