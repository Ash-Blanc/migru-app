from agno.agent import Agent
from agno.models.google import Gemini
from agno.models.mistral import MistralChat
from agno.os import AgentOS
from app.tools import get_forecast, log_attack, get_status, update_status, get_recent_logs

def get_migru_agent(gemini_key: str = None, mistral_key: str = None):
    """
    Returns an Agno Agent configured for the Migru health assistant.
    Supports dynamic API key injection.
    """
    model = None
    
    # Priority: Mistral Key -> Gemini Key -> Env Vars
    if mistral_key:
        model = MistralChat(id="mistral-large-latest", api_key=mistral_key)
    elif gemini_key:
        model = Gemini(id="gemini-2.0-flash-exp", api_key=gemini_key)
    else:
        # Fallback to default (env vars handled by library or default config)
        # Defaulting to Gemini for this prototype
        model = Gemini(id="gemini-2.0-flash-exp")

    return Agent(
        name="Migru Voice Agent",
        model=model,
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

# Initialize the default agent (can be overridden per request in custom endpoints if needed)
# For AgentOS standard endpoints, this default instance is used.
migru_agent = get_migru_agent()

# Create the AgentOS instance
agent_os = AgentOS(
    id="migru-os",
    name="Migru Agent OS",
    description="Backend OS for Migru App",
    agents=[migru_agent],
    # You can add teams, workflows, knowledge, etc. here
)
