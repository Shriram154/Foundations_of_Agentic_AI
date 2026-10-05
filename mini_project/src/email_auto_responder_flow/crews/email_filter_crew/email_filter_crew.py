import os
import time
import requests
from crewai import Agent, Crew, LLM, Process, Task
from crewai.project import CrewBase, agent, crew, task
from crewai.tools import tool

from email_auto_responder_flow.tools.create_draft import create_draft


@tool("Web Search")
def web_search_tool(query: str) -> str:
    """Search the web for background information. Input must be a search query string."""
    try:
        api_key = os.environ.get("SERPER_API_KEY", "")
        if api_key:
            url = "https://google.serper.dev/search"
            headers = {'X-API-KEY': api_key, 'Content-Type': 'application/json'}
            res = requests.post(url, headers=headers, json={"q": str(query)}).json()
            snippets = [item.get("snippet", "") for item in res.get("organic", [])[:2]]
            return " ".join(snippets)[:250]
    except Exception:
        pass
    return f"Background information for {query}"


@CrewBase
class EmailFilterCrew:
    """Email Filter Crew"""

    agents_config = "config/agents.yaml"
    tasks_config = "config/tasks.yaml"

    @property
    def llm(self):
        # Support Google Gemini API if present
        if os.environ.get("GEMINI_API_KEY"):
            return LLM(
                model="gemini/gemini-1.5-flash",
                api_key=os.environ["GEMINI_API_KEY"],
            )
        # Groq API open-source model with max retries and fallback delay
        elif os.environ.get("GROQ_API_KEY"):
            return LLM(
                model="openai/openai/gpt-oss-20b",
                base_url="https://api.groq.com/openai/v1",
                api_key=os.environ["GROQ_API_KEY"],
                max_retries=5,
            )
        else:
            return LLM(model="gpt-4o-mini")

    @agent
    def email_filter_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["email_filter_agent"],
            tools=[web_search_tool],
            llm=self.llm,
            verbose=True,
            allow_delegation=False,
            max_retry_limit=3,
        )

    @agent
    def email_action_agent(self) -> Agent:
        return Agent(
            config=self.agents_config["email_action_agent"],
            llm=self.llm,
            verbose=True,
            tools=[web_search_tool],
            max_retry_limit=3,
        )

    @agent
    def email_response_writer(self) -> Agent:
        return Agent(
            config=self.agents_config["email_response_writer"],
            llm=self.llm,
            verbose=True,
            tools=[web_search_tool, create_draft],
            max_retry_limit=3,
        )

    @task
    def filter_emails_task(self) -> Task:
        return Task(config=self.tasks_config["filter_emails"])

    @task
    def action_required_emails_task(self) -> Task:
        return Task(config=self.tasks_config["action_required_emails"])

    @task
    def draft_responses_task(self) -> Task:
        return Task(config=self.tasks_config["draft_responses"])

    @crew
    def crew(self) -> Crew:
        """Creates the Email Filter Crew"""
        return Crew(
            agents=self.agents,
            tasks=self.tasks,
            process=Process.sequential,
            verbose=True,
        )
