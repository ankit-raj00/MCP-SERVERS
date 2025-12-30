"""
Gmail Tools - MCP tools for Gmail operations.

This module provides tools for interacting with Gmail API,
including sending emails using the authenticated user's account.
"""

import base64
from email.mime.text import MIMEText
from email.mime.multipart import MIMEMultipart

from fastmcp.server.dependencies import get_access_token
from googleapiclient.discovery import build
from google.oauth2.credentials import Credentials


def register_tools(mcp):
    """Register Gmail tools with the MCP server."""
    
    @mcp.tool
    async def send_email(
        to: str,
        subject: str,
        body: str,
        cc: str = None,
        bcc: str = None,
        is_html: bool = False
    ) -> dict:
        """
        Send an email using the authenticated user's Gmail account.
        
        Args:
            to: Recipient email address (required)
            subject: Email subject line (required)
            body: Email body content (required)
            cc: Optional CC recipients (comma-separated email addresses)
            bcc: Optional BCC recipients (comma-separated email addresses)
            is_html: Set to True if body contains HTML content (default: False)
        
        Returns:
            dict containing:
                - status: "sent" on success
                - message_id: Gmail message ID
                - to: Recipient address
                - subject: Email subject
        
        Example:
            send_email(
                to="recipient@example.com",
                subject="Hello from MCP",
                body="This is a test email sent via Gmail MCP Server!"
            )
        """
        # Get the access token from the authenticated session
        token = get_access_token()
        
        # Create credentials from the OAuth token
        credentials = Credentials(token=token.token)
        
        # Build Gmail service
        service = build('gmail', 'v1', credentials=credentials)
        
        # Create email message
        if is_html:
            message = MIMEMultipart('alternative')
            message.attach(MIMEText(body, 'html'))
        else:
            message = MIMEText(body, 'plain')
        
        message['to'] = to
        message['subject'] = subject
        
        if cc:
            message['cc'] = cc
        if bcc:
            message['bcc'] = bcc
        
        # Encode message to base64 URL-safe format
        raw = base64.urlsafe_b64encode(message.as_bytes()).decode('utf-8')
        
        # Send the email
        result = service.users().messages().send(
            userId='me',
            body={'raw': raw}
        ).execute()
        
        return {
            "status": "sent",
            "message_id": result.get('id'),
            "thread_id": result.get('threadId'),
            "to": to,
            "subject": subject
        }
    
    @mcp.tool
    async def get_my_email() -> dict:
        """
        Get the authenticated user's email address and profile information.
        
        Returns:
            dict containing:
                - email: User's email address
                - name: User's display name
                - picture: URL to user's profile picture
        
        Example:
            get_my_email() -> {"email": "user@gmail.com", "name": "John Doe", ...}
        """
        token = get_access_token()
        
        return {
            "email": token.claims.get("email"),
            "name": token.claims.get("name"),
            "picture": token.claims.get("picture"),
            "email_verified": token.claims.get("email_verified")
        }
