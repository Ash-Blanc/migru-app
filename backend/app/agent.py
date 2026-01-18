from agno.agent import Agent
from agno.models.google import Gemini
from backend.app.tools import get_forecast, log_attack, get_status, update_status, get_recent_logs
import os

# You would typically load the API key from environment variables
# os.environ["GOOGLE_API_KEY"] = "..."

def get_migru_agent():
    """
    Returns an Agno Agent configured for the Migru health assistant.
    """
    return Agent(
        name="Migru Voice Agent",
        model=Gemini(id="gemini-2.0-flash-exp"),
        instructions=[
            "You are Migru, an empathetic AI assistant for migraine management.",
            "Your goal is to help the user track their health, provide forecasts, and log attacks via voice.",
            "Be concise, calm, and supportive.",
            "When a user reports pain, be empathetic first, then ask for details to log it.",
            "Use the provided tools to fetch data or perform actions."
        ],
        tools=[get_forecast, log_attack, get_status, update_status, get_recent_logs],
        markdown=True
    )
