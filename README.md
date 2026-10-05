# Agentic AI Gmail Auto-Responder & Draft Generator

## Problem Statement

Email has become an essential communication channel in academic and professional environments, but managing a large volume of incoming messages can be repetitive and time-consuming. Important emails may require careful analysis to identify questions, deadlines, requests, or actions, while many other messages are automated notifications, announcements, or no-reply communications that do not require a response.

Conventional email automation systems generally rely on fixed rules or simple prompt-based response generation. Such systems may fail to understand the context of an email, distinguish actionable messages from automated notifications, or generate responses without verifying information that may have changed over time. Fully automated email sending also introduces a significant risk of sending incorrect, incomplete, or inappropriate responses.

## Proposed Solution

The **Agentic AI Gmail Auto-Responder & Draft Generator** is a multi-agent AI system designed to intelligently process incoming Gmail messages and assist users in preparing appropriate responses.

The system uses a sequence of specialized AI agents to:

- Identify emails that require a response.
- Filter automated and no-reply messages.
- Analyze the intent, questions, deadlines, and required actions within actionable emails.
- Retrieve additional information through web search when external context is required.
- Generate professional and context-aware email responses.
- Save the generated responses directly to the Gmail Drafts folder for user review.

Instead of automatically sending AI-generated emails, the system follows a **Drafts-Only, Human-in-the-Loop approach**. The final decision to modify or send a response remains with the user, providing a safer and more controlled form of email automation.

## How It Works

The system follows a sequential multi-agent workflow:

**Gmail Inbox → Email Filtering → Action Analysis → Web Search (if required) → Response Generation → Gmail Draft**

Three specialized agents are responsible for different stages of the process:

1. **Email Filter Agent**  
   Determines whether an incoming email is actionable or should be ignored, including automated and no-reply messages.

2. **Action Analyzer Agent**  
   Examines actionable emails, identifies questions, requests, deadlines, and missing information, and performs web searches when additional context is required.

3. **Response Writer Agent**  
   Uses the email context and retrieved information to generate a professional response and save it as a Gmail draft.

## Key Objective

The primary objective of this project is to demonstrate how **Agentic AI can be used to build a controlled, tool-using, multi-agent workflow for real-world email automation**, while maintaining user oversight and reducing the risks associated with fully autonomous communication.

## Technology

- Python
- CrewAI Flow
- Groq Cloud
- Gmail REST API
- Google OAuth 2.0
- Pydantic
- SerperDev Web Search API

## Safety

The system is intentionally designed so that AI-generated responses are **never automatically sent**. Responses are created as Gmail drafts, allowing the user to review, edit, and manually send them.

This provides a practical balance between **AI-driven automation and human control**.
