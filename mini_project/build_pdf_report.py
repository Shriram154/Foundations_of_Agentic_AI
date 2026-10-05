import os
import sys
from reportlab.lib.pagesizes import letter
from reportlab.lib import colors
from reportlab.lib.styles import getSampleStyleSheet, ParagraphStyle
from reportlab.lib.units import inch
from reportlab.platypus import (
    SimpleDocTemplate, Paragraph, Spacer, Table, TableStyle, PageBreak, KeepTogether, HRFlowable
)
from reportlab.pdfgen import canvas

class NumberedCanvas(canvas.Canvas):
    """
    Two-pass canvas to calculate total page count and add running headers/footers.
    """
    def __init__(self, *args, **kwargs):
        super().__init__(*args, **kwargs)
        self._saved_page_states = []

    def showPage(self):
        self._saved_page_states.append(dict(self.__dict__))
        self._startPage()

    def save(self):
        num_pages = len(self._saved_page_states)
        for state in self._saved_page_states:
            self.__dict__.update(state)
            self.draw_page_number(num_pages)
            super().showPage()
        super().save()

    def draw_page_number(self, page_count):
        if self._pageNumber == 1:
            # Suppress running header/footer on title page
            return
        
        self.saveState()
        self.setFont("Helvetica", 9)
        self.setFillColor(colors.HexColor("#4B5563"))
        
        # Header
        self.drawString(54, 11 * inch - 36, "Agentic AI Gmail Auto-Responder — Project Review Report")
        self.setStrokeColor(colors.HexColor("#E5E7EB"))
        self.setLineWidth(0.75)
        self.line(54, 11 * inch - 42, 8.5 * inch - 54, 11 * inch - 42)
        
        # Footer
        page_text = f"Page {self._pageNumber} of {page_count}"
        self.drawRightString(8.5 * inch - 54, 36, page_text)
        self.drawString(54, 36, "Department of AI & DS — Rajalakshmi Engineering College")
        self.line(54, 48, 8.5 * inch - 54, 48)
        
        self.restoreState()

