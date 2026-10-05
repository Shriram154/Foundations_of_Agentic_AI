import os
import base64
from email.mime.text import MIMEText
from google.auth.transport.requests import Request
from google.oauth2.credentials import Credentials
from google_auth_oauthlib.flow import InstalledAppFlow
from googleapiclient.discovery import build

SCOPES = [
    'https://www.googleapis.com/auth/gmail.readonly',
    'https://www.googleapis.com/auth/gmail.compose',
    'https://www.googleapis.com/auth/gmail.modify'
]

def get_gmail_service():
    creds = None
    if os.path.exists('token.json'):
        creds = Credentials.from_authorized_user_file('token.json', SCOPES)
        
    if not creds or not creds.valid:
        if creds and creds.expired and creds.refresh_token:
            try:
                creds.refresh(Request())
            except Exception:
                creds = None
                
        if not creds:
            if not os.path.exists('credentials.json'):
                raise FileNotFoundError(
                    "credentials.json file is required for Gmail API OAuth authentication.\n"
                    "Please download credentials.json from Google Cloud Console and place it in d:\\Agentic_AI_PROJECT\\credentials.json"
                )
            flow = InstalledAppFlow.from_client_secrets_file('credentials.json', SCOPES)
            creds = flow.run_local_server(port=0)
            
        with open('token.json', 'w') as token:
            token.write(creds.to_json())

    return build('gmail', 'v1', credentials=creds)


def fetch_unread_gmail_messages(checked_ids: set) -> list:
    """Fetch real unread messages directly via official Gmail API."""
    service = get_gmail_service()
    
    # Query for unread emails
    results = service.users().messages().list(userId='me', q='is:unread').execute()
    messages = results.get('messages', [])
    
    # If no unread, get recent messages from inbox
    if not messages:
        results = service.users().messages().list(userId='me', maxResults=5).execute()
        messages = results.get('messages', [])

    new_emails = []
    for msg_meta in messages:
        msg_id = msg_meta['id']
        if msg_id in checked_ids:
            continue
            
        msg = service.users().messages().get(userId='me', id=msg_id, format='full').execute()
        headers = msg.get('payload', {}).get('headers', [])
        
        subject = "No Subject"
        sender = "Unknown Sender"
        for h in headers:
            if h['name'].lower() == 'subject':
                subject = h['value']
            elif h['name'].lower() == 'from':
                sender = h['value']
                
        snippet = msg.get('snippet', '')
        full_text = f"Subject: {subject} | From: {sender} | Snippet: {snippet}"
        
        new_emails.append({
            'id': msg_id,
            'threadId': msg.get('threadId', msg_id),
            'snippet': full_text,
            'sender': sender,
            'subject': subject
        })
        checked_ids.add(msg_id)
        
    return new_emails


def create_real_gmail_draft(to_email: str, subject: str, body_text: str) -> str:
    """Create a real draft in user's Gmail account via official Gmail API."""
    service = get_gmail_service()
    
    # Ensure multi-paragraph UTF-8 formatting
    message = MIMEText(body_text, 'plain', 'utf-8')
    message['to'] = to_email
    message['from'] = 'me'
    message['subject'] = subject
    
    raw_message = base64.urlsafe_b64encode(message.as_bytes()).decode()
    draft_body = {
        'message': {
            'raw': raw_message
        }
    }
    
    draft = service.users().drafts().create(userId='me', body=draft_body).execute()
    draft_id = draft.get('id', 'unknown')
    print(f"[GMAIL API SUCCESS] Real draft created in your Gmail inbox! Draft ID: {draft_id}")
    return f"Draft created in Gmail Inbox (Draft ID: {draft_id})"
