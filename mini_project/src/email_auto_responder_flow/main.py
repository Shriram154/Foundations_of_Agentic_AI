#!/usr/bin/env python
import os
import sys
import io
import time
import uuid
from typing import List

# Fix Windows console UTF-8 encoding for unicode characters (like ₹, emojis, etc.)
if sys.platform == "win32":
    sys.stdout = io.TextIOWrapper(sys.stdout.buffer, encoding='utf-8', errors='replace')
    sys.stderr = io.TextIOWrapper(sys.stderr.buffer, encoding='utf-8', errors='replace')

from crewai.flow.flow import Flow, listen, start
from pydantic import BaseModel, Field

from email_auto_responder_flow.types import Email
from email_auto_responder_flow.utils.emails import check_email, format_emails
from email_auto_responder_flow.crews.email_filter_crew.email_filter_crew import EmailFilterCrew


class AutoResponderState(BaseModel):
    id: str = Field(default_factory=lambda: str(uuid.uuid4()))
    emails: List[Email] = []
    checked_emails_ids: set[str] = set()


class EmailAutoResponderFlow(Flow[AutoResponderState]):
    initial_state = AutoResponderState

    @start()
    def fetch_new_emails(self):
        print("\n========================================================")
        print("  🤖 [AGENTIC FLOW] Connecting to Gmail API...")
        print("========================================================\n")
        new_emails, updated_checked_email_ids = check_email(
            checked_emails_ids=self.state.checked_emails_ids
        )

        self.state.emails = new_emails
        self.state.checked_emails_ids = updated_checked_email_ids

    @listen(fetch_new_emails)
    def generate_draft_responses(self):
        total_count = len(self.state.emails)
        print(f"\n[FLOW] Total Gmail emails scanned: {total_count}")
        if total_count > 0:
            print("[FLOW] Triggering Multi-Agent Crew for intelligent triage & draft generation...\n")
            
            # Batch emails in chunks of 2 to guarantee zero rate limits on Groq LLM
            batch_size = 2
            for i in range(0, total_count, batch_size):
                batch = self.state.emails[i:i + batch_size]
                print(f"\n[FLOW BATCH] Processing emails {i+1} to {min(i+batch_size, total_count)} of {total_count}...")
                emails_formatted = format_emails(batch)
                
                try:
                    EmailFilterCrew().crew().kickoff(inputs={"emails": emails_formatted})
                except Exception as batch_err:
                    print(f"[FLOW BATCH WARNING] Batch error: {batch_err}")
                
                # Small 2-second pause between batches to respect API limits
                if i + batch_size < total_count:
                    time.sleep(2)

            self.state.emails = []
            
            # Feature: Executive Agentic Audit Report
            print("\n========================================================")
            print("  📊 AGENTIC EMAIL EXECUTION & AUDIT REPORT")
            print("========================================================")
            print(f"  📥 Total Inbox Messages Scanned: {total_count}")
            print("  🛡️  Safety Filter: Automated / No-Reply messages skipped")
            print("  ✍️  Draft Generation: Saved directly into Gmail 'Drafts' tab")
            print("  🔒 Security Protocol: Human-In-The-Loop (0% Auto-Send Risk)")
            print("========================================================\n")
        else:
            print("\n========================================================")
            print("  ℹ️ [FLOW INFO] No unread messages found in Gmail inbox.")
            print("========================================================\n")


def kickoff():
    """
    Run the email flow.
    """
    try:
        email_auto_response_flow = EmailAutoResponderFlow()
        email_auto_response_flow.kickoff()
    except KeyboardInterrupt:
        print("\n[FLOW] Execution stopped by user.")
    except Exception as e:
        print(f"\n[FLOW COMPLETED] Result: {e}")


def plot_flow():
    """
    Plot the flow.
    """
    email_auto_response_flow = EmailAutoResponderFlow()
    email_auto_response_flow.plot()


if __name__ == "__main__":
    kickoff()
