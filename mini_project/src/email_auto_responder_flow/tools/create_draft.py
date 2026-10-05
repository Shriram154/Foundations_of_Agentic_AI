import os
import re
from crewai.tools import tool
from email_auto_responder_flow.utils.gmail_api import create_real_gmail_draft

NO_REPLY_PATTERNS = ["noreply", "no-reply", "donotreply", "do-not-reply", "mailer-daemon", "notifications@", "alerts@"]

def extract_email(sender: str) -> str:
    match = re.search(r'[\w\.-]+@[\w\.-]+', str(sender))
    if match:
        return match.group(0).strip()
    return str(sender).strip()

@tool("Create Draft")
def create_draft(to_email: str, subject: str, message: str) -> str:
    """
    Create a real email draft in your Gmail inbox.
    
    Args:
        to_email: The recipient email address to reply to.
        subject: The subject line for the reply email.
        message: The complete body text for the reply draft.
    """
    try:
        clean_recipient = extract_email(to_email).lower()
        
        # Guardrail Check: Skip draft creation for no-reply / automated email senders
        if any(pattern in clean_recipient for pattern in NO_REPLY_PATTERNS):
            print(f"\n[SAFETY SKIP] Recipient '{clean_recipient}' is an automated/no-reply address. Draft skipped.\n")
            return f"\n[SKIPPED] Draft creation skipped because sender '{clean_recipient}' is automated/no-reply.\n"
            
        if not clean_recipient or "@" not in clean_recipient:
            clean_recipient = "student@rajalakshmi.edu.in"
            
        clean_subject = str(subject).strip()
        if not clean_subject.lower().startswith("re:"):
            clean_subject = f"Re: {clean_subject}"
            
        clean_message = str(message).strip()
        
        result_msg = create_real_gmail_draft(clean_recipient, clean_subject, clean_message)
        print(f"\n[TOOL EXECUTED] Created real draft for {clean_recipient} | Subject: {clean_subject}\n")
        return f"\n[SUCCESS] {result_msg}\n"
    except Exception as e:
        print(f"\n[TOOL ERROR] {e}\n")
        return f"\nDraft creation failed: {e}\n"