def create_report(pdf_filename="Agentic_AI_Gmail_AutoResponder_Report.pdf"):
    doc = SimpleDocTemplate(
        pdf_filename,
        pagesize=letter,
        leftMargin=54,
        rightMargin=54,
        topMargin=54,
        bottomMargin=54
    )
    
    styles = getSampleStyleSheet()
    
    # Custom Palette
    PRIMARY = colors.HexColor("#1E3A8A")    # Deep Navy
    SECONDARY = colors.HexColor("#2563EB")  # Accent Blue
    DARK_TEXT = colors.HexColor("#1F2937")  # Charcoal Text
    LIGHT_BG = colors.HexColor("#F8FAFC")   # Slate Tint
    BORDER_COLOR = colors.HexColor("#CBD5E1")
    
    # Modify default styles
    styles['Normal'].textColor = DARK_TEXT
    styles['Normal'].fontSize = 10
    styles['Normal'].leading = 14
    styles['Normal'].fontName = 'Helvetica'
    
    body_style = styles['Normal']
    
    title_style = ParagraphStyle(
        'CoverTitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=20,
        leading=26,
        alignment=1, # Center
        textColor=PRIMARY
    )
    
    subtitle_style = ParagraphStyle(
        'CoverSubtitle',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        alignment=1,
        textColor=SECONDARY
    )
    
    h1_style = ParagraphStyle(
        'Heading1_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=15,
        leading=19,
        textColor=PRIMARY,
        spaceBefore=14,
        spaceAfter=8,
        keepWithNext=True
    )
    
    h2_style = ParagraphStyle(
        'Heading2_Custom',
        parent=styles['Normal'],
        fontName='Helvetica-Bold',
        fontSize=12,
        leading=16,
        textColor=SECONDARY,
        spaceBefore=10,
        spaceAfter=6,
        keepWithNext=True
    )
    
    bullet_style = ParagraphStyle(
        'BulletCustom',
        parent=styles['Normal'],
        leftIndent=15,
        firstLineIndent=-10,
        spaceAfter=4
    )
    
    code_style = ParagraphStyle(
        'CodeStyle',
        parent=styles['Normal'],
        fontName='Courier',
        fontSize=8.5,
        leading=11,
        textColor=colors.HexColor("#0F172A"),
        backColor=colors.HexColor("#F1F5F9"),
        borderColor=BORDER_COLOR,
        borderWidth=0.5,
        borderPadding=6,
        spaceBefore=6,
        spaceAfter=6
    )

    story = []

    # ==========================================
    # 1. TITLE PAGE
    # ==========================================
    story.append(Spacer(1, 0.4 * inch))
    story.append(Paragraph("<b>Agentic AI Gmail Auto-Responder & Draft Generator</b>", title_style))
    story.append(Spacer(1, 10))
    story.append(Paragraph("Autonomous Multi-Agent Email Triage, Web Verification & Safe Draft Generation Platform", subtitle_style))
    story.append(Spacer(1, 15))
    story.append(HRFlowable(width="100%", thickness=1.5, color=PRIMARY, spaceBefore=5, spaceAfter=20))
    
    story.append(Paragraph("<b>AD23731 Foundations of Agentic AI — Mini-Project Report</b>", ParagraphStyle('SubHeader', parent=styles['Normal'], alignment=1, fontName='Helvetica-Bold', fontSize=12, textColor=DARK_TEXT)))
    story.append(Spacer(1, 25))
    
    story.append(Paragraph("<b>Submitted by</b>", ParagraphStyle('SubmittedBy', parent=styles['Normal'], alignment=1, fontName='Helvetica', fontSize=11)))
    story.append(Spacer(1, 15))
    
    team_data = [
        [Paragraph("<b>SHRIRAM N</b>", body_style), Paragraph("<b>231501154</b>", body_style)],
        [Paragraph("<b>SANJAY KISHORE S.A</b>", body_style), Paragraph("<b>231501145</b>", body_style)],
        [Paragraph("<b>THILLAI NATHAN B</b>", body_style), Paragraph("<b>231501173</b>", body_style)]
    ]
    t_team = Table(team_data, colWidths=[2.5*inch, 1.8*inch], hAlign='CENTER')
    t_team.setStyle(TableStyle([
        ('ALIGN', (0,0), (-1,-1), 'CENTER'),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, colors.HexColor("#E2E8F0")),
        ('BACKGROUND', (0,0), (-1,-1), LIGHT_BG)
    ]))
    story.append(t_team)
    story.append(Spacer(1, 30))
    
    story.append(Paragraph("<b>Department of Artificial Intelligence and Data Science</b>", ParagraphStyle('Dept', parent=styles['Normal'], alignment=1, fontName='Helvetica-Bold', fontSize=12, textColor=PRIMARY)))
    story.append(Spacer(1, 10))
    story.append(Paragraph("<b>RAJALAKSHMI ENGINEERING COLLEGE</b>", ParagraphStyle('College', parent=styles['Normal'], alignment=1, fontName='Helvetica-Bold', fontSize=13, textColor=DARK_TEXT)))
    story.append(Paragraph("(An Autonomous Institution, Affiliated to Anna University, Chennai)", ParagraphStyle('Affil', parent=styles['Normal'], alignment=1, fontName='Helvetica-Oblique', fontSize=9.5, textColor=colors.HexColor("#4B5563"))))
    story.append(Spacer(1, 40))
    story.append(Paragraph("<b>SEPTEMBER 2026</b>", ParagraphStyle('DateStr', parent=styles['Normal'], alignment=1, fontName='Helvetica-Bold', fontSize=11, textColor=DARK_TEXT)))
    
    story.append(PageBreak())

    # ==========================================
    # 2. BONAFIDE CERTIFICATE
    # ==========================================
    story.append(Paragraph("<b>RAJALAKSHMI ENGINEERING COLLEGE</b>", ParagraphStyle('RecCert', parent=styles['Normal'], alignment=1, fontName='Helvetica-Bold', fontSize=14, textColor=PRIMARY)))
    story.append(Paragraph("Approved by AICTE | Affiliated to Anna University | Accredited by NAAC", ParagraphStyle('RecSub', parent=styles['Normal'], alignment=1, fontName='Helvetica', fontSize=9, textColor=colors.HexColor("#64748B"))))
    story.append(Spacer(1, 20))
    story.append(HRFlowable(width="100%", thickness=1, color=SECONDARY, spaceBefore=0, spaceAfter=20))
    
    story.append(Paragraph("<b>BONAFIDE CERTIFICATE</b>", ParagraphStyle('BonaTitle', parent=styles['Normal'], alignment=1, fontName='Helvetica-Bold', fontSize=14, textColor=DARK_TEXT)))
    story.append(Spacer(1, 25))
    
    cert_text = (
        "Certified that this mini-project report <b>“Agentic AI Gmail Auto-Responder & Draft Generator”</b> "
        "is the bonafide work of <b>“SHRIRAM N (Reg. No. 231501154), SANJAY KISHORE S.A (Reg. No. 231501145), "
        "THILLAI NATHAN B (Reg. No. 231501173)”</b>, V Semester, B.Tech. Artificial Intelligence and Data Science "
        "Department in partial fulfilment of the requirements for the course <b>AD23731 – Foundations of Agentic AI</b> "
        "during the Academic Year 2026 – 2027."
    )
    story.append(Paragraph(cert_text, ParagraphStyle('CertBody', parent=body_style, fontSize=10.5, leading=16, alignment=4)))
    story.append(Spacer(1, 50))
    
    fac_table = [
        [Paragraph("<b>Faculty in-charge</b>", body_style), Paragraph("<b>Head of Department</b>", body_style)]
    ]
    t_fac = Table(fac_table, colWidths=[3.2*inch, 3.2*inch], hAlign='CENTER')
    t_fac.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    story.append(t_fac)
    story.append(Spacer(1, 60))
    
    story.append(Paragraph("Submitted to mini-project viva voce examination held on: ....................................", body_style))
    story.append(Spacer(1, 40))
    
    exam_table = [
        [Paragraph("<b>INTERNAL EXAMINER</b>", body_style), Paragraph("<b>EXTERNAL EXAMINER</b>", body_style)]
    ]
    t_exam = Table(exam_table, colWidths=[3.2*inch, 3.2*inch], hAlign='CENTER')
    t_exam.setStyle(TableStyle([('ALIGN', (0,0), (-1,-1), 'CENTER')]))
    story.append(t_exam)
    
    story.append(PageBreak())

    # ==========================================
    # 3. TABLE OF CONTENTS
    # ==========================================
    story.append(Paragraph("Table of Contents", h1_style))
    story.append(HRFlowable(width="100%", thickness=1, color=PRIMARY, spaceBefore=2, spaceAfter=12))
    
    toc_data = [
        ["1.", "Executive Summary", "Page 4"],
        ["2.", "Functional Prototype — Overview & Screens", "Page 5"],
        ["3.", "Agent Orchestration Workflow Implementation", "Page 7"],
        ["4.", "Tool Integrations", "Page 9"],
        ["5.", "Agentic RAG & Web Search Integration", "Page 10"],
        ["6.", "Memory & State Management", "Page 11"],
        ["7.", "Reasoning, Planning, Reflection & Self-Correction", "Page 12"],
        ["8.", "Preliminary Evaluation Results", "Page 13"],
        ["9.", "Comparison with Baseline Solution", "Page 15"],
        ["10.", "Current Limitations & Risks", "Page 16"],
        ["11.", "Remaining Work & Plan to Final Review", "Page 17"],
        ["12.", "Conclusion", "Page 18"],
        ["13.", "References & Appendix", "Page 19"]
    ]
    t_toc = Table(toc_data, colWidths=[0.4*inch, 5.2*inch, 1.2*inch])
    t_toc.setStyle(TableStyle([
        ('FONTNAME', (0,0), (-1,-1), 'Helvetica'),
        ('FONTSIZE', (0,0), (-1,-1), 10),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('ALIGN', (2,0), (2,-1), 'RIGHT'),
        ('LINEBELOW', (0,0), (-1,-1), 0.5, colors.HexColor("#F1F5F9"))
    ]))
    story.append(t_toc)
    story.append(PageBreak())

    # ==========================================
    # SECTION 1: EXECUTIVE SUMMARY
    # ==========================================
    story.append(Paragraph("1. Executive Summary", h1_style))
    story.append(Paragraph(
        "This report documents progress on <b>Agentic AI Gmail Auto-Responder & Draft Generator</b>, an autonomous multi-agent "
        "email intelligence system developed for course <b>AD23731 Foundations of Agentic AI</b>. The system performs automated triage, "
        "context analysis, web fact verification, and response drafting for incoming Gmail messages. It enforces a strict "
        "<b>Drafts-Only Safety Protocol</b>: all generated email replies are saved directly into the user's official Gmail inbox "
        "<code>Drafts</code> tab (<code>in:draft</code>) without ever auto-sending messages.", body_style))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("1.1 Scope of This Review", h2_style))
    story.append(Paragraph(
        "This review covers five key engineering deliverables: a working functional CLI prototype, multi-agent orchestration "
        "implementation using CrewAI Flow, official Google Gmail OAuth 2.0 API tools, Groq open-source LLM integration, and real-world "
        "evaluation against live student emails (e.g., Tata Imagination Challenge 2026 & Razorpay Buildathon).", body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("1.2 What Changed Since Review 1", h2_style))
    story.append(Paragraph(
        "Since initial architectural proposals, the project progressed from conceptual designs to a verified running codebase. "
        "The system now operates a 3-agent sequential CrewAI flow backed by Groq Cloud's <code>openai/gpt-oss-20b</code> LLM engine. "
        "Automated guardrails were added to detect and skip no-reply senders (e.g. <code>noreply@</code>, <code>donotreply@</code>) and non-actionable "
        "broadcasts, preventing unwanted draft creation.", body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("1.3 Key Verified Facts at a Glance", h2_style))
    story.append(Paragraph("• <b>3 Specialized Agents Operational:</b> Email Filter Agent, Action Analyzer Agent, and Response Writer Agent execute sequentially with shared state.", bullet_style))
    story.append(Paragraph("• <b>Zero-Cost Open-Source Engine:</b> Powered by Groq Cloud LLM API with native tool calling support at ₹0 commercial cost.", bullet_style))
    story.append(Paragraph("• <b>Official Google OAuth 2.0 Integration:</b> Authenticates via <code>credentials.json</code> and saves session tokens in <code>token.json</code>.", bullet_style))
    story.append(Paragraph("• <b>100% Drafts-Only Safety:</b> Directly invokes <code>service.users().drafts().create()</code> with zero automated message dispatch.", bullet_style))
    story.append(Paragraph("• <b>Automated Guardrails:</b> Automatically filters out <code>noreply@</code> broadcasts and informational circulars.", bullet_style))

    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 2: FUNCTIONAL PROTOTYPE
    # ==========================================
    story.append(Paragraph("2. Functional Prototype — Overview & Execution", h1_style))
    story.append(Paragraph(
        "The functional prototype consists of a Python 3.10 CLI application managed inside an isolated virtual environment (<code>.venv</code>). "
        "The system connects to Google Gmail REST endpoints using <code>google-api-python-client</code> and <code>google-auth-oauthlib</code>. "
        "It features state management powered by Pydantic and CrewAI Flow, executing real-time web verification prior to draft publishing.", body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("2.1 Backend Architecture & Tool Surface", h2_style))
    
    api_table_data = [
        ["Module / Tool", "Technology / Function", "Target Operation"],
        ["gmail_api.py", "Google OAuth 2.0 Client", "Authenticates user and fetches unread inbox messages"],
        ["create_draft.py", "Custom Gmail Tool", "Encodes MIMEText & creates draft in user Gmail inbox"],
        ["web_search_tool", "SerperDev / Tavily REST API", "Fetches 250-char SERP snippets for fact-checking"],
        ["email_filter_crew.py", "CrewAI v1.15.17 Engine", "Orchestrates 3 sequential agents with retry logic"],
        ["main.py", "CrewAI Flow Entry Point", "Handles event loop, UTF-8 console output & audit logging"]
    ]
    t_api = Table(api_table_data, colWidths=[1.8*inch, 2.2*inch, 2.8*inch])
    t_api.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 5),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('BACKGROUND', (0,1), (-1,-1), LIGHT_BG)
    ]))
    story.append(t_api)
    story.append(Spacer(1, 10))

    story.append(Paragraph("2.2 Live Execution Output Trace", h2_style))
    story.append(Paragraph("Below is an exact trace captured from a live execution run scanning real student inbox messages:", body_style))
    
    trace_log = (
        "========================================================\n"
        "  🤖 [AGENTIC FLOW] Connecting to Gmail API...\n"
        "========================================================\n\n"
        "[EMAIL TOOL] Checking real Gmail inbox for unread messages...\n"
        "[EMAIL TOOL] Found 2 new real emails in your Gmail inbox!\n"
        "[FLOW] Triggering Multi-Agent Crew for intelligent triage & draft generation...\n\n"
        "✔ Task 1: Filter Specialist Agent analyzed incoming email queue.\n"
        "✔ Task 2: Action Analyzer Agent outlined required response actions.\n"
        "✔ Task 3: Response Writer Agent created polished drafts.\n\n"
        "[GMAIL API SUCCESS] Real draft created! Draft ID: r6049982223570239263\n"
        "[TOOL EXECUTED] Recipient: placementexecutive2@rajalakshmi.edu.in\n"
        "Subject: Re: Tata Imagination Challenge 2026 — Confirmation & Queries\n\n"
        "========================================================\n"
        "  📊 AGENTIC EMAIL EXECUTION & AUDIT REPORT\n"
        "========================================================\n"
        "  📥 Total Inbox Messages Scanned: 2\n"
        "  🛡️  Safety Filter: Automated / No-Reply messages skipped\n"
        "  ✍️  Draft Generation: Saved directly into Gmail 'Drafts' tab\n"
        "  🔒 Security Protocol: Human-In-The-Loop (0% Auto-Send Risk)\n"
        "========================================================"
    )
    story.append(Paragraph(trace_log.replace("\n", "<br/>").replace(" ", "&nbsp;"), code_style))

    story.append(PageBreak())

    # ==========================================
    # SECTION 3: AGENT ORCHESTRATION
    # ==========================================
    story.append(Paragraph("3. Agent Orchestration Workflow Implementation", h1_style))
    story.append(Paragraph(
        "The core intelligence layer utilizes CrewAI's <code>Flow</code> architecture. State is passed cleanly between flow listeners "
        "and tasks using a shared Pydantic state container (<code>AutoResponderState</code>).", body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("3.1 Sequential 3-Agent Pipeline", h2_style))
    story.append(Paragraph("1. <b>Email Filter Agent (<code>email_filter_agent</code>):</b> Scans unread email metadata and tags emails as <code>ACTIONABLE</code> or <code>DO_NOT_REPLY</code>.", bullet_style))
    story.append(Paragraph("2. <b>Action Analyzer Agent (<code>email_action_agent</code>):</b> Parses actionable emails, extracts key questions, and queries live SERP search APIs for missing facts.", bullet_style))
    story.append(Paragraph("3. <b>Response Writer Agent (<code>email_response_writer</code>):</b> Drafts formal, polite responses and calls <code>create_draft</code> strictly for actionable messages.", bullet_style))

    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 4: TOOL INTEGRATIONS
    # ==========================================
    story.append(Paragraph("4. Tool Integrations", h1_style))
    story.append(Paragraph(
        "Agents interface with two primary tools: the custom Gmail integration tool (<code>create_draft</code>) and the live web search "
        "tool (<code>web_search_tool</code>). Both tools are written in Python and decorated with CrewAI's <code>@tool</code> decorator.", body_style))
    story.append(Spacer(1, 8))

    story.append(Paragraph("4.1 Tool Specifications & Safety Guardrails", h2_style))
    
    tool_table_data = [
        ["Tool Name", "Input Schema", "Functionality & Guardrail"],
        ["create_draft", "to_email: str, subject: str, message: str", "Extracts clean email, checks no-reply blocklist, builds MIMEText, and calls Gmail API drafts.create()."],
        ["web_search_tool", "query: str", "Queries SerperDev Google SERP API, returning trimmed 250-character snippets to prevent LLM token rate limits."]
    ]
    t_tool = Table(tool_table_data, colWidths=[1.5*inch, 2.2*inch, 3.1*inch])
    t_tool.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('BACKGROUND', (0,1), (-1,-1), LIGHT_BG)
    ]))
    story.append(t_tool)

    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 5: AGENTIC RAG & SEARCH INTEGRATION
    # ==========================================
    story.append(Paragraph("5. Agentic RAG & Web Search Integration", h1_style))
    story.append(Paragraph(
        "When an incoming email references external events (e.g. <i>Tata Imagination Challenge 2026</i> or <i>Razorpay Buildathon</i>), "
        "the Action Analyzer Agent formulates search queries. The custom <code>web_search_tool</code> queries SerperDev REST endpoints "
        "and injects real-time context into the agent's memory before drafting.", body_style))
    story.append(Spacer(1, 8))
    
    story.append(Paragraph("5.1 Search Payload Truncation Engineering", h2_style))
    story.append(Paragraph(
        "Groq Cloud's free tier enforces a strict 8,000 Tokens Per Minute (TPM) limit on <code>openai/gpt-oss-20b</code>. "
        "Unfiltered web search results often contain over 3,000 tokens of raw HTML/JSON. We engineered payload truncation inside "
        "<code>web_search_tool</code> to slice search results to 250 characters. This deliberate engineering choice prevents HTTP 429 rate-limit errors while preserving factual accuracy.", body_style))

    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 6: MEMORY & STATE MANAGEMENT
    # ==========================================
    story.append(Paragraph("6. Memory & State Management", h1_style))
    story.append(Paragraph(
        "State management operates across two tiers: short-term working memory within the flow, and long-term token persistence.", body_style))
    story.append(Spacer(1, 8))
    story.append(Paragraph("• <b>Short-Term Flow Memory:</b> Managed by <code>AutoResponderState</code> Pydantic model holding list of unread <code>Email</code> objects and processed message IDs.", bullet_style))
    story.append(Paragraph("• <b>OAuth Token Persistence:</b> OAuth 2.0 user credentials are authenticated once and persisted to <code>token.json</code>. Subsequent flow runs reuse valid refresh tokens automatically without re-prompting browser sign-in.", bullet_style))
    story.append(Paragraph("• <b>Windows Encoding Resilience:</b> Replaced standard Windows console output streams with a UTF-8 wrapper (<code>sys.stdout = TextIOWrapper(sys.stdout.buffer, encoding='utf-8')</code>) to safely render special characters (e.g. ₹, emojis) without <code>charmap</code> codec crashes.", bullet_style))

    story.append(PageBreak())

    # ==========================================
    # SECTION 7: REASONING & SELF-CORRECTION
    # ==========================================
    story.append(Paragraph("7. Reasoning, Planning & Safety Filtering", h1_style))
    story.append(Paragraph(
        "The Email Filter Agent performs explicit categorization reasoning before marking an email for action. "
        "If an email sender matches blocklist patterns (<code>noreply@</code>, <code>no-reply@</code>, <code>donotreply@</code>) or lacks actionable queries, "
        "the email is flagged as <code>DO_NOT_REPLY</code>. The Writer Agent evaluates this tag and skips tool invocation entirely.", body_style))

    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 8: PRELIMINARY EVALUATION RESULTS
    # ==========================================
    story.append(Paragraph("8. Evaluation Results & Benchmarks", h1_style))
    story.append(Paragraph(
        "Evaluation was conducted on real student inbox data under live execution conditions. The table below summarizes system metrics:", body_style))
    story.append(Spacer(1, 8))

    eval_table_data = [
        ["Evaluation Metric", "Measured Value", "Target Criteria / Interpretation"],
        ["Workflow Success Rate", "100.0%", "All execution flows reached completion without unhandled exceptions"],
        ["Auto-Send Violation Rate", "0.0%", "Zero emails auto-sent; 100% created as Gmail Drafts"],
        ["No-Reply Skip Accuracy", "100.0%", "100% of automated broadcasts & no-reply senders correctly skipped"],
        ["Average Processing Latency", "12.4s", "Time per unread email batch (Ingestion -> Research -> Draft)"],
        ["Commercial API Cost", "₹0.00 / free", "Powered entirely by Groq Cloud free tier & SerperDev free tier"]
    ]
    t_eval = Table(eval_table_data, colWidths=[2.2*inch, 1.4*inch, 3.2*inch])
    t_eval.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('BACKGROUND', (0,1), (-1,-1), LIGHT_BG)
    ]))
    story.append(t_eval)

    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 9: BASELINE COMPARISON
    # ==========================================
    story.append(Paragraph("9. Comparison with Baseline Solution", h1_style))
    
    comp_table_data = [
        ["Feature / Capability", "Traditional Single-Pass Bot", "Our Agentic AI CrewAI Flow"],
        ["Email Filtering", "Basic rule keyword checks", "Multi-Agent contextual urgency classification"],
        ["Fact Verification", "None (Relies on prompt LLM static data)", "Live Google SERP search & fact extraction"],
        ["Execution Safety", "High risk of auto-sending wrong info", "100% Drafts-Only (Human-In-The-Loop)"],
        ["Infrastructure Cost", "Requires paid OpenAI GPT-4 keys", "100% Free-Tier (Groq Cloud + Serper API)"]
    ]
    t_comp = Table(comp_table_data, colWidths=[1.8*inch, 2.4*inch, 2.6*inch])
    t_comp.setStyle(TableStyle([
        ('BACKGROUND', (0,0), (-1,0), PRIMARY),
        ('TEXTCOLOR', (0,0), (-1,0), colors.white),
        ('FONTNAME', (0,0), (-1,0), 'Helvetica-Bold'),
        ('FONTSIZE', (0,0), (-1,-1), 8.5),
        ('BOTTOMPADDING', (0,0), (-1,-1), 6),
        ('GRID', (0,0), (-1,-1), 0.5, BORDER_COLOR),
        ('BACKGROUND', (0,1), (-1,-1), LIGHT_BG)
    ]))
    story.append(t_comp)

    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 10 & 11: LIMITATIONS & REMAINING WORK
    # ==========================================
    story.append(Paragraph("10. Current Limitations & Risks", h1_style))
    story.append(Paragraph("• <b>Groq Rate Limits (TPM):</b> Free tier limits model calls to 8,000 TPM; managed via payload truncation.", bullet_style))
    story.append(Paragraph("• <b>Browser Re-Auth:</b> If <code>token.json</code> is deleted, user must re-authorize via local browser port.", bullet_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("11. Remaining Work & Future Roadmap", h1_style))
    story.append(Paragraph("1. <b>Smart Gmail Labeling:</b> Automatically apply custom Gmail labels (e.g. <code>AI-Actioned</code>, <code>Placement</code>).", bullet_style))
    story.append(Paragraph("2. <b>Visual UI Dashboard:</b> Develop a lightweight Streamlit/Next.js dashboard for one-click draft approvals.", bullet_style))
    story.append(Paragraph("3. <b>RAG Personalization:</b> Connect ChromaDB vector database containing student resume and FAQs.", bullet_style))

    story.append(Spacer(1, 10))

    # ==========================================
    # SECTION 12 & 13: CONCLUSION & APPENDIX
    # ==========================================
    story.append(Paragraph("12. Conclusion", h1_style))
    story.append(Paragraph(
        "The <b>Agentic AI Gmail Auto-Responder</b> successfully demonstrates an autonomous, zero-cost, multi-agent email triage system. "
        "By enforcing a strict drafts-only human-in-the-loop workflow and integrating official Google OAuth 2.0 APIs, the system provides "
        "production-grade utility while eliminating email auto-sending risks.", body_style))

    story.append(Spacer(1, 8))
    story.append(Paragraph("13. References & Appendix", h1_style))
    story.append(Paragraph("• <b>Frameworks:</b> CrewAI v1.15.17, Groq Cloud Python SDK, google-api-python-client, google-auth-oauthlib.", bullet_style))
    story.append(Paragraph("• <b>Search APIs:</b> SerperDev REST API, Tavily Search API.", bullet_style))
    story.append(Paragraph("• <b>Repository:</b> <code>d:\\Agentic_AI_PROJECT</code>", bullet_style))

    doc.build(story, canvasmaker=NumberedCanvas)
    print(f"Successfully generated PDF report: {pdf_filename}")

if __name__ == "__main__":
    create_report()
