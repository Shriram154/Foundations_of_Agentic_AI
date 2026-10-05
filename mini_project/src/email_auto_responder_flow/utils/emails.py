import os
from typing import List
from email_auto_responder_flow.types import Email
from email_auto_responder_flow.utils.gmail_api import fetch_unread_gmail_messages

def check_email(checked_emails_ids: set[str]) -> tuple[list[Email], set[str]]:
    print("[EMAIL TOOL] Checking real Gmail inbox for unread messages...")
    
    try:
        real_messages = fetch_unread_gmail_messages(checked_emails_ids)
        new_emails: List[Email] = []
        for msg in real_messages:
            new_emails.append(
                Email(
                    id=str(msg['id']),
                    threadId=str(msg['threadId']),
                    snippet=str(msg['snippet']),
                    sender=str(msg['sender']),
                )
            )
        print(f"[EMAIL TOOL] Found {len(new_emails)} new real emails in your Gmail inbox!")
        return new_emails, checked_emails_ids
    except FileNotFoundError as fnf:
        print(f"\n[GMAIL SETUP REQUIRED] {fnf}\n")
        return [], checked_emails_ids
    except Exception as e:
        print(f"[EMAIL TOOL WARNING] Gmail API fetch error: {e}")
        return [], checked_emails_ids


def format_emails(emails: List[Email]) -> str:
    emails_string = []
    for email in emails:
        arr = [
            f"ID: {email.id}",
            f"- Thread ID: {email.threadId}",
            f"- Snippet: {email.snippet}",
            f"- From: {email.sender}",
            "--------",
        ]
        emails_string.append("\n".join(arr))
    return "\n".join(emails_string)
